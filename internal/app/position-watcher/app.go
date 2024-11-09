package position_watcher

import (
	"encoding/json"
	"fmt"
	"github.com/shopspring/decimal"
	Bybit "github.com/wuhewuhe/bybit.go.api"
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"mm-tradebot/internal/model/api"
	"strings"
	"sync"
)

func Start(
	mu *sync.Mutex,
	cfg *config.Config,
	positionService model.IPositionService,
) {
	ws := Bybit.NewBybitPrivateWebSocket(
		"wss://stream.bybit.com/v5/private",
		cfg.ApiKey,
		cfg.ApiSecret,
		PositionHandler(mu, cfg, positionService),
	)

	_ = ws.Connect([]string{"position"})
	select {}
}

func PositionHandler(
	mu *sync.Mutex,
	cfg *config.Config,
	positionService model.IPositionService,
) func(message string) error {
	return func(message string) error {
		mu.Lock()
		defer mu.Unlock()
		fmt.Println(message)
		if strings.Contains(message, "conn_id") {
			return nil
		}

		var Message api.StreamPositionMessage
		err := json.Unmarshal([]byte(message), &Message)
		if err != nil {
			return err
		}

		positionDB := positionService.Position()
		if positionDB == nil {
			return nil
		}

		positionActual := Message.Data[0]
		openPriceActual, err := decimal.NewFromString(positionActual.EntryPrice)
		if err != nil {
			return err
		}

		if positionActual.TakeProfit == "0" && positionDB.Status == model.Limit {
			err = positionService.OpenPosition(
				positionDB.Symbol,
				positionDB.Side,
				openPriceActual,
				positionDB.LimitOrder.Price,
				positionDB.LimitOrder.Size,
				cfg.TakeInPercent,
			)
			if err != nil {
				return err
			}
		}

		if positionActual.Size == "0" && positionDB.Status != model.Limit {
			err = positionService.ClosePosition(positionDB.Symbol)
			if err != nil {
				return err
			}
		}
		return nil
	}
}
