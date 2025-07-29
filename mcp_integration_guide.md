# MCP Integration Guide
## Yahoo Finance + TA-Lib Technical Analysis Workflow

This guide shows how to effectively combine both MCP servers for comprehensive S&P 500 technical analysis.

---

## Quick Start Workflow

### 1. Start Both MCP Servers
```bash
# Terminal 1 - Yahoo Finance MCP
python yfinance_mcp_server.py

# Terminal 2 - TA-Lib MCP  
python talib_mcp_server.py
```

### 2. Basic Analysis Pattern
```
Step 1: Fetch data using Yahoo Finance MCP
Step 2: Extract OHLCV arrays from the data
Step 3: Calculate indicators using TA-Lib MCP
Step 4: Interpret signals and generate insights
```

---

## Data Flow Examples

### Example 1: Simple Moving Average Analysis
```
# Step 1: Get S&P 500 data
get_stock_history(symbol="^GSPC", period="6mo", interval="1d")

# Step 2: Extract close prices from response
close_prices = [100.50, 101.25, 99.80, 102.15, ...]

# Step 3: Calculate moving averages
simple_moving_average(prices=close_prices, timeperiod=20)
simple_moving_average(prices=close_prices, timeperiod=50)
simple_moving_average(prices=close_prices, timeperiod=200)

# Step 4: Compare current price vs moving averages for trend analysis
```

### Example 2: Complete OHLC Analysis
```
# Step 1: Get comprehensive S&P 500 data
market_data = get_stock_history(symbol="^GSPC", period="1y", interval="1d")

# Step 2: Extract OHLC arrays
open_prices = market_data["data"]["open"]
high_prices = market_data["data"]["high"] 
low_prices = market_data["data"]["low"]
close_prices = market_data["data"]["close"]
volume = market_data["data"]["volume"]

# Step 3: Calculate multiple indicators
rsi_result = relative_strength_index(prices=close_prices, timeperiod=14)
macd_result = macd(prices=close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
bb_result = bollinger_bands(prices=close_prices, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
atr_result = average_true_range(high_prices=high_prices, low_prices=low_prices, close_prices=close_prices, timeperiod=14)

# Step 4: Generate comprehensive market analysis
```

---

## Common Data Extraction Patterns

### Pattern 1: Basic Price Data
```python
# After getting stock history
data = get_stock_history("^GSPC", period="3mo")
closes = data["data"]["close"]
dates = data["data"]["dates"]
```

### Pattern 2: OHLC + Volume
```python
# Full OHLCV extraction
market_data = get_stock_history("^GSPC", period="6mo")
ohlcv = {
    "open": market_data["data"]["open"],
    "high": market_data["data"]["high"], 
    "low": market_data["data"]["low"],
    "close": market_data["data"]["close"],
    "volume": market_data["data"]["volume"],
    "dates": market_data["data"]["dates"]
}
```

### Pattern 3: Multi-Symbol Analysis
```python
# Get multiple symbols
symbols = ["^GSPC", "SPY", "QQQ", "IWM"]
multi_data = download_market_data(symbols=symbols, period="1mo")

# Extract data for each symbol
for symbol in symbols:
    closes = multi_data["data"][symbol]["close"]
    # Calculate indicators for each symbol
    rsi = relative_strength_index(prices=closes, timeperiod=14)
```

---

## Indicator Combination Strategies

### Strategy 1: Trend Confirmation
```
1. Get S&P 500 data: get_stock_history("^GSPC", period="1y")
2. Calculate trend indicators:
   - simple_moving_average(closes, timeperiod=50)
   - exponential_moving_average(closes, timeperiod=21)
   - average_directional_index(highs, lows, closes, timeperiod=14)
3. Confirm trend: Price > MA, ADX > 25
```

### Strategy 2: Momentum Oscillator Suite
```
1. Get data: get_stock_history("^GSPC", period="6mo")
2. Calculate momentum indicators:
   - relative_strength_index(closes, timeperiod=14)
   - stochastic_oscillator(highs, lows, closes)
   - williams_percent_r(highs, lows, closes, timeperiod=14)
   - commodity_channel_index(highs, lows, closes, timeperiod=20)
3. Look for overbought/oversold confluence
```

### Strategy 3: Volatility Breakout
```
1. Get data: get_stock_history("^GSPC", period="1y")
2. Calculate volatility indicators:
   - bollinger_bands(closes, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
   - average_true_range(highs, lows, closes, timeperiod=14)
   - standard_deviation(closes, timeperiod=20)
3. Identify squeeze and expansion patterns
```

### Strategy 4: Volume Confirmation
```
1. Get data with volume: get_stock_history("^GSPC", period="6mo")
2. Calculate volume indicators:
   - on_balance_volume(closes, volume)
   - money_flow_index(highs, lows, closes, volume, timeperiod=14)
   - accumulation_distribution_line(highs, lows, closes, volume)
3. Confirm price moves with volume analysis
```

---

## Advanced Integration Patterns

### Pattern 1: Multi-Timeframe Analysis
```python
# Get different timeframes
yearly_data = get_stock_history("^GSPC", period="1y", interval="1d")
monthly_data = get_stock_history("^GSPC", period="3mo", interval="1d") 
weekly_data = get_stock_history("^GSPC", period="1mo", interval="1d")

# Calculate same indicators on different timeframes
yearly_rsi = relative_strength_index(yearly_data["data"]["close"], 14)
monthly_rsi = relative_strength_index(monthly_data["data"]["close"], 14)
weekly_rsi = relative_strength_index(weekly_data["data"]["close"], 14)

# Look for timeframe confluence
```

### Pattern 2: Sector Rotation Analysis
```python
# Get sector ETFs
sectors = ["XLK", "XLF", "XLV", "XLE", "XLY", "XLI", "XLP", "XLU", "XLRE"]
sector_data = download_market_data(symbols=sectors, period="6mo")

# Calculate relative strength for each sector
spx_data = get_stock_history("^GSPC", period="6mo")
spx_closes = spx_data["data"]["close"]

for sector in sectors:
    sector_closes = sector_data["data"][sector]["close"]
    # Calculate sector vs SPX relative strength
    sector_roc = rate_of_change(sector_closes, timeperiod=20)
    spx_roc = rate_of_change(spx_closes, timeperiod=20)
    # Compare ROC values for relative strength
```

### Pattern 3: Market Regime Detection
```python
# Get long-term data
long_data = get_stock_history("^GSPC", period="2y", interval="1d")
closes = long_data["data"]["close"]
highs = long_data["data"]["high"]
lows = long_data["data"]["low"]

# Calculate regime indicators
adx = average_directional_index(highs, lows, closes, timeperiod=14)
atr = average_true_range(highs, lows, closes, timeperiod=20)
rsi = relative_strength_index(closes, timeperiod=14)

# Classify regime based on indicator levels
# Trending: ADX > 25, Ranging: ADX < 20
# High Vol: ATR > 80th percentile, Low Vol: ATR < 20th percentile
```

---

## Error Handling Best Practices

### 1. Data Validation
```python
# Always check for errors in API responses
data = get_stock_history("^GSPC", period="1mo")
if "error" in data:
    print(f"Error fetching data: {data['error']}")
    return

# Check for sufficient data points
if len(data["data"]["close"]) < 50:
    print("Insufficient data for analysis")
    return
```

### 2. Indicator Validation
```python
# Check indicator results
rsi = relative_strength_index(closes, timeperiod=14)
if not rsi or len(rsi) == 0:
    print("RSI calculation failed")
    return

# Handle NaN values (common in early periods)
valid_rsi = [x for x in rsi if x is not None and not math.isnan(x)]
```

### 3. Data Alignment
```python
# Ensure data arrays are same length
min_length = min(len(closes), len(highs), len(lows))
aligned_closes = closes[:min_length]
aligned_highs = highs[:min_length]
aligned_lows = lows[:min_length]
```

---

## Performance Optimization Tips

### 1. Batch Operations
```python
# Instead of multiple single calls
rsi = relative_strength_index(closes, 14)
macd_result = macd(closes, 12, 26, 9)
bb = bollinger_bands(closes, 20, 2.0, 2.0)

# Consider combining related calculations
```

### 2. Data Caching
```python
# Cache frequently used data
cached_spx_data = get_stock_history("^GSPC", period="1y")
# Reuse for multiple indicator calculations
```

### 3. Selective Updates
```python
# Only fetch new data when needed
last_date = cached_data["data"]["dates"][-1]
if is_market_day() and last_date < today():
    # Fetch incremental update
    new_data = get_stock_history("^GSPC", period="5d")
```

---

## Production Checklist

- [ ] Both MCP servers are running and responsive
- [ ] Data validation checks in place
- [ ] Error handling for API failures
- [ ] Sufficient historical data for indicators
- [ ] Proper data type conversion (string dates to datetime)
- [ ] NaN/null value handling
- [ ] Data alignment across different time series
- [ ] Performance monitoring for large datasets
- [ ] Logging for debugging and audit trails
- [ ] Backup data sources if primary fails

This integration guide provides the foundation for building robust, professional-grade technical analysis systems using both MCP servers.