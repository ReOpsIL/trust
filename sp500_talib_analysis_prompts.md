# S&P 500 Technical Analysis Prompts
## Using Yahoo Finance + TA-Lib MCP Servers

This document contains comprehensive prompts for performing technical analysis on S&P 500 data using the Yahoo Finance MCP server to fetch data and the TA-Lib MCP server to calculate indicators.

---

## 1. Basic Moving Average Analysis

```
Analyze the S&P 500 (^GSPC) using moving averages:

1. Get 6 months of daily S&P 500 data using get_stock_history
2. Calculate these moving averages using the TA-Lib MCP:
   - 20-day Simple Moving Average (SMA)
   - 50-day Simple Moving Average (SMA) 
   - 200-day Simple Moving Average (SMA)
   - 20-day Exponential Moving Average (EMA)

3. Analyze the current trend by comparing:
   - Current price vs all moving averages
   - 20-day vs 50-day MA crossover signals
   - 50-day vs 200-day MA (golden/death cross)

4. Provide a summary of the trend strength and direction
```

---

## 2. Momentum Oscillator Analysis

```
Perform momentum analysis on the S&P 500 (^GSPC):

1. Fetch 3 months of S&P 500 daily data
2. Calculate these momentum indicators:
   - RSI (14-period) - identify overbought/oversold levels
   - MACD (12,26,9) - trend and momentum changes
   - Stochastic Oscillator (14,3,3) - short-term momentum
   - Williams %R (14-period) - momentum confirmation

3. Current market assessment:
   - Is the market overbought (RSI > 70) or oversold (RSI < 30)?
   - MACD signal line crossovers and histogram direction
   - Stochastic %K and %D levels and crossovers
   - Williams %R momentum signals

4. Provide trading signals based on momentum convergence/divergence
```

---

## 3. Volatility Breakout Strategy

```
Analyze S&P 500 volatility and potential breakouts:

1. Get 6 months of S&P 500 (^GSPC) daily OHLC data
2. Calculate volatility indicators:
   - Bollinger Bands (20-period, 2 std dev)
   - Average True Range (ATR, 14-period)
   - Standard Deviation (20-period)

3. Identify potential breakout conditions:
   - Current price position relative to Bollinger Bands
   - Band squeeze conditions (low volatility)
   - ATR expansion indicating increased volatility
   - Price approaching upper/lower Bollinger Band

4. Generate volatility-based trading signals and risk levels
```

---

## 4. Multi-Timeframe Trend Analysis

```
Perform multi-timeframe analysis of S&P 500 trend strength:

1. Fetch S&P 500 data for different timeframes:
   - 1 year of daily data for long-term trend
   - 3 months of daily data for medium-term trend
   - 1 month of daily data for short-term trend

2. Calculate trend indicators for each timeframe:
   - ADX (14-period) for trend strength
   - DEMA and TEMA (20-period) for trend direction
   - KAMA (30-period) for adaptive trend following

3. Trend analysis:
   - Long-term trend direction and strength (ADX > 25)
   - Medium-term trend alignment with long-term
   - Short-term trend for entry timing
   - Adaptive moving average signals

4. Provide multi-timeframe trend confluence assessment
```

---

## 5. Volume-Price Analysis

```
Analyze S&P 500 price-volume relationships:

1. Get 6 months of S&P 500 (^GSPC) data with volume
2. Calculate volume indicators:
   - On-Balance Volume (OBV)
   - Accumulation/Distribution Line (AD)
   - Chaikin A/D Oscillator (ADOSC)
   - Money Flow Index (MFI, 14-period)

3. Volume analysis:
   - OBV trend vs price trend (confirm or diverge)
   - A/D line accumulation or distribution phases
   - MFI overbought/oversold levels (>80/<20)
   - Volume flow changes via Chaikin Oscillator

4. Identify volume-price divergences and confirmation signals
```

---

## 6. Support/Resistance with Parabolic SAR

```
Identify S&P 500 support/resistance levels and trend changes:

1. Fetch 1 year of S&P 500 daily OHLC data
2. Calculate support/resistance indicators:
   - Parabolic SAR for dynamic support/resistance
   - Simple Moving Averages (50, 100, 200) as key levels
   - Bollinger Bands for dynamic support/resistance zones

3. Level analysis:
   - Current SAR level and trend direction
   - Distance from key moving average support/resistance
   - Price action near Bollinger Band levels
   - Historical support/resistance level tests

4. Generate stop-loss levels and trend reversal signals
```

---

## 7. Comprehensive Market Timing Strategy

```
Create a comprehensive S&P 500 market timing analysis:

1. Get 1 year of S&P 500 (^GSPC) daily OHLC data
2. Calculate a full suite of indicators:
   
   Trend: SMA(20,50,200), EMA(12,26), ADX(14)
   Momentum: RSI(14), MACD(12,26,9), Stochastic(14,3,3)
   Volatility: Bollinger Bands(20,2), ATR(14)
   Volume: OBV, MFI(14)
   Other: Parabolic SAR, ROC(10), TRIX(30)

3. Multi-factor analysis:
   - Trend strength and direction consensus
   - Momentum overbought/oversold levels
   - Volatility expansion/contraction cycles
   - Volume confirmation of price moves
   - Mean reversion vs trend continuation signals

4. Generate overall market outlook: BULLISH/BEARISH/NEUTRAL with confidence level
5. Provide specific entry/exit signals and risk management levels
```

---

## 8. Sector Rotation Analysis

```
Analyze S&P 500 sectors for rotation opportunities:

1. Get 6 months of data for major sector ETFs:
   - Technology (XLK)
   - Financial (XLF) 
   - Healthcare (XLV)
   - Energy (XLE)
   - Consumer Discretionary (XLY)

2. For each sector, calculate:
   - Relative Strength vs S&P 500 using ROC(20)
   - RSI(14) for momentum
   - MACD(12,26,9) for trend changes
   - Money Flow Index for institutional flow

3. Sector analysis:
   - Rank sectors by relative strength
   - Identify momentum shifts (RSI crossovers)
   - MACD trend confirmations
   - Money flow analysis for sector rotation

4. Recommend sector allocation based on technical confluence
```

---

## 9. Risk-Adjusted Position Sizing

```
Calculate risk-adjusted position sizing for S&P 500 trading:

1. Get 3 months of S&P 500 daily OHLC data
2. Calculate risk metrics:
   - Average True Range (ATR, 14-period) for volatility
   - Standard Deviation (20-period) for price dispersion
   - Bollinger Band width for volatility measurement

3. Position sizing calculation:
   - Use ATR for stop-loss distance (2x ATR)
   - Calculate position size based on 1-2% account risk
   - Volatility-adjusted position sizing
   - Dynamic stop-loss levels using Parabolic SAR

4. Provide specific position sizing recommendations with risk metrics
```

---

## 10. Market Regime Detection

```
Detect current S&P 500 market regime:

1. Get 2 years of S&P 500 daily data for regime analysis
2. Calculate regime indicators:
   - ADX(14) for trend strength vs ranging
   - ATR(20) percentile for volatility regime
   - RSI(14) distribution for momentum regime
   - VIX-like analysis using price volatility

3. Regime classification:
   - Trending vs Ranging market (ADX levels)
   - Low vs High volatility environment
   - Bull vs Bear market momentum
   - Mean reversion vs Momentum regime

4. Strategy recommendations based on detected regime:
   - Trending regime: Use trend-following indicators
   - Ranging regime: Use mean-reversion indicators
   - High volatility: Reduce position sizes
   - Low volatility: Prepare for breakout strategies
```

---

## Usage Instructions

### Setup
1. Start both MCP servers:
   ```bash
   python yfinance_mcp_server.py &
   python talib_mcp_server.py &
   ```

2. Use these prompts in your MCP client to perform comprehensive technical analysis

### Data Flow
1. **Yahoo Finance MCP** → Fetch S&P 500 OHLC data
2. **TA-Lib MCP** → Calculate technical indicators on the data
3. **Analysis** → Interpret signals and generate trading insights

### Key Symbols
- **S&P 500 Index**: `^GSPC`
- **S&P 500 ETF**: `SPY`
- **Major Sector ETFs**: `XLK`, `XLF`, `XLV`, `XLE`, `XLY`, etc.

### Customization
- Adjust timeframes based on trading style (day/swing/position)
- Modify indicator parameters for different market conditions
- Combine multiple prompts for comprehensive analysis
- Add risk management rules specific to your strategy

These prompts provide a complete framework for professional-grade S&P 500 technical analysis using both MCP servers.