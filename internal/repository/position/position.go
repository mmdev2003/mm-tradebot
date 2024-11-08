package position

import (
	"github.com/shopspring/decimal"
	"mm-tradebot/internal/model"
	"time"
)

func New() *RepositoryPosition {
	return &RepositoryPosition{}
}

type RepositoryPosition struct {
	positions map[string]*model.Position
}

func (positionRepo *RepositoryPosition) OpenLimitOrder(
	symbol string,
	side model.Side,
	status model.Status,
	size decimal.Decimal,
	limitOrderPrice decimal.Decimal,
) {
	positionRepo.positions[symbol].LimitOrder = &model.LimitOrder{
		Size:      size,
		Price:     limitOrderPrice,
		CreatedAt: time.Now(),
	}
	positionRepo.positions[symbol].Side = side
	positionRepo.positions[symbol].Status = status
}

func (positionRepo *RepositoryPosition) ReopenLimitOrder(
	symbol string,
	status model.Status,
	size decimal.Decimal,
	price decimal.Decimal,
) {
	positionRepo.positions[symbol].LimitOrder.Price = price
	positionRepo.positions[symbol].LimitOrder.Size = size
	positionRepo.positions[symbol].Status = status
}

func (positionRepo *RepositoryPosition) Position(symbol string) *model.Position {
	return positionRepo.positions[symbol]
}
