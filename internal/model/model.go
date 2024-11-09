package model

import (
	"github.com/shopspring/decimal"
	"time"
)

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
	Leverage   decimal.Decimal

	OpenPrice decimal.Decimal
	AvgPrice  decimal.Decimal

	TakeInPercent decimal.Decimal
	StopInPercent decimal.Decimal

	CommissionInDollar decimal.Decimal
	OpenTime           time.Time
	UpdateTime         time.Time
	CloseTime          time.Time
}
