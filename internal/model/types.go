package model

type Status string

const (
	Limit       Status = "limit"
	Active      Status = "active"
	ActiveLimit Status = "activeLimit"
	Closed      Status = "closed"
)

type Side string

const (
	BUY  Side = "BUY"
	SELL Side = "SELL"
)
