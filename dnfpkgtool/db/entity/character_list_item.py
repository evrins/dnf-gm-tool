from pydantic import BaseModel


class CharacterListItem(BaseModel):
    account_id: int = 0
    character_no: int = 0
    character_name: str = ''
    level: int = 0
    job: str = ''
    expert_job: str = ''

    online: bool = False

    @property
    def online_text(self) -> str:
        return '在线' if self.online else '离线'
