package position

import (
	"github.com/shopspring/decimal"
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"time"
)

func New(
	positionRepo model.IPositionRepository,
	bybitClient model.IBybitClient,
	tradeCalculator model.ITradeCalculator,
	cfg *config.Config,
) *ServicePosition {
	return &ServicePosition{
		positionRepo:    positionRepo,
		bybitClient:     bybitClient,
		tradeCalculator: tradeCalculator,
		cfg:             cfg,
	}
}

type ServicePosition struct {
	positionRepo    model.IPositionRepository
	bybitClient     model.IBybitClient
	tradeCalculator model.ITradeCalculator
	cfg             *config.Config
}

func (positionService *ServicePosition) OpenPosition(
	symbol string,
	side model.Side,
	openPriceActual decimal.Decimal,
	openPriceDB decimal.Decimal,
	size decimal.Decimal,
	takeInPercent decimal.Decimal,
) error {
	var commissionInPercent decimal.Decimal
	if openPriceActual.Equal(openPriceDB) {
		commissionInPercent = positionService.cfg.Maker
	} else {
		commissionInPercent = positionService.cfg.Taker
	}

	err := positionService.SetTakeProfit(
		symbol,
		side,
		openPriceActual,
		size,
		commissionInPercent,
		takeInPercent,
	)
	if err != nil {
		return err
	}

	positionService.positionRepo.OpenPosition(openPriceActual)
	return nil

}

func (positionService *ServicePosition) SetTakeProfit(
	symbol string,
	side model.Side,
	price decimal.Decimal,
	size decimal.Decimal,
	commissionInPercent decimal.Decimal,
	takeInPercent decimal.Decimal,
) error {
	commissionInDollar := positionService.tradeCalculator.CalcCommission(
		commissionInPercent,
		price,
		size,
	)
	takePrice := positionService.tradeCalculator.CalcTakePrice(
		price,
		side,
		size,
		commissionInDollar,
		commissionInPercent,
		takeInPercent,
	)
	err := positionService.bybitClient.SetTakeProfit(
		symbol,
		takePrice,
	)
	if err != nil {
		return err
	}
	return nil
}

func (positionService *ServicePosition) OpenLimitOrder(
	symbol string,
	side model.Side,
	status model.Status,
	size decimal.Decimal,
	limitDepth decimal.Decimal,
	leverage decimal.Decimal,
) error {
	limitOrderPrice, err := positionService.CalcLimitOrderPrice(
		symbol,
		side,
		limitDepth,
	)
	if err != nil {
		return err
	}

	err = positionService.bybitClient.OpenLimitOrder(
		symbol,
		side,
		limitOrderPrice,
		size,
		leverage,
	)
	if err != nil {
		return err
	}

	positionService.positionRepo.OpenLimitOrder(
		symbol,
		side,
		status,
		size,
		limitOrderPrice,
	)
	return nil
}

func (positionService *ServicePosition) CancelLimitOrder(
	symbol string,
) error {
	err := positionService.bybitClient.CancelAllOrder(symbol)
	if err != nil {
		return err
	}
	positionService.positionRepo.CancelLimitOrder()
	return nil
}

func (positionService *ServicePosition) CalcLimitOrderPrice(
	symbol string,
	side model.Side,
	limitDepth decimal.Decimal,
) (decimal.Decimal, error) {
	lastPrice, err := positionService.bybitClient.LastPrice(symbol)
	if err != nil {
		return decimal.Zero, err
	}

	limitOrderPrice := positionService.tradeCalculator.CalcLimitOrderPrice(
		lastPrice,
		limitDepth,
		side,
	)

	return limitOrderPrice, nil
}

func (positionService *ServicePosition) CalcCancelTime(
	openTime time.Time,
	secondsToCancelLimitOrder int,
) time.Time {
	cancelTime := openTime.Add(time.Duration(secondsToCancelLimitOrder) * time.Second)
	return cancelTime
}

func (positionService *ServicePosition) Position() *model.Position {
	position := positionService.positionRepo.Position()
	return position
}
