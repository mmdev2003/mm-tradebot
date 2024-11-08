package position

import (
	"github.com/shopspring/decimal"
	"log/slog"
	"mm-tradebot/internal/model"
	"time"
)

func New(
	positionRepo model.IPositionRepository,
	bybitClient model.IBybitClient,
	tradeCalculator model.ITradeCalculator,
) *ServicePosition {
	return &ServicePosition{
		positionRepo:    positionRepo,
		bybitClient:     bybitClient,
		tradeCalculator: tradeCalculator,
	}
}

type ServicePosition struct {
	positionRepo    model.IPositionRepository
	bybitClient     model.IBybitClient
	tradeCalculator model.ITradeCalculator
}

func (positionService *ServicePosition) OpenLimitOrder(
	symbol string,
	side model.Side,
	status model.Status,
	size decimal.Decimal,
	limitDepth decimal.Decimal,
) error {
	limitOrderPrice, err := positionService.CalcLimitOrderPrice(
		symbol,
		side,
		limitDepth,
	)
	if err != nil {
		slog.Error(err.Error())
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
