package main

import (
	"mm-tradebot/internal/config"
	"sync"
)
import (
	BybitClient "mm-tradebot/pkg/api/bybit"
	TradeCalculator "mm-tradebot/pkg/calculator"
)

import (
	PositionRepository "mm-tradebot/internal/repository/position"
)

import (
	PositionService "mm-tradebot/internal/service/position"
)

import (
	CancelOrder "mm-tradebot/internal/app/cancel-order"
	OpenPosition "mm-tradebot/internal/app/open-position"
	PositionWatcher "mm-tradebot/internal/app/position-watcher"
	SetStop "mm-tradebot/internal/app/set-stop"
)

func main() {
	cfg := config.New()
	bybitClient := BybitClient.New(cfg.ApiKey, cfg.ApiSecret)

	tradeCalculator := TradeCalculator.New(cfg.Maker, cfg.Taker)

	positionRepository := PositionRepository.New()
	positionService := PositionService.New(
		positionRepository,
		bybitClient,
		tradeCalculator,
		cfg,
	)

	mu := sync.Mutex{}
	go func() {
		OpenPosition.Start(
			&mu,
			cfg,
			positionService,
		)
	}()

	go func() {
		PositionWatcher.Start(
			&mu,
			cfg,
			positionService,
		)
	}()

	go func() {
		SetStop.Start(
			&mu,
			cfg,
			positionService,
		)
	}()

	CancelOrder.Start(
		&mu,
		cfg,
		positionService,
	)
}
