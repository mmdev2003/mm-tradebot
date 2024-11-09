package config

import "github.com/shopspring/decimal"

func New() *Config {
	return &Config{
		Maker: decimal.NewFromFloat(0.001),
		Taker: decimal.NewFromFloat(0.002),

		ApiKey:    "ZBzJ4KOUSnS1kYAuF8",
		ApiSecret: "JyWYCUhnX2XzA6wVTXYoHo5VsDAsMVz7cIc0",

		SecondsToCancelLimitOrder: 30,
		SecondsToSetStop:          30,
		Leverage:                  decimal.NewFromInt(3),
		MaxLoss:                   decimal.NewFromInt(-1),
	}
}

type Config struct {
	Maker decimal.Decimal
	Taker decimal.Decimal

	ApiKey    string
	ApiSecret string

	SecondsToCancelLimitOrder int
	SecondsToSetStop          int
	Leverage                  decimal.Decimal
	MaxLoss                   decimal.Decimal
	Size                      decimal.Decimal
	LimitDepth                decimal.Decimal

	TakeInPercent decimal.Decimal
	StopInPercent decimal.Decimal
}
