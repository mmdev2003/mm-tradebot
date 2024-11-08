package model

import (
	"github.com/shopspring/decimal"
	"time"
)

type Account struct {
	Balance              decimal.Decimal
	StartBalance         decimal.Decimal
	TotalProfitInPercent decimal.Decimal
	TotalProfitInDollars decimal.Decimal
	CountProfitPositions int
	CountLossPositions   int
	CountActivePositions int
	CountClosedPositions int
}

type LimitOrder struct {
	Size     decimal.Decimal
	Price    decimal.Decimal
	OpenTime time.Time
}

type Position struct {
	Symbol     string
	Status     Status
	Side       Side
	LimitOrder *LimitOrder
	Size       decimal.Decimal
	AvgPrice   decimal.Decimal
	Leverage   decimal.Decimal

	OpenTime   time.Time
	UpdateTime time.Time
	CloseTime  time.Time
}
