from internal import model


class AccountService(model.IAccountService):
    def __init__(
            self,
            account_repo: model.IAccountRepository,
            market_client: model.IMarketClient,
    ):
        self.account_repo = account_repo
        self.market_client = market_client

    def init_account(self):
        wallet = self.market_client.wallet_by_symbol("USDT")
        balance = wallet.coin[0].walletBalance

        self.account_repo.init_account(balance)

    def get_account(self) -> model.Account:
        return self.account_repo.get_account()
