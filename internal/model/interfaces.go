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
	OpenLimitOrder(symbol string, side Side, status Status, size decimal.Decimal, limitDepth decimal.Decimal) error
	CancelLimitOrder(symbol string) error
	Position() *Position
	CalcLimitOrderPrice(symbol string, side Side, limitDepth decimal.Decimal) (decimal.Decimal, error)
	CalcCancelTime(openTime time.Time, secondsToCancelLimitOrder int) time.Time
}

type IPositionRepository interface {
	OpenLimitOrder(symbol string, side Side, status Status, size decimal.Decimal, limitOrderPrice decimal.Decimal)
	CancelLimitOrder()
	ReopenLimitOrder(status Status, size decimal.Decimal, price decimal.Decimal)
	Position() *Position
}

type IBybitClient interface {
	Balance() decimal.Decimal
	PositionBySymbol(symbol string) (*api.BybitPosition, error)
	LastPrice(symbol string) (decimal.Decimal, error)
	CancelAllOrder(symbol string) error
}

type ITradeCalculator interface {
	CalcLimitOrderPrice(price, limitDepth decimal.Decimal, side Side) decimal.Decimal
}
