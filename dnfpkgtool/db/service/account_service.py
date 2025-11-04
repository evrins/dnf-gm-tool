from typing import List

from dnfpkgtool.db.entity.character_list_item import CharacterListItem
from dnfpkgtool.db.model.character_info import CharacterInfo
from dnfpkgtool.db.repo.character_info_repo import CharacterInfoRepo
from dnfpkgtool.db.repo.event_1306_account_reward_repo import Event1306AccountRewardRepo
from dnfpkgtool.db.repo.login_account_3_repo import LoginAccount3Repo


class AccountService:
    def __init__(self):
        self.login_account_3_repo = LoginAccount3Repo()
        self.event_1306_account_reward_repo = Event1306AccountRewardRepo()
        self.character_info_repo = CharacterInfoRepo()

    def get_all_valid_character_list(self) -> List[CharacterInfo]:
        return self.character_info_repo.query_all_valid_character_info_list()

    def get_online_character_list(self) -> List[CharacterInfo]:
        logged_in_account_m_id_list = (
            self.login_account_3_repo.query_logged_account_m_id()
        )
        character_no_list = (
            self.event_1306_account_reward_repo.query_character_no_by_m_id_list(
                logged_in_account_m_id_list
            )
        )
        character_list = self.character_info_repo.query_by_character_no_list(
            character_no_list
        )
        return character_list

    def search_characters(self, name: str) -> List[CharacterListItem]:
        logged_in_account_m_id_list = (
            self.login_account_3_repo.query_logged_account_m_id()
        )
        online_character_no_list = (
            self.event_1306_account_reward_repo.query_character_no_by_m_id_list(
                logged_in_account_m_id_list
            )
        )
        online_character_set = set(online_character_no_list)
        res: List[CharacterListItem] = []

        character_list = self.character_info_repo.query_by_name(name.strip())
        for it in character_list:
            res.append(
                CharacterListItem(
                    account_id=it.m_id,
                    character_no=it.charac_no,
                    character_name=it.charac_name,
                    level=it.lev,
                    job=get_job_name_by_job_grow_type(it.job, it.grow_type),
                    expert_job=get_expert_job_name(it.expert_job),
                    online=it.charac_no in online_character_set,
                )
            )

        return res


expert_jobs = ['无副职业', '附魔师', '炼金术师', '分解师', '控偶师']


def get_expert_job_name(idx: int) -> str:
    return expert_jobs[idx]


jobs = [
    [
        '鬼剑士',
        '剑魂',
        '鬼泣',
        '狂战士',
        '阿修罗',
        '剑魔',
    ],
    ['格斗家', '气功师', '散打', '街霸', '柔道家', '格斗家'],
    ['神枪手', '漫游枪手', '枪炮师', '机械师', '弹药专家', '邪神'],
    ['魔法师', '元素师', '召唤师', '战斗法师', '魔道学者', '魔法师'],
    ['圣职者', '圣骑士', '蓝拳圣使', '驱魔师', '复仇者', '金刚力士'],
    ['神枪手', '漫游枪手', '枪炮师', '机械师', '弹药专家', '神枪手'],
    ['暗夜使者', '刺客', '死灵术士', '忍者', '影武者', '暗夜使者'],
    ['格斗家', '气功师', '散打', '街霸', '柔道家', '格斗家'],
    ['魔法师', '元素爆破师', '冰结师', '战斗法师', '魔道学者', '魔法师'],
    ['黑暗武士', '剑魂', '鬼泣', '狂战士', '阿修罗', '剑魔'],
    ['缔造者', '元素师', '召唤师', '战斗法师', '魔道学者', '魔法师'],
]


def get_job_name_by_job_grow_type(job: int, grow_type: int) -> str:
    grow_type_idx = grow_type % 16
    return jobs[job][grow_type_idx]
