package position

import (
	"github.com/labstack/echo/v4"
	"log/slog"
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"sync"
)

func Control(
	mu *sync.Mutex,
	cfg *config.Config,
	positionService model.IPositionService,

) echo.HandlerFunc {
	type OpenPositionBody struct {
		Symbol string     `json:"Symbol"`
		Side   model.Side `json:"Side"`
	}
	return func(request echo.Context) error {
		mu.Lock()
		defer mu.Unlock()

		var body OpenPositionBody
		if err := request.Bind(&body); err != nil {
			slog.Error(err.Error())
			return request.JSON(422, err)
		}

		if err := request.Validate(&body); err != nil {
			slog.Error(err.Error())
			return request.JSON(422, err)
		}

		//if greater := decimal.Max(account.TotalProfitInPercent, cfg.MaxLoss); greater == cfg.MaxLoss {
		//	return request.JSON(200, "Максимальная просадка, давай думать")
		//}

		positionDB := positionService.Position()

		if positionDB.Status == "" {
			err := positionService.OpenLimitOrder(
				body.Symbol,
				body.Side,
				model.Limit,
				cfg.Size,
				cfg.LimitDepth,
				cfg.Leverage,
			)
			if err != nil {
				slog.Error(err.Error())
				return request.JSON(500, err)
			}
		}

		if positionDB.Status != "" {
			return request.JSON(200, "Позиция уже открыта, ну его нафиг что-то делать с этим")
		}

		return nil
	}
}
