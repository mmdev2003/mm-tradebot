package config

import "github.com/shopspring/decimal"

func New() *Config {
	return &Config{
		Maker:     decimal.NewFromFloat(0.001),
		Taker:     decimal.NewFromFloat(0.002),
		MaxLoss:   decimal.NewFromInt(-1),
		ApiKey:    "ZBzJ4KOUSnS1kYAuF8",
		ApiSecret: "JyWYCUhnX2XzA6wVTXYoHo5VsDAsMVz7cIc0",
	}
}

type Config struct {
	Maker decimal.Decimal
	Taker decimal.Decimal

	ApiKey    string
	ApiSecret string

	TimeToCancelLimitOrder int
	MaxLoss                decimal.Decimal
}
