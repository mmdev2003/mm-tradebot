package api

type BybitCoinWallet struct {
	AvailableToBorrow   string `json:"availableToBorrow"`
	Bonus               string `json:"bonus"`
	AccruedInterest     string `json:"accruedInterest"`
	AvailableToWithdraw string `json:"availableToWithdraw"`
	TotalOrderIM        string `json:"totalOrderIM"`
	Equity              string `json:"equity"`
	TotalPositionMM     string `json:"totalPositionMM"`
	UsdValue            string `json:"usdValue"`
	SpotHedgingQty      string `json:"spotHedgingQty"`
	UnrealisedPnl       string `json:"unrealisedPnl"`
	CollateralSwitch    bool   `json:"collateralSwitch"`
	BorrowAmount        string `json:"borrowAmount"`
	TotalPositionIM     string `json:"totalPositionIM"`
	WalletBalance       string `json:"walletBalance"`
	CumRealisedPnl      string `json:"cumRealisedPnl"`
	Locked              string `json:"locked"`
	MarginCollateral    bool   `json:"marginCollateral"`
	Coin                string `json:"coin"`
}

type BybitWallet struct {
	TotalEquity            string `json:"totalEquity"`
	AccountIMRate          string `json:"accountIMRate"`
	TotalMarginBalance     string `json:"totalMarginBalance"`
	TotalInitialMargin     string `json:"totalInitialMargin"`
	AccountType            string `json:"accountType"`
	TotalAvailableBalance  string `json:"totalAvailableBalance"`
	AccountMMRate          string `json:"accountMMRate"`
	TotalPerpUPL           string `json:"totalPerpUPL"`
	TotalWalletBalance     string `json:"totalWalletBalance"`
	AccountLTV             string `json:"accountLTV"`
	TotalMaintenanceMargin string `json:"totalMaintenanceMargin"`
}

type BybitWalletResponse struct {
	RetCode int    `json:"retCode"`
	RetMsg  string `json:"retMsg"`
	Result  struct {
		List []struct {
			BybitWallet
			Coin []BybitCoinWallet `json:"coin"`
		} `json:"list"`
	} `json:"result"`
	RetExtInfo struct {
	} `json:"retExtInfo"`
	Time int64 `json:"time"`
}

type BybitPosition struct {
	PositionIdx            int    `json:"positionIdx"`
	RiskId                 int    `json:"riskId"`
	RiskLimitValue         string `json:"riskLimitValue"`
	Symbol                 string `json:"symbol"`
	Side                   string `json:"side"`
	Size                   string `json:"size"`
	AvgPrice               string `json:"avgPrice"`
	PositionValue          string `json:"positionValue"`
	TradeMode              int    `json:"tradeMode"`
	PositionStatus         string `json:"positionStatus"`
	AutoAddMargin          int    `json:"autoAddMargin"`
	AdlRankIndicator       int    `json:"adlRankIndicator"`
	Leverage               string `json:"leverage"`
	PositionBalance        string `json:"positionBalance"`
	MarkPrice              string `json:"markPrice"`
	LiqPrice               string `json:"liqPrice"`
	BustPrice              string `json:"bustPrice"`
	PositionMM             string `json:"positionMM"`
	PositionIM             string `json:"positionIM"`
	TpslMode               string `json:"tpslMode"`
	TakeProfit             string `json:"takeProfit"`
	StopLoss               string `json:"stopLoss"`
	TrailingStop           string `json:"trailingStop"`
	UnrealisedPnl          string `json:"unrealisedPnl"`
	CurRealisedPnl         string `json:"curRealisedPnl"`
	CumRealisedPnl         string `json:"cumRealisedPnl"`
	Seq                    int64  `json:"seq"`
	IsReduceOnly           bool   `json:"isReduceOnly"`
	MmrSysUpdateTime       string `json:"mmrSysUpdateTime"`
	LeverageSysUpdatedTime string `json:"leverageSysUpdatedTime"`
	SessionAvgPrice        string `json:"sessionAvgPrice"`
	CreatedTime            string `json:"createdTime"`
	UpdatedTime            string `json:"updatedTime"`
}

type BybitPositionResponse struct {
	RetCode int    `json:"retCode"`
	RetMsg  string `json:"retMsg"`
	Result  struct {
		List           []BybitPosition `json:"list"`
		NextPageCursor string          `json:"nextPageCursor"`
		Category       string          `json:"category"`
	} `json:"result"`
	RetExtInfo struct {
	} `json:"retExtInfo"`
	Time int64 `json:"time"`
}

type BybitTicker struct {
	Symbol                 string `json:"symbol"`
	LastPrice              string `json:"lastPrice"`
	IndexPrice             string `json:"indexPrice"`
	MarkPrice              string `json:"markPrice"`
	PrevPrice24H           string `json:"prevPrice24h"`
	Price24HPcnt           string `json:"price24hPcnt"`
	HighPrice24H           string `json:"highPrice24h"`
	LowPrice24H            string `json:"lowPrice24h"`
	PrevPrice1H            string `json:"prevPrice1h"`
	OpenInterest           string `json:"openInterest"`
	OpenInterestValue      string `json:"openInterestValue"`
	Turnover24H            string `json:"turnover24h"`
	Volume24H              string `json:"volume24h"`
	FundingRate            string `json:"fundingRate"`
	NextFundingTime        string `json:"nextFundingTime"`
	PredictedDeliveryPrice string `json:"predictedDeliveryPrice"`
	BasisRate              string `json:"basisRate"`
	DeliveryFeeRate        string `json:"deliveryFeeRate"`
	DeliveryTime           string `json:"deliveryTime"`
	Ask1Size               string `json:"ask1Size"`
	Bid1Price              string `json:"bid1Price"`
	Ask1Price              string `json:"ask1Price"`
	Bid1Size               string `json:"bid1Size"`
	Basis                  string `json:"basis"`
}

type TickersResponse struct {
	RetCode int    `json:"retCode"`
	RetMsg  string `json:"retMsg"`
	Result  struct {
		Category string        `json:"category"`
		List     []BybitTicker `json:"list"`
	} `json:"result"`
	RetExtInfo struct {
	} `json:"retExtInfo"`
	Time int64 `json:"time"`
}

type StreamPositionMessage struct {
	Id           string `json:"id"`
	Topic        string `json:"topic"`
	CreationTime int64  `json:"creationTime"`
	Data         []struct {
		PositionIdx            int    `json:"positionIdx"`
		TradeMode              int    `json:"tradeMode"`
		RiskId                 int    `json:"riskId"`
		RiskLimitValue         string `json:"riskLimitValue"`
		Symbol                 string `json:"symbol"`
		Side                   string `json:"side"`
		Size                   string `json:"size"`
		EntryPrice             string `json:"entryPrice"`
		Leverage               string `json:"leverage"`
		PositionValue          string `json:"positionValue"`
		PositionBalance        string `json:"positionBalance"`
		MarkPrice              string `json:"markPrice"`
		PositionIM             string `json:"positionIM"`
		PositionMM             string `json:"positionMM"`
		TakeProfit             string `json:"takeProfit"`
		StopLoss               string `json:"stopLoss"`
		TrailingStop           string `json:"trailingStop"`
		UnrealisedPnl          string `json:"unrealisedPnl"`
		CurRealisedPnl         string `json:"curRealisedPnl"`
		CumRealisedPnl         string `json:"cumRealisedPnl"`
		SessionAvgPrice        string `json:"sessionAvgPrice"`
		CreatedTime            string `json:"createdTime"`
		UpdatedTime            string `json:"updatedTime"`
		TpslMode               string `json:"tpslMode"`
		LiqPrice               string `json:"liqPrice"`
		BustPrice              string `json:"bustPrice"`
		Category               string `json:"category"`
		PositionStatus         string `json:"positionStatus"`
		AdlRankIndicator       int    `json:"adlRankIndicator"`
		AutoAddMargin          int    `json:"autoAddMargin"`
		LeverageSysUpdatedTime string `json:"leverageSysUpdatedTime"`
		MmrSysUpdatedTime      string `json:"mmrSysUpdatedTime"`
		Seq                    int64  `json:"seq"`
		IsReduceOnly           bool   `json:"isReduceOnly"`
	} `json:"data"`
}
