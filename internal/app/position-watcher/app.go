package position_watcher

import (
	"encoding/json"
	"github.com/shopspring/decimal"
	Bybit "github.com/wuhewuhe/bybit.go.api"
	"mm-tradebot/internal/model"
	"mm-tradebot/internal/model/api"
	"sync"
)

func New(
	mu *sync.Mutex,
	positionService model.IPositionService,
	accountService model.IAccountService,
) {
	ws := Bybit.NewBybitPrivateWebSocket(
		"wss://stream.bybit.com/v5/private",
		"YOUR_API_KEY",
		"YOUR_API_SECRET",
		PositionHandler(mu, positionService, accountService),
	)

	_ = ws.Connect([]string{"position"})
	select {}
}

func PositionHandler(
	mu *sync.Mutex,
	positionService model.IPositionService,
	accountService model.IAccountService,
) func(message string) error {
	return func(message string) error {
		mu.Lock()
		defer mu.Unlock()

		var Message api.StreamPositionMessage
		err := json.Unmarshal([]byte(message), &Message)
		if err != nil {
			return err
		}
		positionActual := Message.Data[0]

		positionDB := positionService.Position()
		if positionDB == nil {
			return nil
		}

		actualOpenPrice, err := decimal.NewFromString(positionActual.EntryPrice)
		if err != nil {
			return err
		}

		if positionActual.TakeProfit == "0" && positionDB.Status == model.Limit {

		}
		return nil
	}
}
