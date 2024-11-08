package account

import (
	"mm-tradebot/internal/model"
)

func New(
	account *model.Account,
) *RepositoryAccount {
	return &RepositoryAccount{
		account: account,
	}
}

type RepositoryAccount struct {
	account *model.Account
}

func (accountRepo *RepositoryAccount) Account() *model.Account {
	return accountRepo.account
}
