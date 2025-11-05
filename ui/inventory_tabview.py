from PySide6 import QtWidgets

from config import config
from dnfpkgtool.db.entity.dnf_item_slot import DnfItemSlot
from dnfpkgtool.db.entity.signals import gs
from dnfpkgtool.db.service.item_service import InventoryLoc, ItemService
from ui.components.inventory.inventory import InventoryWidget


class InventoryTabView(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.item_svc: ItemService = None
        self.creatures_tab: InventoryWidget = None
        self.equipments_tab: InventoryWidget = None
        self.backpack_tab: InventoryWidget = None
        self.character_cargo_tab: InventoryWidget = None
        self.account_cargo_tab: InventoryWidget = None

        self.item_svc = ItemService()

        self.account_cargo_tab = InventoryWidget([])
        self.account_cargo_tab.on_refresh.connect(self.refresh_account_cargo)
        self.account_cargo_tab.on_save.connect(self.save_account_cargo)
        self.account_cargo_tab.on_delete.connect(self.delete_account_cargo)
        self.addTab(self.account_cargo_tab, 'Account Cargo')

        self.character_cargo_tab = InventoryWidget([])
        self.character_cargo_tab.on_refresh.connect(self.refresh_character_cargo)
        self.character_cargo_tab.on_save.connect(self.save_character_cargo)
        self.character_cargo_tab.on_delete.connect(self.delete_character_cargo)
        self.addTab(self.character_cargo_tab, 'Character Cargo')

        self.backpack_tab = InventoryWidget([])
        self.backpack_tab.on_refresh.connect(self.refresh_character_inventory)
        self.backpack_tab.on_save.connect(self.save_backpack)
        self.backpack_tab.on_delete.connect(self.delete_backpack)
        self.addTab(self.backpack_tab, 'Backpack')

        self.equipments_tab = InventoryWidget([])
        self.equipments_tab.on_refresh.connect(self.refresh_character_inventory)
        self.equipments_tab.on_save.connect(self.save_equipments)
        self.equipments_tab.on_delete.connect(self.delete_equipments)
        self.addTab(self.equipments_tab, 'Equipment')

        self.creatures_tab = InventoryWidget([])
        self.creatures_tab.on_refresh.connect(self.refresh_character_inventory)
        self.creatures_tab.on_save.connect(self.save_creatures)
        self.creatures_tab.on_delete.connect(self.delete_creatures)
        self.addTab(self.creatures_tab, 'Creatures')

        gs.db_config_changed.connect(self.refresh_data)
        gs.pvf_changed.connect(self.refresh_data)

        gs.account_id_changed.connect(self.refresh_account_cargo)
        gs.character_no_changed.connect(self.refresh_character_cargo)
        gs.character_no_changed.connect(self.refresh_character_inventory)

        self.refresh_data()

    def refresh_data(self):
        if not config.have_valid_account_id_and_character_no():
            return

        self.refresh_account_cargo()
        self.refresh_character_cargo()
        self.refresh_character_inventory()

    def refresh_account_cargo(self):
        account_cargo = self.item_svc.get_current_account_cargo()
        self.account_cargo_tab.set_data(account_cargo)

    def save_account_cargo(self, new_item: DnfItemSlot):
        self.item_svc.update_current_account_cargo(new_item)
        self.refresh_account_cargo()

    # 删除操作就是将二进制序列中的一段置为空
    def delete_account_cargo(self, item: DnfItemSlot):
        self.item_svc.update_current_account_cargo(
            DnfItemSlot.with_idx(item.display_idx)
        )
        self.refresh_account_cargo()

    def refresh_character_cargo(self):
        character_cargo = self.item_svc.get_current_character_cargo()
        self.character_cargo_tab.set_data(character_cargo)

    def save_character_cargo(self, new_item: DnfItemSlot):
        self.item_svc.update_current_character_cargo(new_item)
        self.refresh_character_cargo()

    def delete_character_cargo(self, item: DnfItemSlot):
        self.item_svc.update_current_character_cargo(
            DnfItemSlot.with_idx(item.display_idx)
        )
        self.refresh_character_cargo()

    def refresh_character_inventory(self):
        ci = self.item_svc.get_current_character_inventory()
        self.backpack_tab.set_data(ci.backpack)
        self.equipments_tab.set_data(ci.equipments)
        self.creatures_tab.set_data(ci.creatures)

    def save_backpack(self, new_item: DnfItemSlot):
        self.item_svc.update_current_character_inventory(
            new_item, InventoryLoc.Backpack
        )
        self.refresh_character_inventory()

    def delete_backpack(self, item: DnfItemSlot):
        self.item_svc.update_current_character_inventory(
            DnfItemSlot.with_idx(item.display_idx), InventoryLoc.Backpack
        )
        self.refresh_character_inventory()

    def save_equipments(self, new_item: DnfItemSlot):
        self.item_svc.update_current_character_inventory(
            new_item, InventoryLoc.Equipment
        )
        self.refresh_character_inventory()

    def delete_equipments(self, item: DnfItemSlot):
        self.item_svc.update_current_character_inventory(
            DnfItemSlot.with_idx(item.display_idx), InventoryLoc.Equipment
        )
        self.refresh_character_inventory()

    def save_creatures(self, new_item: DnfItemSlot):
        self.item_svc.update_current_character_inventory(
            new_item, InventoryLoc.Creatures
        )
        self.refresh_character_inventory()

    def delete_creatures(self, item: DnfItemSlot):
        self.item_svc.update_current_character_inventory(
            DnfItemSlot.with_idx(item.display_idx), InventoryLoc.Creatures
        )
        self.refresh_character_inventory()
