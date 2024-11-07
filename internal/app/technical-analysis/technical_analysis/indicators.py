import sys
sys.path.append('/root/mm-tradebot')
import pandas_ta as ta
from src.services import utils
import numpy as np
import pandas as pd

time_frames = { 
    "5m": 5,
    "15m": 15,
    "1h": 60,
    "2h": 120,
    "4h": 240
}

def get_trend_ADX(kline):
    close = kline['close']
    high = kline['high']
    low = kline['low']
    
    adx = ta.adx(high, low, close, lenght=21)
    atr = ta.atr(high, low, close)
    plus_di = 100 * (adx.iloc[:, 1] / atr)
    minus_di = 100 * (adx.iloc[:, 2] / atr)
      
    trend_ADX = 'Flat'
    if adx.iloc[-1, 0] > 20:
        if plus_di.iloc[-1] > minus_di.iloc[-1]:
            trend_ADX = 'Buy'
        if plus_di.iloc[-1] < minus_di.iloc[-1]:
            trend_ADX = 'Sell'
    
     
    return trend_ADX
    

def get_trend_AD(kline):
    
    close = kline['close']
    high = kline['high']
    low = kline['low']
    volume = kline['volume']
    ad = ta.ad(high, low, close, volume)
    
    price_direction = pd.Series(np.sign(close.diff().fillna(0)))
    ad_direction = pd.Series(np.sign(ad.diff().fillna(0)))
        
    if price_direction[:-10].sum() > 5 and ad_direction[:-10].sum() > 5:
        trend_AD = 'Buy'
    elif price_direction[:-10].sum() > 5 and  ad_direction[:-10].sum() > 5:
        trend_AD = 'Sell'
    else:
        trend_AD = 'Flat'
        
    divergence_AD = utils.get_divergence(high, low, close, ad)
            
    return trend_AD, divergence_AD
    

def get_trend_MACD(kline):

    close = kline['close']
    high = kline['high']
    low = kline['low']
    
    macd_df = ta.macd(close)
    macd = macd_df.iloc[:, 0]
    signal = macd_df.iloc[:, 2]
    
    if macd.iloc[-1] > signal.iloc[-1]:
        trend_MACD = 'Buy'
    
    elif macd.iloc[-1] < signal.iloc[-1]:
        trend_MACD = 'Sell'
    else:
        trend_MACD = 'Flat'
    
    divergence_MACD = utils.get_divergence(high, low, close, macd)
    
    return trend_MACD, divergence_MACD



def get_signal_OBV(kline):
    
    close = kline['close']
    high = kline['high']
    low = kline['low']
    volume = kline['volume']
    obv = ta.obv(close, volume)
    
    divergence_OBV = utils.get_divergence(high, low, close, obv)
   
    price_change = high.pct_change(periods=15)
    obv_change = obv.pct_change(periods=5)
    
    signal_OBV = 'No signal'
    if price_change.iloc[-1] > 2 and obv_change > 1:
        signal_OBV = 'Buy'
    if price_change.iloc[-1] < -2 and obv_change > 1:
        signal_OBV = 'Sell'
    
    return divergence_OBV, signal_OBV


def get_signal_KVO(kline):
    
    close = kline['close']
    high = kline['high']
    low = kline['low']
    volume = kline['volume']
    
    kvo_df = ta.kvo(high, low, close, volume)
    kvo = kvo_df.iloc[:, 0]
    signal = kvo_df.iloc[:, 1]
    
    crossing_up, crossing_down = utils.crossing_threshold(kvo, 0)
    
    signal_KVO = 'No signal'
    if crossing_down:
        if crossing_down[-1] == len(high) - 1:
            signal_KVO = 'Buy'
       
    if crossing_up:
        if crossing_up[-1] == len(high) - 1:
            signal_KVO = 'Sell'
    
    
    divergence_KVO = utils.get_divergence(high, low, close, kvo)
    
    return signal_KVO, divergence_KVO


def get_trend_RSI(kline):
   
    close = kline['close']
    high = kline['high']
    low = kline['low']
    signal_RSI = 'No signal'
    
    rsi = ta.rsi(close)
    
    if rsi.iloc[-1] < 50:
        trend_RSI = 'Buy'
    if rsi.iloc[-1] > 50:
        trend_RSI = 'Buy'
   
    _, crossing_down_70 = utils.crossing_threshold(rsi, 70)
    if crossing_down_70:
        if crossing_down_70[-1] == len(rsi) - 1:
            signal_RSI = 'Sell'
       
    crossing_up_30, _ = utils.crossing_threshold(rsi, 30)
    if crossing_up_30:
        if crossing_up_30[-1] == len(rsi) - 1:
            signal_RSI = 'Buy'
       
       
    divergence_RSI = utils.get_divergence(high, low, close, rsi)
    
    
    return trend_RSI, divergence_RSI, signal_RSI


def get_signal_STOCH(kline):
    
    close = kline['close']
    high = kline['high']
    low = kline['low']
    stoch = ta.stoch(high, low, close)
    stoch_k = stoch.iloc[:, 0]
    stoch_d = stoch.iloc[:, 1]
    
    signal_STOCH = 'No signal'
    _, crossing_down_80 = utils.crossing_threshold(stoch_k, 80)
    if crossing_down_80[-1] == len(high) - 1:
        signal_STOCH = 'Sell'
    
    crossing_up_20, _ = utils.crossing_threshold(stoch_k, 20)
    if crossing_up_20[-1] == len(high) - 1:
        signal_STOCH = 'Buy'
        
    divergence_STOCH = utils.get_divergence(high, low, close, stoch_k)
    
    crossing_up, _ = utils.crossing_threshold(stoch_k, stoch_d.iloc[-1])
    _, crossing_down = utils.crossing_threshold(stoch_k, stoch_d.iloc[-1])
    if crossing_down:
        if crossing_down[-1] == len(high) - 1:
            signal_STOCH = 'Sell'
    
    if crossing_up:
        if crossing_up[-1] == len(high) - 1:
            signal_STOCH = 'Buy'
    
    return signal_STOCH, divergence_STOCH

def get_signal_SUN(kline, len_stoch, smooth_k, smooth_d, len_rsi, len_change, len_up_and_down, len_ma_rsi, max_rsi, min_rsi, max_sun, min_sun):
    
    close = kline['close']
    rsi = ta.rsi(close, len_rsi)
    stoch = ta.stoch(rsi, rsi, rsi, smooth_k=smooth_k,  d=smooth_d, k=len_stoch)
    stoch_k = stoch.iloc[:, 0]
    stoch_d = stoch.iloc[:, 1]
   
    
    change = close.pct_change(periods=len_change)
    
    max_change = change.apply(lambda percent: percent if percent > 0 else 0)
    min_change = change.apply(lambda percent: abs(percent) if percent < 0 else 0)
    
    up = ta.ema(max_change, len_up_and_down)
    down = ta.ema(min_change, len_up_and_down)
    
    rsi = pd.Series(np.where(down == 0, 100, np.where(up == 0, 0, 100 - (100 / (1 + up / down)))))
    sma_rsi = ta.sma(rsi, len_ma_rsi)
    
    sun = (stoch_k.iloc[0] + sma_rsi.iloc[-1]) / 2
    
    stoch_d = stoch_d.iloc[0]
    stoch_k = stoch_k.iloc[0]
    
    signal_SUN = 'No signal'
    if (stoch_d > stoch_k) and (stoch_k <= min_r) and (sun <= min_sun):
        signal_SUN = 'Buy'
    if (stoch_d < stoch_k) and (stoch_k >= max_r) and (sun >= max_sun):
        signal_SUN = 'Sell'
    
    return signal_SUN