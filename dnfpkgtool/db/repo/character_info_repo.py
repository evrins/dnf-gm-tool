from functools import wraps
from typing import Callable, List

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dnfpkgtool.db.model.character_info import CharacterInfo
from dnfpkgtool.db.repo.base_repo import BaseRepo
from util import decode_string_to_utf8


def apply_map_function(map_func: Callable[[CharacterInfo], CharacterInfo]):
    """
    Decorator that applies a map function to each CharacterInfo in the returned list.
    
    Args:
        map_func: A function that takes a CharacterInfo and returns a modified CharacterInfo
        
    Example:
        @apply_map_function(lambda char: fix_character_encoding(char))
        def query_all_character_info_list(self) -> List[CharacterInfo]:
            ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, list):
                return [map_func(item) for item in result]
            elif isinstance(result, CharacterInfo) and result is not None:
                return map_func(result)
            return result

        return wrapper

    return decorator


def fix_character_name_encoding(character: CharacterInfo) -> CharacterInfo:
    """
    Fix mojibake in character names by converting cp1252 misinterpreted UTF-8 back to proper UTF-8.
    
    Args:
        character: CharacterInfo object with potentially garbled character_name
        
    Returns:
        CharacterInfo with fixed character_name encoding
    """
    try:
        # Try to fix mojibake: encode as cp1252 to get original UTF-8 bytes, then decode as UTF-8
        fixed_name = decode_string_to_utf8(character.character_name)
        character.character_name = fixed_name
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If conversion fails, the name is probably already correct or has other encoding issues
        pass
    return character


class CharacterInfoRepo(BaseRepo):
    def __init__(self):
        super().__init__('taiwan_cain')

    @apply_map_function(lambda char: recode_character_name(char))
    def query_all_character_info_list(self) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInfo)
            return list(session.scalars(stmt).all())

    @apply_map_function(lambda char: recode_character_name(char))
    def query_all_valid_character_info_list(self) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInfo).where(CharacterInfo.delete_flag == 0)
            return list(session.scalars(stmt).all())

    @apply_map_function(lambda char: recode_character_name(char))
    def query_by_character_no_list(self, character_no_list) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = select(CharacterInfo).where(
                CharacterInfo.character_no.in_(character_no_list)
            )
            return list(session.scalars(stmt).all())

    @apply_map_function(lambda char: recode_character_name(char))
    def query_by_name(self, name: str) -> List[CharacterInfo]:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterInfo)
                .where(CharacterInfo.character_name.ilike(f'%{name}%'))
                .order_by(CharacterInfo.character_no.desc())
            )
            return list(session.scalars(stmt).all())

    @apply_map_function(lambda char: recode_character_name(char))
    def query_by_character_no(self, character_no: int) -> CharacterInfo:
        with Session(self.get_engine()) as session:
            stmt = (
                select(CharacterInfo).where(CharacterInfo.character_no == character_no)
            ).limit(1)
            return session.scalars(stmt).first()

    def update_character_info(self, character_info: CharacterInfo):
        with Session(self.get_engine()) as session:
            stmt = (
                update(CharacterInfo)
                .where(CharacterInfo.character_no == character_info.character_no)
                .values(
                    lev=character_info.lev,
                    job=character_info.job,
                    grow_type=character_info.grow_type,
                )
            )
            session.execute(stmt)
            session.commit()


def recode_character_name(it: CharacterInfo) -> CharacterInfo:
    it.character_name = decode_string_to_utf8(it.character_name)
    return it


def get_character_info_repo() -> CharacterInfoRepo:
    return CharacterInfoRepo()
