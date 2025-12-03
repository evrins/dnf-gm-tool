import enum
import zlib
from typing import List, Tuple

from loguru import logger

from config import config
from dnfpkgtool.db.entity.character_inventory import CharacterInventory
from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot
from dnfpkgtool.db.entity.magic_seal import MagicSeal
from dnfpkgtool.db.repo.account_cargo_repo import get_account_cargo_repo
from dnfpkgtool.db.repo.character_inventory_expand_repo import (
    get_character_inventory_expand_repo,
)
from dnfpkgtool.db.repo.inventory_repo import get_inventory_repo
from dnfpkgtool.pvf.pvf_reader import PVFReader
from dnfpkgtool.repo.equipment_repo import (
    EquipmentIdNotFoundException,
    build_equipment_repo_parquet,
)
from dnfpkgtool.repo.magic_seal_repo import (
    build_magic_seal_parquet,
)
from dnfpkgtool.repo.orb_repo import build_orb_repo_parquet
from dnfpkgtool.repo.quest_repo import build_quest_repo_parquet
from dnfpkgtool.repo.repo_manager import (
    get_equipment_repo,
    get_magic_seal_repo,
    get_skill_repo,
    get_stackable_repo,
)
from dnfpkgtool.repo.skill_repo import build_skill_repo_parquet
from dnfpkgtool.repo.stackable_repo import (
    StackableIdNotFoundException,
    build_stackable_repo_parquet,
)


class InventoryLoc(enum.Enum):
    Backpack = 0
    Creatures = 1
    Equipment = 2


class ItemType(enum.Enum):
    Equipment = 1
    Stackable = 2


class ItemService:
    def __init__(self):
        self.stackable_repo = get_stackable_repo()
        self.equipment_repo = get_equipment_repo()
        self.magic_seal_repo = get_magic_seal_repo()
        self.account_cargo_repo = get_account_cargo_repo()
        self.character_cargo_repo = get_character_inventory_expand_repo()
        self.character_inventory = get_inventory_repo()

    # 账户仓库
    def get_current_account_cargo(self) -> List[DnfItemSlot]:
        account_id = config.get_current_account_id()
        account_cargo = self.account_cargo_repo.query_by_m_id(account_id)
        if not account_cargo:
            return []
        return self.unpack_blob_items(account_cargo.cargo)

    # 角色仓库
    def get_current_character_cargo(self) -> List[DnfItemSlot]:
        character_no = config.get_current_character_no()
        character_cargo = self.character_cargo_repo.query_by_character_no(character_no)
        return self.unpack_blob_items(character_cargo.cargo)

    # 角色装备 角色宠物 角色背包
    def get_current_character_inventory(self) -> CharacterInventory:
        character_no = config.get_current_character_no()
        inventory = self.character_inventory.query_by_character_no(character_no)
        ci = CharacterInventory()
        ci.equipments = self.unpack_blob_items(inventory.equipment_slot)
        ci.creatures = self.unpack_blob_items(inventory.creature)
        ci.backpack = self.unpack_blob_items(inventory.inventory)

        return ci

    # 更新账户仓库中的物品
    def update_current_account_cargo(self, item: DnfItemSlot) -> None:
        account_id = config.get_current_account_id()
        account_cargo = self.account_cargo_repo.query_by_m_id(account_id)
        new_cargo = self.update_blob_items(account_cargo.cargo, item)
        self.account_cargo_repo.update_cargo_by_m_id(account_id, new_cargo)

    # 更新角色仓库中的物品
    def update_current_character_cargo(self, item: DnfItemSlot) -> None:
        character_no = config.get_current_character_no()
        character_cargo = self.character_cargo_repo.query_by_character_no(character_no)
        new_cargo = self.update_blob_items(character_cargo.cargo, item)
        self.character_cargo_repo.update_cargo_by_character_no(character_no, new_cargo)

    # 更新角色装备, 角色宠物, 角色装备 中的物品
    def update_current_character_inventory(
            self, item: DnfItemSlot, inventory_loc: InventoryLoc
    ) -> None:
        character_no = config.get_current_character_no()
        inventory = self.character_inventory.query_by_character_no(character_no)
        if inventory_loc == InventoryLoc.Backpack:
            new_inventory = self.update_blob_items(inventory.inventory, item)
            self.character_inventory.update_inventory_by_character_no(
                character_no, new_inventory
            )
        elif inventory_loc == InventoryLoc.Equipment:
            new_equipment = self.update_blob_items(inventory.equipment_slot, item)
            self.character_inventory.update_equipments_by_character_no(
                character_no, new_equipment
            )
        elif inventory_loc == InventoryLoc.Creatures:
            new_creatures = self.update_blob_items(inventory.creature, item)
            self.character_inventory.update_creatures_by_character_no(
                character_no, new_creatures
            )
        else:
            raise ValueError(f'Inventory location not supported {inventory_loc}')

    def update_blob_items(self, buf: bytes, item: DnfItemSlot) -> bytes:
        prefix = buf[:4]
        items_bytes = bytearray(zlib.decompress(buf[4:]))
        idx = item.display_idx
        items_bytes[idx * 61: idx * 61 + 61] = item.to_bytes()
        res = prefix + zlib.compress(items_bytes)
        return res

    def unpack_blob_items(self, buf: bytes) -> List[DnfItemSlot]:
        buf = zlib.decompress(buf[4:])
        num = len(buf) // 61
        res = []
        for i in range(num):
            item = self.unpack_blob_item(buf[i * 61: (i + 1) * 61])
            item.display_idx = i
            res.append(item)
        return res

    def unpack_blob_item(self, buf: bytes) -> DnfItemSlot:
        item = DnfItemSlot(buf)
        if item.id:
            try:
                if item.type == 0x01 or item.type == 0x05 or item.type == 0x06:
                    inner_item = self.equipment_repo.query_by_id(item.id)
                    item.equipment_type = inner_item['equipment_type']
                    item.endurance_limit = inner_item['durability']
                    item.display_category = inner_item['display_equipment_type']
                else:
                    inner_item = self.stackable_repo.query_by_id(item.id)
                    item.stack_limit = inner_item['stack_limit']
                    item.display_category = inner_item['display_stackable_type']
                item.display_name = inner_item['name']
                item.display_rarity = inner_item['rarity']
                item.display_rarity_name = inner_item['display_rarity']
            except StackableIdNotFoundException:
                item.is_missing = True
                item.display_name = f'物品 ID {item.id} 不存在'
            except EquipmentIdNotFoundException:
                item.is_missing = True
                item.display_name = f'装备 ID {item.id} 不存在'

        magic_seal_range_list = [(0, 3), (3, 6), (6, 9), (10, 13)]
        for idx, it in enumerate(magic_seal_range_list):
            ms = MagicSeal.from_bytes(item.magic_seal[it[0]: it[1]])
            if ms.id == 0:
                continue
            ms.name = self.magic_seal_repo.query_by_id(ms.id)['name']
            item.display_magic_seals[idx] = ms
        return item

    def find_by_id(self, item_id: int) -> Tuple[ItemType, dict]:
        try:
            item = self.stackable_repo.query_by_id(item_id)
            return ItemType.Stackable, item
        except StackableIdNotFoundException:
            logger.info(f'Item {item_id} not found in stackable')

        try:
            item = self.equipment_repo.query_by_id(item_id)
            return ItemType.Equipment, item
        except EquipmentIdNotFoundException:
            logger.warning(f'item with id {item_id} not found in equipment')

        raise ValueError(f'item with id {item_id} not found')


def get_item_service() -> ItemService:
    return ItemService()


def build_repo_parquet(fp: str):
    reader = PVFReader(fp)
    build_equipment_repo_parquet(
        reader.get_equipment_list(), config.get_equipment_parquet_file_path()
    )
    build_stackable_repo_parquet(
        reader.get_stackable_dict(), config.get_stackable_parquet_file_path()
    )
    build_magic_seal_parquet(
        reader.get_magic_seal_dict(), config.get_magic_seal_parquet_file_path()
    )
    build_skill_repo_parquet(
        reader.get_skill_list(), config.get_skill_parquet_file_path()
    )

    # build orb repo should come after stackable_repo and skill_repo
    stackable_repo = get_stackable_repo()
    skill_repo = get_skill_repo()
    build_orb_repo_parquet(
        stackable_repo, skill_repo, config.get_orb_parquet_file_path()
    )

    build_quest_repo_parquet(
        reader.get_quest_list(), config.get_quest_parquet_file_path()
    )

    reader.close()
