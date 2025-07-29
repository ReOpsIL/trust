# Financial Analysis MCP Servers

![Alt text](trust.png "Trust")


A comprehensive suite of Model Context Protocol (MCP) servers that provide technical analysis and market data capabilities for financial analysis and trading applications.

## Components

### 1. TA-Lib MCP Server (`talib_mcp_server.py`)
Technical Analysis Library server providing 31 professional-grade indicators through FastMCP.

### 2. Yahoo Finance MCP Server (`yfinance_mcp_server.py`)
Market data server providing real-time and historical stock data through Yahoo Finance API.

## TA-Lib MCP Server Features

### Momentum Indicators (7)
- **RSI** (Relative Strength Index): `relative_strength_index()`
- **MACD** (Moving Average Convergence Divergence): `macd()`
- **STOCH** (Stochastic Oscillator): `stochastic_oscillator()`
- **STOCHRSI** (Stochastic RSI): `stochastic_rsi()`
- **MOM** (Momentum): `momentum()`
- **CCI** (Commodity Channel Index): `commodity_channel_index()`
- **WILLR** (Williams %R): `williams_percent_r()`

### Trend Indicators (6)
- **ADX** (Average Directional Index): `average_directional_index()`
- **EMA** (Exponential Moving Average): `exponential_moving_average()`
- **SMA** (Simple Moving Average): `simple_moving_average()`
- **DEMA** (Double Exponential Moving Average): `double_exponential_moving_average()`
- **TEMA** (Triple Exponential Moving Average): `triple_exponential_moving_average()`
- **KAMA** (Kaufman's Adaptive Moving Average): `kaufman_adaptive_moving_average()`

### Volatility Indicators (4)
- **BBANDS** (Bollinger Bands): `bollinger_bands()`
- **ATR** (Average True Range): `average_true_range()`
- **NATR** (Normalized Average True Range): `normalized_average_true_range()`
- **STDDEV** (Standard Deviation): `standard_deviation()`

### Volume Indicators (4)
- **OBV** (On-Balance Volume): `on_balance_volume()`
- **AD** (Accumulation/Distribution Line): `accumulation_distribution_line()`
- **ADOSC** (Chaikin A/D Oscillator): `chaikin_ad_oscillator()`
- **MFI** (Money Flow Index): `money_flow_index()`

### Candlestick Pattern Indicators (7)
- **CDLDOJI** (Doji): `doji_pattern()`
- **CDLENGULFING** (Engulfing): `engulfing_pattern()`
- **CDLHAMMER** (Hammer): `hammer_pattern()`
- **CDLSHOOTINGSTAR** (Shooting Star): `shooting_star_pattern()`
- **CDLMORNINGSTAR** (Morning Star): `morning_star_pattern()`
- **CDLEVENINGSTAR** (Evening Star): `evening_star_pattern()`
- **CDLHARAMI** (Harami): `harami_pattern()`

### Other Technical Indicators (4)
- **SAR** (Parabolic Stop and Reverse): `parabolic_sar()`
- **ROC** (Rate of Change): `rate_of_change()`
- **PPO** (Percentage Price Oscillator): `percentage_price_oscillator()`
- **TRIX** (Triple Smoothed Exponential Moving Average): `trix()`

## Yahoo Finance MCP Server Features

### Market Data Functions (9)
- **Historical Data**: `get_stock_history()` - OHLCV data with flexible periods/intervals
- **Stock Information**: `get_stock_info()` - Comprehensive company and market data
- **Multiple Quotes**: `get_multiple_quotes()` - Current quotes for multiple symbols
- **Bulk Downloads**: `download_market_data()` - Multi-threaded data retrieval
- **Financial Statements**: `get_financials()` - Income, balance sheet, cash flow data
- **Dividends & Splits**: `get_dividends_and_splits()` - Corporate action history
- **Analyst Recommendations**: `get_recommendations()` - Professional analyst ratings
- **Symbol Search**: `search_symbols()` - Company and ticker symbol lookup
- **Earnings Calendar**: `get_earnings_calendar()` - Upcoming earnings dates

## Installation

### Prerequisites

1. **TA-Lib System Library** (for technical analysis):
   ```bash
   # macOS
   brew install ta-lib
   
   # Ubuntu/Debian
   sudo apt-get install libta-lib-dev
   
   # Windows (using conda)
   conda install -c conda-forge ta-lib
   ```

### Python Dependencies

2. **TA-Lib Server Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - `fastmcp>=0.1.0`
   - `TA-Lib>=0.4.25`
   - `numpy>=1.21.0`

3. **Yahoo Finance Server Dependencies**:
   ```bash
   pip install -r yfinance_requirements.txt
   ```
   - `fastmcp>=0.1.0`
   - `yfinance>=0.2.18`
   - `pandas>=1.3.0`
   - `requests>=2.25.0`

## Usage

### Running the Servers

**TA-Lib Technical Analysis Server:**
```bash
python talib_mcp_server.py
```

**Yahoo Finance Market Data Server:**
```bash
python yfinance_mcp_server.py
```

Both servers run on STDIO transport by default, suitable for MCP clients.

### Testing

Verify server functionality with test scripts:

```bash
# Test TA-Lib indicators
python test_talib_mcp.py

# Test Yahoo Finance data retrieval
python test_yfinance_mcp.py
```

## Example Usage

### Technical Analysis with TA-Lib

```python
# Simple Moving Average
prices = [100.0, 101.5, 99.8, 102.1, 103.5, ...]
sma_20 = simple_moving_average(prices, timeperiod=20)

# Bollinger Bands
bb_result = bollinger_bands(prices, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
# Returns: {'upper': [...], 'middle': [...], 'lower': [...]}

# RSI Momentum Indicator
rsi_values = relative_strength_index(prices, timeperiod=14)

# MACD Analysis
macd_result = macd(prices, fastperiod=12, slowperiod=26, signalperiod=9)
# Returns: {'macd': [...], 'signal': [...], 'histogram': [...]}
```

### Market Data with Yahoo Finance

```python
# Get S&P 500 historical data
sp500_data = get_stock_history("^GSPC", period="6mo", interval="1d")

# Get Apple stock information
aapl_info = get_stock_info("AAPL")

# Download multiple stocks
multi_data = download_market_data(["AAPL", "MSFT", "GOOGL"], period="1mo")

# Search for stocks
search_results = search_symbols("Apple Inc", max_results=5)
```

### Combined Analysis Workflow

```python
# 1. Get market data
stock_data = get_stock_history("AAPL", period="3mo", interval="1d")
close_prices = stock_data["data"]["close"]

# 2. Calculate technical indicators
sma_20 = simple_moving_average(close_prices, timeperiod=20)
rsi = relative_strength_index(close_prices, timeperiod=14)
bb_bands = bollinger_bands(close_prices, timeperiod=20)

# 3. Analyze trends and signals
current_price = close_prices[-1]
current_sma = sma_20[-1]
trend_signal = "Bullish" if current_price > current_sma else "Bearish"
```

## File Structure

```
/
├── talib_mcp_server.py           # TA-Lib technical analysis server
├── yfinance_mcp_server.py        # Yahoo Finance market data server
├── requirements.txt              # TA-Lib server dependencies
├── yfinance_requirements.txt     # Yahoo Finance server dependencies
├── test_talib_mcp.py            # TA-Lib server tests
├── test_yfinance_mcp.py         # Yahoo Finance server tests
├── README.md                     # This documentation
├── yfinance_README.md           # Yahoo Finance server specific docs
├── advanced_sp500_prompts.md    # Advanced S&P 500 analysis examples
├── sp500_talib_analysis_prompts.md # S&P 500 technical analysis prompts
└── mcp_integration_guide.md     # MCP integration guidelines
```

## Technical Specifications

- **Total TA-Lib Indicators**: 31 professional indicators
- **Yahoo Finance Functions**: 9 comprehensive market data functions
- **Transport Protocol**: STDIO (Model Context Protocol standard)
- **Data Format**: JSON with numpy array serialization
- **Error Handling**: Comprehensive logging and exception management
- **Performance**: Multi-threaded data downloads, optimized calculations

## Use Cases

- **Algorithmic Trading**: Real-time technical analysis and signal generation
- **Portfolio Management**: Multi-asset analysis and risk assessment
- **Market Research**: Historical backtesting and pattern recognition
- **Financial Education**: Learning technical analysis concepts
- **Investment Analysis**: Fundamental and technical stock evaluation

This comprehensive MCP server suite provides everything needed for professional-grade financial analysis and trading applications.