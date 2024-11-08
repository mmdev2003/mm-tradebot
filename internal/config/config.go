package config

import "github.com/shopspring/decimal"

func New() *Config {
	return &Config{
		Maker:   decimal.NewFromInt(0.001),
		Taker:   decimal.NewFromInt(0.002),
		MaxLoss: decimal.NewFromInt(-1),
	}
}

type Config struct {
	Maker decimal.Decimal
	Taker decimal.Decimal

	ApiKey    string
	ApiSecret string

	MaxLoss decimal.Decimal
}
