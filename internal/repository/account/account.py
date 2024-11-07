from decimal import Decimal

from internal import model


class AccountRepository(model.IAccountRepository):
    def __init__(
            self,
            in_memory_kv_db: model.IInMemoryKvDB,
    ):
        self.in_memory_kv_db = in_memory_kv_db

    def init_account(self, balance: str):
        self.in_memory_kv_db.set("balance", balance)
        self.in_memory_kv_db.set("start_balance", balance)
        self.in_memory_kv_db.set("total_profit_in_percent", "0")
        self.in_memory_kv_db.set("total_profit_in_dollars", "0")
        self.in_memory_kv_db.set("count_profit_positions", "0")
        self.in_memory_kv_db.set("count_loss_positions", "0")
        self.in_memory_kv_db.set("count_active_positions", "0")
        self.in_memory_kv_db.set("count_closed_positions", "0")

    def get_account(self) -> model.Account:
        return model.Account(
            balance=self.in_memory_kv_db.get("balance"),
            start_balance=self.in_memory_kv_db.get("start_balance"),
            total_profit_in_percent=self.in_memory_kv_db.get("total_profit_in_percent"),
            total_profit_in_dollars=self.in_memory_kv_db.get("total_profit_in_dollars"),
            count_profit_positions=self.in_memory_kv_db.get("count_profit_positions"),
            count_loss_positions=self.in_memory_kv_db.get("count_loss_positions"),
            count_active_positions=self.in_memory_kv_db.get("count_active_positions"),
            count_closed_positions=self.in_memory_kv_db.get("count_closed_positions")
        )

    def update_balance(self, amount: Decimal):
        balance = Decimal(self.in_memory_kv_db.get("balance"))
        self.in_memory_kv_db.set("balance", balance + amount)
