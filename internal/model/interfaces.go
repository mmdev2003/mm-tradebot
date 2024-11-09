package model

import (
	"github.com/shopspring/decimal"
	"mm-tradebot/internal/model/api"
)

type IPositionService interface {
	OpenLimitOrder(symbol string, side Side, status Status, size decimal.Decimal, limitDepth decimal.Decimal, leverage decimal.Decimal) error
	OpenPosition(symbol string, side Side, openPriceActual decimal.Decimal, openPriceDB decimal.Decimal, size decimal.Decimal, takeInPercent decimal.Decimal) error
	CancelLimitOrder(symbol string) error
	ClosePosition(symbol string) error
	SetStop(symbol string, price decimal.Decimal, size decimal.Decimal, side Side, commissionInDollar decimal.Decimal, stopInPercent decimal.Decimal) error
	Position() *Position
}

type IPositionRepository interface {
	OpenLimitOrder(symbol string, side Side, status Status, size decimal.Decimal, limitOrderPrice decimal.Decimal)
	OpenPosition(openPrice decimal.Decimal, commissionInDollar decimal.Decimal)
	ReopenLimitOrder(status Status, size decimal.Decimal, price decimal.Decimal)
	CancelLimitOrder()
	ClosePosition()
	Position() *Position
}

type IBybitClient interface {
	Balance() decimal.Decimal
	PositionBySymbol(symbol string) (*api.BybitPosition, error)
	LastPrice(symbol string) (decimal.Decimal, error)
	CancelAllOrder(symbol string) error
	SetLeverage(symbol string, leverage decimal.Decimal) error
	OpenLimitOrder(symbol string, side Side, price decimal.Decimal, size decimal.Decimal, leverage decimal.Decimal) error
	SetTakeProfit(symbol string, takePrice decimal.Decimal) error
	SetStopLoss(symbol string, stopPrice decimal.Decimal) error
}

type ITradeCalculator interface {
	CalcLimitOrderPrice(price, limitDepth decimal.Decimal, side Side) decimal.Decimal
	CalcCommission(commissionInPercent decimal.Decimal, price decimal.Decimal, size decimal.Decimal) decimal.Decimal
	CalcTakePrice(price decimal.Decimal, side Side, size decimal.Decimal, commissionInDollar decimal.Decimal, takeInPercent decimal.Decimal) decimal.Decimal
	CalcStopPrice(price decimal.Decimal, side Side, size decimal.Decimal, commissionInDollar decimal.Decimal, stopInPercent decimal.Decimal) decimal.Decimal
}
