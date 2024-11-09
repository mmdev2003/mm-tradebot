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

func (c *TradeCalculator) CalcCommission(
	commissionInPercent, price, size decimal.Decimal,
) decimal.Decimal {
	commissionInDollar := price.Mul(size.Mul(commissionInPercent.Div(decimal.NewFromInt(100))))
	return commissionInDollar
}

func (c *TradeCalculator) CalcTakePrice(
	price decimal.Decimal,
	side model.Side,
	size decimal.Decimal,
	commissionInDollar decimal.Decimal,
	commissionInPercent decimal.Decimal,
	takeInPercent decimal.Decimal,
) decimal.Decimal {
	var takePrice decimal.Decimal
	if side == model.BUY {
		positionSum := commissionInDollar.Add(price.Mul(size))
		takeInPart := decimal.NewFromInt(1).Add(takeInPercent.Div(decimal.NewFromInt(100)))
		commissionInPart := decimal.NewFromInt(1).Add(commissionInPercent.Div(decimal.NewFromInt(100)))
		takePrice = commissionInPart.Mul(takeInPart.Mul(positionSum.Div(size)))
	} else {
		positionSum := commissionInDollar.Sub(price.Mul(size))
		takeInPart := decimal.NewFromInt(1).Sub(takeInPercent.Div(decimal.NewFromInt(100)))
		commissionInPart := decimal.NewFromInt(1).Sub(commissionInPercent.Div(decimal.NewFromInt(100)))
		takePrice = commissionInPart.Mul(takeInPart.Mul(positionSum.Div(size)))
	}
	return takePrice
}
