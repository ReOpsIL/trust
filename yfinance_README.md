# Yahoo Finance MCP Server

A comprehensive Model Context Protocol (MCP) server that provides access to Yahoo Finance market data through the yfinance library via FastMCP.

## Features

### Market Data Tools
- **Historical Data**: `get_stock_history()` - Get OHLCV data with flexible periods and intervals
- **Multiple Downloads**: `download_market_data()` - Bulk download data for multiple symbols
- **Real-time Quotes**: `get_multiple_quotes()` - Current market prices and key metrics
- **Search**: `search_symbols()` - Find stocks by company name or symbol

### Company Information
- **Stock Info**: `get_stock_info()` - Comprehensive company and market data
- **Financials**: `get_financials()` - Income statements, balance sheets, cash flow
- **Dividends & Splits**: `get_dividends_and_splits()` - Historical dividend and split data
- **Analyst Data**: `get_recommendations()` - Analyst recommendations and ratings
- **Earnings**: `get_earnings_calendar()` - Upcoming earnings dates and estimates

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r yfinance_requirements.txt
   ```

## Usage

### Running the Server

```bash
python yfinance_mcp_server.py
```

The server runs on STDIO transport by default, suitable for MCP clients.

### Testing

Run the test script to verify all tools work correctly:

```bash
python test_yfinance_mcp.py
```

## Available Tools

### 1. Stock History
```python
get_stock_history(
    symbol="AAPL",
    period="1mo",           # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval="1d",          # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    start="2023-01-01",     # Optional start date (YYYY-MM-DD)
    end="2023-12-31"        # Optional end date (YYYY-MM-DD)
)
```

### 2. Stock Information
```python
get_stock_info(symbol="AAPL")
# Returns: company details, market data, valuation metrics, dividend info
```

### 3. Multiple Quotes
```python
get_multiple_quotes(symbols=["AAPL", "MSFT", "GOOGL"])
# Returns: current prices, changes, volume, market cap for each symbol
```

### 4. Market Data Download
```python
download_market_data(
    symbols=["AAPL", "MSFT"],
    period="3mo",
    interval="1d",
    group_by="ticker"
)
```

### 5. Financial Statements
```python
get_financials(
    symbol="AAPL",
    financial_type="financials"  # "financials", "balance_sheet", "cashflow"
)
```

### 6. Dividends and Splits
```python
get_dividends_and_splits(symbol="AAPL")
# Returns: historical dividend payments and stock split events
```

### 7. Analyst Recommendations
```python
get_recommendations(symbol="AAPL")
# Returns: analyst ratings, upgrades, downgrades with dates
```

### 8. Symbol Search
```python
search_symbols(query="Apple", max_results=10)
# Returns: matching stocks with company names, sectors, exchanges
```

### 9. Earnings Calendar
```python
get_earnings_calendar(symbol="AAPL")
# Returns: upcoming earnings dates and estimates
```

## Data Periods and Intervals

### Valid Periods
- **Intraday**: `1d`, `5d`
- **Short-term**: `1mo`, `3mo`, `6mo`
- **Long-term**: `1y`, `2y`, `5y`, `10y`
- **Special**: `ytd` (year-to-date), `max` (all available data)

### Valid Intervals
- **Intraday**: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`
- **Daily**: `1d`, `5d`
- **Weekly/Monthly**: `1wk`, `1mo`, `3mo`

## Example Usage

```python
# Get Apple's recent stock history
history = get_stock_history("AAPL", period="1mo", interval="1d")

# Get company information
info = get_stock_info("AAPL")

# Compare multiple tech stocks
quotes = get_multiple_quotes(["AAPL", "MSFT", "GOOGL", "AMZN"])

# Download historical data for analysis
data = download_market_data(
    symbols=["AAPL", "MSFT"],
    start="2023-01-01",
    end="2023-12-31",
    interval="1d"
)

# Get financial statements
financials = get_financials("AAPL", "financials")
balance_sheet = get_financials("AAPL", "balance_sheet")
cashflow = get_financials("AAPL", "cashflow")

# Search for companies
results = search_symbols("artificial intelligence", max_results=10)
```

## Data Structure

All tools return structured dictionaries with:
- Consistent error handling (returns `{"error": "message"}` on failure)
- Properly formatted dates (YYYY-MM-DD HH:MM:SS)
- Numeric data as lists for easy processing
- Metadata including symbols, periods, and counts

## Limitations

- **Rate Limits**: Yahoo Finance may impose rate limits on requests
- **Data Availability**: Not all data is available for all symbols
- **Real-time Data**: Some data may have delays (typically 15-20 minutes)
- **Terms of Service**: Users should comply with Yahoo Finance's terms of service

## Error Handling

All tools include comprehensive error handling and will return structured error messages rather than throwing exceptions. Common errors include:
- Invalid symbols
- Network connectivity issues
- Data not available for requested period
- Rate limiting

## Total Tools: 9

This MCP server provides comprehensive access to Yahoo Finance data, suitable for financial analysis, research, and trading applications.

## Legal Notice

This tool uses the yfinance library to access Yahoo Finance data. Users should:
- Use data for personal/educational purposes
- Comply with Yahoo Finance's terms of service
- Not use for commercial redistribution without proper licensing
- Be aware that this is not an official Yahoo Finance API