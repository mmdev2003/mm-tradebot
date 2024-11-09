package model

import (
	"github.com/shopspring/decimal"
	"mm-tradebot/internal/model/api"
	"time"
)

type IAccountService interface {
	Account() *Account
}
type IAccountRepository interface {
	Account() *Account
}

type IPositionService interface {
	OpenLimitOrder(symbol string, side Side, status Status, size decimal.Decimal, limitDepth decimal.Decimal, leverage decimal.Decimal) error
	SetTakeProfit(symbol string, side Side, price decimal.Decimal, size decimal.Decimal, commissionInPercent decimal.Decimal, takeInPercent decimal.Decimal) error
	CancelLimitOrder(symbol string) error
	Position() *Position

	CalcLimitOrderPrice(symbol string, side Side, limitDepth decimal.Decimal) (decimal.Decimal, error)
	CalcCancelTime(openTime time.Time, secondsToCancelLimitOrder int) time.Time
}

type IPositionRepository interface {
	OpenLimitOrder(symbol string, side Side, status Status, size decimal.Decimal, limitOrderPrice decimal.Decimal)
	CancelLimitOrder()
	OpenPosition(openPrice decimal.Decimal)
	ReopenLimitOrder(status Status, size decimal.Decimal, price decimal.Decimal)
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
}

type ITradeCalculator interface {
	CalcLimitOrderPrice(price, limitDepth decimal.Decimal, side Side) decimal.Decimal
	CalcCommission(commissionInPercent decimal.Decimal, price decimal.Decimal, size decimal.Decimal) decimal.Decimal
	CalcTakePrice(price decimal.Decimal, side Side, size decimal.Decimal, commissionInDollar decimal.Decimal, commissionInPercent decimal.Decimal, takeInPercent decimal.Decimal) decimal.Decimal
}
