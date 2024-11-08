package calculator

import (
	"github.com/shopspring/decimal"
	"mm-tradebot/internal/model"
)

func New(
	maker decimal.Decimal,
	taker decimal.Decimal,
) *TradeCalculator {
	return &TradeCalculator{
		maker: maker,
		taker: taker,
	}
}

type TradeCalculator struct {
	maker decimal.Decimal
	taker decimal.Decimal
}

func (c *TradeCalculator) CalcLimitOrderPrice(
	price, limitDepth decimal.Decimal,
	side model.Side,
) decimal.Decimal {
	var limitPrice decimal.Decimal
	if side == model.BUY {
		limitPrice = price.Mul(decimal.NewFromInt(1).Add(limitDepth.Div(decimal.NewFromInt(100))))
	} else {
		limitPrice = price.Mul(decimal.NewFromInt(1).Sub(limitDepth.Div(decimal.NewFromInt(100))))
	}
	return limitPrice
}
