from pydantic import BaseModel


class AccountMoney(BaseModel):
    # 账号金库金币
    account_cargo_money: int = 0
    # 背包金币
    backpack_money: int = 0
    # 复活币
    pay_coin: int = 0
