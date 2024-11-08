package main

import (
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"sync"
)
import (
	BybitClient "mm-tradebot/pkg/api/bybit"
	TradeCalculator "mm-tradebot/pkg/calculator"
)

import (
	AccountRepository "mm-tradebot/internal/repository/account"
	PositionRepository "mm-tradebot/internal/repository/position"
)

import (
	AccountService "mm-tradebot/internal/service/account"
	PositionService "mm-tradebot/internal/service/position"
)

import (
	OpenPosition "mm-tradebot/internal/app/open-position"
)

func main() {
	cfg := config.New()
	bybitClient := BybitClient.New(cfg.ApiKey, cfg.ApiSecret)
	balance := bybitClient.Balance()

	account := model.Account{
		Balance:      balance,
		StartBalance: balance,
	}

	tradeCalculator := TradeCalculator.New(cfg.Maker, cfg.Taker)

	accountRepository := AccountRepository.New(&account)
	accountService := AccountService.New(accountRepository)

	positionRepository := PositionRepository.New()
	positionService := PositionService.New(
		positionRepository,
		bybitClient,
		tradeCalculator,
	)

	mu := sync.Mutex{}
	wg := sync.WaitGroup{}

	go func() {
		OpenPosition.Start(
			&mu,
			cfg,
			accountService,
			positionService,
		)
	}()

	wg.Wait()
}
