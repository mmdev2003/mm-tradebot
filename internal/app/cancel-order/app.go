package cancel_order

import (
	"log/slog"
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"sync"
	"time"
)

func Start(
	mu *sync.Mutex,
	cfg *config.Config,
	positionService model.IPositionService,
) {
	for {
		mu.Lock()
		position := positionService.Position()
		status := position.Status

		if status == model.Limit || status == model.ActiveLimit {
			cancelTime := positionService.CalcCancelTime(
				position.LimitOrder.OpenTime,
				cfg.TimeToCancelLimitOrder,
			)
			if cancelTime.Before(time.Now()) {
				err := positionService.CancelLimitOrder(position.Symbol)
				if err != nil {
					slog.Error(err.Error())
				}
			}
		}
		mu.Unlock()

		time.Sleep(time.Second * 20)
	}
}
