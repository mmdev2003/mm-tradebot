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
	takeInPercent decimal.Decimal,
) decimal.Decimal {
	var takePrice decimal.Decimal
	if side == model.BUY {
		positionSum := price.Mul(size)
		takeInPart := takeInPercent.Div(decimal.NewFromInt(100))
		potentialProfitInDollar := positionSum.Mul(takeInPart)
		neededPrice := positionSum.Add(potentialProfitInDollar.Add(commissionInDollar))
		takePrice = neededPrice.Mul(size)
	} else {
		positionSum := price.Mul(size)
		takeInPart := takeInPercent.Div(decimal.NewFromInt(100))
		potentialProfitInDollar := positionSum.Mul(takeInPart)
		neededPrice := positionSum.Sub(potentialProfitInDollar.Sub(commissionInDollar))
		takePrice = neededPrice.Mul(size)
	}
	return takePrice
}

func (c *TradeCalculator) CalcStopPrice(
	price decimal.Decimal,
	side model.Side,
	size decimal.Decimal,
	commissionInDollar decimal.Decimal,
	stopInPercent decimal.Decimal,
) decimal.Decimal {
	var stopPrice decimal.Decimal
	if side == model.BUY {
		positionSum := price.Mul(size)
		stopInPart := stopInPercent.Div(decimal.NewFromInt(100))
		potentialLossInDollar := positionSum.Mul(stopInPart)
		neededPrice := positionSum.Sub(potentialLossInDollar.Sub(commissionInDollar))
		stopPrice = neededPrice.Mul(size)
	} else {
		positionSum := price.Mul(size)
		stopInPart := stopInPercent.Div(decimal.NewFromInt(100))
		potentialLossInDollar := positionSum.Mul(stopInPart)
		neededPrice := positionSum.Add(potentialLossInDollar.Add(commissionInDollar))
		stopPrice = neededPrice.Mul(size)
	}
	return stopPrice
}
