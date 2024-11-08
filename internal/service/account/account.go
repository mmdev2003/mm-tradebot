package account

import "mm-tradebot/internal/model"

func New(
	accountRepo model.IAccountRepository,
) *ServiceAccount {
	return &ServiceAccount{
		accountRepo: accountRepo,
	}
}

type ServiceAccount struct {
	accountRepo model.IAccountRepository
}

func (accountService *ServiceAccount) Account() *model.Account {
	return accountService.accountRepo.Account()
}
