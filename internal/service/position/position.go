package position

import (
	"github.com/shopspring/decimal"
	"log/slog"
	"mm-tradebot/internal/model"
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

func (positionService *ServicePosition) Position(
	symbol string,
) *model.Position {
	position := positionService.positionRepo.Position(symbol)
	return position
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
