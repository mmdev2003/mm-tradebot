package bybit

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/shopspring/decimal"
	Bybit "github.com/wuhewuhe/bybit.go.api"
	"mm-tradebot/internal/model"
	"mm-tradebot/internal/model/api"
)

func New(apiKey, apiSecret string) *ClientBybit {
	httpClient := Bybit.NewBybitHttpClient(apiKey, apiSecret)
	return &ClientBybit{
		httpClient: httpClient,
	}
}

type ClientBybit struct {
	httpClient *Bybit.Client
	apiKey     string
	apiSecret  string
}

func (c *ClientBybit) Balance() decimal.Decimal {
	params := map[string]any{
		"accountType": "UNIFIED",
		"coin":        "USDT",
	}
	wallet, err := c.httpClient.NewUtaBybitServiceWithParams(params).GetAccountWallet(context.Background())
	if err != nil {
		panic(err)
	}
	fmt.Println(Bybit.PrettyPrint(wallet))

	rawBytes, err := json.Marshal(wallet)
	if err != nil {
		panic(err)
	}

	var walletBySymbolResponse api.BybitWalletResponse
	err = json.Unmarshal(rawBytes, &walletBySymbolResponse)
	if err != nil {
		panic(err)
	}

	balance, err := decimal.NewFromString(walletBySymbolResponse.Result.List[0].Coin[0].WalletBalance)
	if err != nil {
		panic(err)
	}

	return balance
}

func (c *ClientBybit) PositionBySymbol(symbol string) (*api.BybitPosition, error) {
	params := map[string]any{
		"category": "linear",
		"symbol":   symbol,
	}
	position, err := c.httpClient.NewUtaBybitServiceWithParams(params).GetPositionList(context.Background())
	if err != nil {
		return nil, err
	}

	rawBytes, err := json.Marshal(position)
	if err != nil {
		return nil, err
	}

	var positionBySymbolResponse api.BybitPositionResponse
	err = json.Unmarshal(rawBytes, &positionBySymbolResponse)
	if err != nil {
		return nil, err
	}

	return &positionBySymbolResponse.Result.List[0], nil
}

func (c *ClientBybit) LastPrice(symbol string) (decimal.Decimal, error) {
	params := map[string]any{
		"symbol":   symbol,
		"category": "linear",
	}
	ticker, err := c.httpClient.NewUtaBybitServiceWithParams(params).GetMarketTickers(context.Background())
	if err != nil {
		return decimal.Zero, err
	}

	rawBytes, err := json.Marshal(ticker)
	if err != nil {
		return decimal.Zero, err
	}

	var tickerResponse api.TickersResponse
	err = json.Unmarshal(rawBytes, &tickerResponse)
	if err != nil {
		return decimal.Zero, err
	}

	lastPrice, err := decimal.NewFromString(tickerResponse.Result.List[0].LastPrice)
	if err != nil {
		return decimal.Zero, err
	}

	return lastPrice, nil
}

func (c *ClientBybit) CancelAllOrder(symbol string) error {
	params := map[string]any{
		"symbol":   symbol,
		"category": "linear",
	}
	response, err := c.httpClient.NewUtaBybitServiceWithParams(params).CancelOrder(context.Background())
	if err != nil {
		return err
	}
	fmt.Println(Bybit.PrettyPrint(response))

	return nil
}

func (c *ClientBybit) SetTakeProfit(
	symbol string,
	takePrice decimal.Decimal,
) error {
	params := map[string]any{
		"symbol":     symbol,
		"category":   "linear",
		"takeProfit": takePrice.String(),
	}
	response, err := c.httpClient.NewUtaBybitServiceWithParams(params).SetPositionTradingStop(context.Background())
	if err != nil {
		return err
	}
	fmt.Println(Bybit.PrettyPrint(response))

	return nil
}

func (c *ClientBybit) SetStopLoss(
	symbol string,
	stopPrice decimal.Decimal,
) error {
	params := map[string]any{
		"symbol":   symbol,
		"category": "linear",
		"stopLoss": stopPrice.String(),
	}
	response, err := c.httpClient.NewUtaBybitServiceWithParams(params).SetPositionTradingStop(context.Background())
	if err != nil {
		return err
	}

	fmt.Println(Bybit.PrettyPrint(response))
	return nil
}

func (c *ClientBybit) SetLeverage(
	symbol string,
	leverage decimal.Decimal,
) error {
	params := map[string]any{
		"symbol":       symbol,
		"category":     "linear",
		"buyLeverage":  leverage.String(),
		"sellLeverage": leverage.String(),
	}
	response, err := c.httpClient.NewUtaBybitServiceWithParams(params).SetPositionLeverage(context.Background())
	if err != nil {
		return err
	}

	fmt.Println(Bybit.PrettyPrint(response))
	return nil
}

func (c *ClientBybit) OpenLimitOrder(
	symbol string,
	side model.Side,
	price decimal.Decimal,
	size decimal.Decimal,
	leverage decimal.Decimal,
) error {
	_ = c.SetLeverage(symbol, leverage)

	params := map[string]any{
		"symbol":    symbol,
		"category":  "linear",
		"orderType": "Limit",
		"side":      side,
		"price":     price.String(),
		"qty":       size.String(),
	}
	response, err := c.httpClient.NewUtaBybitServiceWithParams(params).PlaceOrder(context.Background())
	if err != nil {
		return err
	}

	fmt.Println(Bybit.PrettyPrint(response))
	return nil
}
