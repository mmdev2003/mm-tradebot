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
	position *model.Position
}

func (positionRepo *RepositoryPosition) OpenLimitOrder(
	symbol string,
	side model.Side,
	status model.Status,
	size decimal.Decimal,
	limitOrderPrice decimal.Decimal,
) {
	timeNow := time.Now()
	positionRepo.position.LimitOrder = &model.LimitOrder{
		Size:     size,
		Price:    limitOrderPrice,
		OpenTime: timeNow,
	}
	positionRepo.position.Side = side
	positionRepo.position.Status = status
	positionRepo.position.Symbol = symbol
	positionRepo.position.OpenTime = timeNow
}

func (positionRepo *RepositoryPosition) ReopenLimitOrder(
	status model.Status,
	size decimal.Decimal,
	price decimal.Decimal,
) {
	positionRepo.position.LimitOrder.Price = price
	positionRepo.position.LimitOrder.Size = size
	positionRepo.position.Status = status
}

func (positionRepo *RepositoryPosition) CancelLimitOrder() {
	if positionRepo.position.Status == model.Limit {
		positionRepo.position = &model.Position{}
	}

	if positionRepo.position.Status == model.ActiveLimit {
		positionRepo.position.Status = model.Active
	}
}

func (positionRepo *RepositoryPosition) Position() *model.Position {
	return positionRepo.position
}
