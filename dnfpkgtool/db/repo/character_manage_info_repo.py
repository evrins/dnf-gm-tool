from sqlalchemy import delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_manage_info import CharacterManageInfo
from dnfpkgtool.db.repo.base_repo import BaseRepo


class CharacterManageInfoRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    def delete_by_character_no(self, character_no: int) -> None:
        with Session(self.get_engine()) as session:
            stmt = delete(CharacterManageInfo).where(
                CharacterManageInfo.character_no == character_no
            )
            session.execute(stmt)
            session.commit()

    def upsert(self, it: CharacterManageInfo):
        with Session(self.get_engine()) as session:
            stmt = (insert(CharacterManageInfo)
            .values(
                character_no=it.character_no,
                max_equip_level=it.max_equip_level,
            )
            .on_duplicate_key_update(
                max_equip_level=it.max_equip_level,
            ))
            session.execute(stmt)
            session.commit()


def get_character_manage_info_repo() -> CharacterManageInfoRepo:
    return CharacterManageInfoRepo()
