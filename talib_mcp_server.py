#!/usr/bin/env python3
"""
TA-Lib MCP Server
Provides technical analysis indicators through Model Context Protocol
"""

import numpy as np
import talib
from typing import List, Optional, Union, Dict, Any
from fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("TA-Lib Technical Analysis")

@mcp.tool
def simple_moving_average(
    prices: List[float],
    timeperiod: int = 30
) -> List[float]:
    """
    Calculate Simple Moving Average (SMA)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods for the moving average (default: 30)
    
    Returns:
        List of SMA values
    """
    try:
        if len(prices) < timeperiod:
            raise ValueError(f"Need at least {timeperiod} price points for SMA calculation")
        
        close = np.array(prices, dtype=np.float64)
        result = talib.SMA(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating SMA: {e}")
        raise

@mcp.tool
def exponential_moving_average(
    prices: List[float],
    timeperiod: int = 30
) -> List[float]:
    """
    Calculate Exponential Moving Average (EMA)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods for the moving average (default: 30)
    
    Returns:
        List of EMA values
    """
    close = np.array(prices, dtype=np.float64)
    result = talib.EMA(close, timeperiod=timeperiod)
    return result.tolist()

@mcp.tool
def bollinger_bands(
    prices: List[float],
    timeperiod: int = 5,
    nbdevup: float = 2.0,
    nbdevdn: float = 2.0,
    matype: int = 0
) -> Dict[str, List[float]]:
    """
    Calculate Bollinger Bands
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 5)
        nbdevup: Number of standard deviations for upper band (default: 2.0)
        nbdevdn: Number of standard deviations for lower band (default: 2.0)
        matype: Moving average type (default: 0 for SMA)
    
    Returns:
        Dictionary with 'upper', 'middle', and 'lower' band values
    """
    close = np.array(prices, dtype=np.float64)
    upper, middle, lower = talib.BBANDS(close, timeperiod=timeperiod, 
                                       nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
    return {
        'upper': upper.tolist(),
        'middle': middle.tolist(),
        'lower': lower.tolist()
    }

@mcp.tool
def relative_strength_index(
    prices: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods for RSI calculation (default: 14)
    
    Returns:
        List of RSI values
    """
    close = np.array(prices, dtype=np.float64)
    result = talib.RSI(close, timeperiod=timeperiod)
    return result.tolist()

@mcp.tool
def macd(
    prices: List[float],
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9
) -> Dict[str, List[float]]:
    """
    Calculate MACD (Moving Average Convergence/Divergence)
    
    Args:
        prices: List of price values
        fastperiod: Fast EMA period (default: 12)
        slowperiod: Slow EMA period (default: 26)
        signalperiod: Signal line EMA period (default: 9)
    
    Returns:
        Dictionary with 'macd', 'signal', and 'histogram' values
    """
    close = np.array(prices, dtype=np.float64)
    macd_line, signal_line, histogram = talib.MACD(close, fastperiod=fastperiod,
                                                  slowperiod=slowperiod, signalperiod=signalperiod)
    return {
        'macd': macd_line.tolist(),
        'signal': signal_line.tolist(),
        'histogram': histogram.tolist()
    }

@mcp.tool
def stochastic_oscillator(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    fastk_period: int = 5,
    slowk_period: int = 3,
    slowk_matype: int = 0,
    slowd_period: int = 3,
    slowd_matype: int = 0
) -> Dict[str, List[float]]:
    """
    Calculate Stochastic Oscillator
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        fastk_period: Fast %K period (default: 5)
        slowk_period: Slow %K period (default: 3)
        slowk_matype: Slow %K moving average type (default: 0)
        slowd_period: Slow %D period (default: 3)
        slowd_matype: Slow %D moving average type (default: 0)
    
    Returns:
        Dictionary with 'slowk' and 'slowd' values
    """
    high = np.array(high_prices, dtype=np.float64)
    low = np.array(low_prices, dtype=np.float64)
    close = np.array(close_prices, dtype=np.float64)
    
    slowk, slowd = talib.STOCH(high, low, close, 
                              fastk_period=fastk_period,
                              slowk_period=slowk_period,
                              slowk_matype=slowk_matype,
                              slowd_period=slowd_period,
                              slowd_matype=slowd_matype)
    return {
        'slowk': slowk.tolist(),
        'slowd': slowd.tolist()
    }

@mcp.tool
def average_true_range(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Average True Range (ATR)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        timeperiod: Number of periods (default: 14)
    
    Returns:
        List of ATR values
    """
    high = np.array(high_prices, dtype=np.float64)
    low = np.array(low_prices, dtype=np.float64)
    close = np.array(close_prices, dtype=np.float64)
    
    result = talib.ATR(high, low, close, timeperiod=timeperiod)
    return result.tolist()

@mcp.tool
def on_balance_volume(
    close_prices: List[float],
    volume: List[float]
) -> List[float]:
    """
    Calculate On Balance Volume (OBV)
    
    Args:
        close_prices: List of close price values
        volume: List of volume values
    
    Returns:
        List of OBV values
    """
    close = np.array(close_prices, dtype=np.float64)
    vol = np.array(volume, dtype=np.float64)
    
    result = talib.OBV(close, vol)
    return result.tolist()

@mcp.tool
def commodity_channel_index(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Commodity Channel Index (CCI)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        timeperiod: Number of periods (default: 14)
    
    Returns:
        List of CCI values
    """
    high = np.array(high_prices, dtype=np.float64)
    low = np.array(low_prices, dtype=np.float64)
    close = np.array(close_prices, dtype=np.float64)
    
    result = talib.CCI(high, low, close, timeperiod=timeperiod)
    return result.tolist()

@mcp.tool
def williams_percent_r(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Williams' %R
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        timeperiod: Number of periods (default: 14)
    
    Returns:
        List of Williams' %R values
    """
    high = np.array(high_prices, dtype=np.float64)
    low = np.array(low_prices, dtype=np.float64)
    close = np.array(close_prices, dtype=np.float64)
    
    result = talib.WILLR(high, low, close, timeperiod=timeperiod)
    return result.tolist()

@mcp.tool
def stochastic_rsi(
    prices: List[float],
    timeperiod: int = 14,
    fastk_period: int = 5,
    fastd_period: int = 3,
    fastd_matype: int = 0
) -> Dict[str, List[float]]:
    """
    Calculate Stochastic RSI
    
    Args:
        prices: List of price values
        timeperiod: RSI time period (default: 14)
        fastk_period: Fast %K period (default: 5)
        fastd_period: Fast %D period (default: 3)
        fastd_matype: Fast %D moving average type (default: 0)
    
    Returns:
        Dictionary with 'fastk' and 'fastd' values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        fastk, fastd = talib.STOCHRSI(close, timeperiod=timeperiod,
                                     fastk_period=fastk_period,
                                     fastd_period=fastd_period,
                                     fastd_matype=fastd_matype)
        return {
            'fastk': fastk.tolist(),
            'fastd': fastd.tolist()
        }
    except Exception as e:
        logging.error(f"Error calculating Stochastic RSI: {e}")
        raise

@mcp.tool
def momentum(
    prices: List[float],
    timeperiod: int = 10
) -> List[float]:
    """
    Calculate Momentum
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 10)
    
    Returns:
        List of momentum values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.MOM(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating Momentum: {e}")
        raise

@mcp.tool
def average_directional_index(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Average Directional Index (ADX)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        timeperiod: Number of periods (default: 14)
    
    Returns:
        List of ADX values
    """
    try:
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.ADX(high, low, close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating ADX: {e}")
        raise

@mcp.tool
def double_exponential_moving_average(
    prices: List[float],
    timeperiod: int = 30
) -> List[float]:
    """
    Calculate Double Exponential Moving Average (DEMA)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 30)
    
    Returns:
        List of DEMA values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.DEMA(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating DEMA: {e}")
        raise

@mcp.tool
def triple_exponential_moving_average(
    prices: List[float],
    timeperiod: int = 30
) -> List[float]:
    """
    Calculate Triple Exponential Moving Average (TEMA)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 30)
    
    Returns:
        List of TEMA values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.TEMA(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating TEMA: {e}")
        raise

@mcp.tool
def kaufman_adaptive_moving_average(
    prices: List[float],
    timeperiod: int = 30
) -> List[float]:
    """
    Calculate Kaufman's Adaptive Moving Average (KAMA)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 30)
    
    Returns:
        List of KAMA values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.KAMA(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating KAMA: {e}")
        raise

@mcp.tool
def normalized_average_true_range(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Normalized Average True Range (NATR)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        timeperiod: Number of periods (default: 14)
    
    Returns:
        List of NATR values
    """
    try:
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.NATR(high, low, close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating NATR: {e}")
        raise

@mcp.tool
def standard_deviation(
    prices: List[float],
    timeperiod: int = 5,
    nbdev: float = 1.0
) -> List[float]:
    """
    Calculate Standard Deviation
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 5)
        nbdev: Number of deviations (default: 1.0)
    
    Returns:
        List of standard deviation values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.STDDEV(close, timeperiod=timeperiod, nbdev=nbdev)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating Standard Deviation: {e}")
        raise

@mcp.tool
def accumulation_distribution_line(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    volume: List[float]
) -> List[float]:
    """
    Calculate Accumulation/Distribution Line (AD)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        volume: List of volume values
    
    Returns:
        List of AD values
    """
    try:
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        vol = np.array(volume, dtype=np.float64)
        
        result = talib.AD(high, low, close, vol)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating AD: {e}")
        raise

@mcp.tool
def chaikin_ad_oscillator(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    volume: List[float],
    fastperiod: int = 3,
    slowperiod: int = 10
) -> List[float]:
    """
    Calculate Chaikin A/D Oscillator (ADOSC)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        volume: List of volume values
        fastperiod: Fast period (default: 3)
        slowperiod: Slow period (default: 10)
    
    Returns:
        List of ADOSC values
    """
    try:
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        vol = np.array(volume, dtype=np.float64)
        
        result = talib.ADOSC(high, low, close, vol, fastperiod=fastperiod, slowperiod=slowperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating ADOSC: {e}")
        raise

@mcp.tool
def money_flow_index(
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    volume: List[float],
    timeperiod: int = 14
) -> List[float]:
    """
    Calculate Money Flow Index (MFI)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        volume: List of volume values
        timeperiod: Number of periods (default: 14)
    
    Returns:
        List of MFI values
    """
    try:
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        vol = np.array(volume, dtype=np.float64)
        
        result = talib.MFI(high, low, close, vol, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating MFI: {e}")
        raise

@mcp.tool
def doji_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float]
) -> List[int]:
    """
    Detect Doji candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLDOJI(open_p, high, low, close)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Doji pattern: {e}")
        raise

@mcp.tool
def engulfing_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float]
) -> List[int]:
    """
    Detect Engulfing candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLENGULFING(open_p, high, low, close)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Engulfing pattern: {e}")
        raise

@mcp.tool
def hammer_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float]
) -> List[int]:
    """
    Detect Hammer candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLHAMMER(open_p, high, low, close)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Hammer pattern: {e}")
        raise

@mcp.tool
def shooting_star_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float]
) -> List[int]:
    """
    Detect Shooting Star candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLSHOOTINGSTAR(open_p, high, low, close)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Shooting Star pattern: {e}")
        raise

@mcp.tool
def morning_star_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    penetration: float = 0.3
) -> List[int]:
    """
    Detect Morning Star candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        penetration: Penetration factor (default: 0.3)
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLMORNINGSTAR(open_p, high, low, close, penetration=penetration)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Morning Star pattern: {e}")
        raise

@mcp.tool
def evening_star_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    penetration: float = 0.3
) -> List[int]:
    """
    Detect Evening Star candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
        penetration: Penetration factor (default: 0.3)
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLEVENINGSTAR(open_p, high, low, close, penetration=penetration)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Evening Star pattern: {e}")
        raise

@mcp.tool
def harami_pattern(
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float]
) -> List[int]:
    """
    Detect Harami candlestick pattern
    
    Args:
        open_prices: List of open price values
        high_prices: List of high price values
        low_prices: List of low price values
        close_prices: List of close price values
    
    Returns:
        List of pattern signals (0=no pattern, 100=bullish, -100=bearish)
    """
    try:
        open_p = np.array(open_prices, dtype=np.float64)
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        close = np.array(close_prices, dtype=np.float64)
        
        result = talib.CDLHARAMI(open_p, high, low, close)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error detecting Harami pattern: {e}")
        raise

@mcp.tool
def parabolic_sar(
    high_prices: List[float],
    low_prices: List[float],
    acceleration: float = 0.02,
    maximum: float = 0.2
) -> List[float]:
    """
    Calculate Parabolic Stop and Reverse (SAR)
    
    Args:
        high_prices: List of high price values
        low_prices: List of low price values
        acceleration: Acceleration factor (default: 0.02)
        maximum: Maximum acceleration factor (default: 0.2)
    
    Returns:
        List of SAR values
    """
    try:
        high = np.array(high_prices, dtype=np.float64)
        low = np.array(low_prices, dtype=np.float64)
        
        result = talib.SAR(high, low, acceleration=acceleration, maximum=maximum)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating SAR: {e}")
        raise

@mcp.tool
def rate_of_change(
    prices: List[float],
    timeperiod: int = 10
) -> List[float]:
    """
    Calculate Rate of Change (ROC)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 10)
    
    Returns:
        List of ROC values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.ROC(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating ROC: {e}")
        raise

@mcp.tool
def percentage_price_oscillator(
    prices: List[float],
    fastperiod: int = 12,
    slowperiod: int = 26,
    matype: int = 0
) -> List[float]:
    """
    Calculate Percentage Price Oscillator (PPO)
    
    Args:
        prices: List of price values
        fastperiod: Fast EMA period (default: 12)
        slowperiod: Slow EMA period (default: 26)
        matype: Moving average type (default: 0)
    
    Returns:
        List of PPO values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.PPO(close, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating PPO: {e}")
        raise

@mcp.tool
def trix(
    prices: List[float],
    timeperiod: int = 30
) -> List[float]:
    """
    Calculate TRIX (Triple Smoothed Exponential Moving Average)
    
    Args:
        prices: List of price values
        timeperiod: Number of periods (default: 30)
    
    Returns:
        List of TRIX values
    """
    try:
        close = np.array(prices, dtype=np.float64)
        result = talib.TRIX(close, timeperiod=timeperiod)
        return result.tolist()
    except Exception as e:
        logging.error(f"Error calculating TRIX: {e}")
        raise

if __name__ == "__main__":
    mcp.run()