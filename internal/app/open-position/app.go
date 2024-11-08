package open_position

import (
	"github.com/labstack/echo/v4"
	"mm-tradebot/internal/config"
	"mm-tradebot/internal/model"
	"sync"
)

import (
	. "mm-tradebot/internal/api/http/position"
)

var PREFIX = "/api/position"

func Start(
	mu *sync.Mutex,
	cfg *config.Config,
	accountService model.IAccountService,
	positionService model.IPositionService,
) {
	server := echo.New()
	server.POST(PREFIX+"/control", Control(mu, cfg, accountService, positionService))
	server.Logger.Fatal(server.Start(":8001"))
}
