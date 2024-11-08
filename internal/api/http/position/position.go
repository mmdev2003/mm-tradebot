package position

import (
	"github.com/labstack/echo/v4"
	"github.com/shopspring/decimal"
	"log/slog"
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"sync"
)

func Control(
	mu *sync.Mutex,
	cfg *config.Config,
	accountService model.IAccountService,
	positionService model.IPositionService,

) echo.HandlerFunc {
	type OpenPositionBody struct {
		Symbol     string          `json:"Symbol"`
		Side       model.Side      `json:"Side"`
		Size       decimal.Decimal `json:"Size"`
		LimitDepth decimal.Decimal `json:"LimitDepth"`
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

		account := accountService.Account()

		if greater := decimal.Max(account.TotalProfitInPercent, cfg.MaxLoss); greater == cfg.MaxLoss {
			return request.JSON(200, "Максимальная просадка, давай думать")
		}

		positionDB := positionService.Position(body.Symbol)

		if positionDB.Status == "" {
			err := positionService.OpenLimitOrder(
				body.Symbol,
				body.Side,
				model.Limit,
				body.Size,
				body.LimitDepth,
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
