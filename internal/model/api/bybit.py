from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class _Coin:
    availableToBorrow: str
    bonus: str
    accruedInterest: str
    availableToWithdraw: str
    totalOrderIM: str
    equity: str
    totalPositionMM: str
    usdValue: str
    spotHedgingQty: str
    unrealisedPnl: str
    collateralSwitch: bool
    borrowAmount: str
    totalPositionIM: str
    walletBalance: str
    cumRealisedPnl: str
    locked: str
    marginCollateral: bool
    coin: str


@dataclass
class BybitWallet:
    totalEquity: str
    accountIMRate: str
    totalMarginBalance: str
    totalInitialMargin: str
    accountType: str
    totalAvailableBalance: str
    accountMMRate: str
    totalPerpUPL: str
    totalWalletBalance: str
    accountLTV: str
    totalMaintenanceMargin: str
    coin: List[_Coin] = field(default_factory=list)


@dataclass
class WalletResponse:
    @dataclass
    class Result:
        list: List[BybitWallet] = field(default_factory=list)

    retCode: int
    retMsg: str
    result: Result
    retExtInfo: dict
    time: int


@dataclass
class BybitPosition:
    positionIdx: int
    riskId: int
    riskLimitValue: str
    symbol: str
    side: str
    size: str
    avgPrice: str
    positionValue: str
    tradeMode: int
    positionStatus: str
    autoAddMargin: int
    adlRankIndicator: int
    leverage: str
    positionBalance: str
    markPrice: str
    liqPrice: str
    bustPrice: str
    positionMM: str
    positionIM: str
    tpslMode: str
    takeProfit: str
    stopLoss: str
    trailingStop: str
    unrealisedPnl: str
    curRealisedPnl: str
    cumRealisedPnl: str
    seq: int
    isReduceOnly: bool
    mmrSysUpdateTime: str
    leverageSysUpdatedTime: str
    sessionAvgPrice: str
    createdTime: str
    updatedTime: str


@dataclass
class PositionResponse:
    @dataclass
    class Result:
        list: List[BybitPosition]
        nextPageCursor: str
        category: str

    retCode: int
    retMsg: str
    result: Result
    retExtInfo: dict
    time: int
