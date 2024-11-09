package set_stop

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

		setTime := position.OpenTime.Add(time.Duration(cfg.SecondsToSetStop) * time.Second)

		if setTime.Before(time.Now()) {
			err := positionService.SetStop(
				position.Symbol,
				position.AvgPrice,
				position.Size,
				position.Side,
				position.CommissionInDollar,
				cfg.StopInPercent,
			)
			if err != nil {
				slog.Error(err.Error())
			}
		}
		mu.Unlock()
		time.Sleep(20 * time.Second)
	}
}
