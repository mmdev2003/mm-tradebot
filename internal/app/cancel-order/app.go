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
		if position == nil {
			mu.Unlock()
			time.Sleep(20 * time.Second)
			continue
		}
		status := position.Status

		if status == model.Limit || status == model.ActiveLimit {
			cancelTime := position.LimitOrder.OpenTime.Add(time.Duration(cfg.SecondsToCancelLimitOrder) * time.Second)

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
