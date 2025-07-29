#!/usr/bin/env python3
"""
Yahoo Finance MCP Server
Provides market data access through Model Context Protocol using yfinance
"""

import yfinance as yf
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from fastmcp import FastMCP
import logging
import json

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("Yahoo Finance Data")

@mcp.tool
def get_stock_history(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
    start: Optional[str] = None,
    end: Optional[str] = None,
    prepost: bool = True,
    auto_adjust: bool = True,
    back_adjust: bool = False
) -> Dict[str, Any]:
    """
    Get historical market data for a stock
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        start: Start date string (YYYY-MM-DD)
        end: End date string (YYYY-MM-DD)
        prepost: Include pre and post market data
        auto_adjust: Adjust prices for dividends and splits
        back_adjust: Back-adjust prices for dividends and splits
    
    Returns:
        Dictionary with OHLCV data and metadata
    """
    try:
        ticker = yf.Ticker(symbol)
        
        if start and end:
            hist = ticker.history(start=start, end=end, interval=interval, 
                                prepost=prepost, auto_adjust=auto_adjust, back_adjust=back_adjust)
        else:
            hist = ticker.history(period=period, interval=interval, 
                                prepost=prepost, auto_adjust=auto_adjust, back_adjust=back_adjust)
        
        if hist.empty:
            return {"error": f"No data found for symbol {symbol}"}
        
        # Convert to dictionary format
        result = {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "data": {
                "dates": [date.strftime('%Y-%m-%d %H:%M:%S') for date in hist.index],
                "open": hist['Open'].tolist(),
                "high": hist['High'].tolist(),
                "low": hist['Low'].tolist(),
                "close": hist['Close'].tolist(),
                "volume": hist['Volume'].tolist()
            },
            "count": len(hist)
        }
        
        # Add dividends and splits if available
        if 'Dividends' in hist.columns:
            result["data"]["dividends"] = hist['Dividends'].tolist()
        if 'Stock Splits' in hist.columns:
            result["data"]["stock_splits"] = hist['Stock Splits'].tolist()
            
        return result
        
    except Exception as e:
        logging.error(f"Error fetching history for {symbol}: {e}")
        return {"error": str(e)}

@mcp.tool
def get_stock_info(symbol: str) -> Dict[str, Any]:
    """
    Get comprehensive stock information
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Dictionary with detailed stock information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info:
            return {"error": f"No information found for symbol {symbol}"}
        
        # Extract key information
        result = {
            "symbol": symbol,
            "basic_info": {
                "longName": info.get("longName"),
                "shortName": info.get("shortName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "website": info.get("website"),
                "business_summary": info.get("longBusinessSummary")
            },
            "market_data": {
                "current_price": info.get("currentPrice"),
                "previous_close": info.get("previousClose"),
                "open": info.get("open"),
                "day_low": info.get("dayLow"),
                "day_high": info.get("dayHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "volume": info.get("volume"),
                "average_volume": info.get("averageVolume"),
                "market_cap": info.get("marketCap"),
                "shares_outstanding": info.get("sharesOutstanding"),
                "float_shares": info.get("floatShares")
            },
            "valuation_metrics": {
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "price_to_book": info.get("priceToBook"),
                "price_to_sales": info.get("priceToSalesTrailing12Months"),
                "enterprise_value": info.get("enterpriseValue"),
                "profit_margins": info.get("profitMargins"),
                "return_on_equity": info.get("returnOnEquity")
            },
            "dividend_info": {
                "dividend_rate": info.get("dividendRate"),
                "dividend_yield": info.get("dividendYield"),
                "payout_ratio": info.get("payoutRatio"),
                "ex_dividend_date": info.get("exDividendDate")
            }
        }
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching info for {symbol}: {e}")
        return {"error": str(e)}

@mcp.tool
def get_multiple_quotes(symbols: List[str]) -> Dict[str, Any]:
    """
    Get current quotes for multiple stocks
    
    Args:
        symbols: List of stock ticker symbols
    
    Returns:
        Dictionary with quote data for each symbol
    """
    try:
        tickers = yf.Tickers(' '.join(symbols))
        
        result = {}
        for symbol in symbols:
            try:
                ticker = tickers.tickers[symbol]
                info = ticker.info
                
                result[symbol] = {
                    "current_price": info.get("currentPrice"),
                    "previous_close": info.get("previousClose"),
                    "open": info.get("open"),
                    "day_low": info.get("dayLow"),
                    "day_high": info.get("dayHigh"),
                    "volume": info.get("volume"),
                    "market_cap": info.get("marketCap"),
                    "pe_ratio": info.get("trailingPE"),
                    "change": info.get("regularMarketChange"),
                    "change_percent": info.get("regularMarketChangePercent")
                }
            except Exception as e:
                result[symbol] = {"error": str(e)}
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching quotes: {e}")
        return {"error": str(e)}

@mcp.tool
def download_market_data(
    symbols: List[str],
    period: str = "1mo",
    interval: str = "1d",
    start: Optional[str] = None,
    end: Optional[str] = None,
    group_by: str = "ticker",
    auto_adjust: bool = True,
    prepost: bool = True,
    threads: bool = True
) -> Dict[str, Any]:
    """
    Download market data for multiple symbols
    
    Args:
        symbols: List of stock ticker symbols
        period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        start: Start date string (YYYY-MM-DD)
        end: End date string (YYYY-MM-DD)
        group_by: Group by 'ticker' or 'column'
        auto_adjust: Adjust prices for dividends and splits
        prepost: Include pre and post market data
        threads: Use threading for faster downloads
    
    Returns:
        Dictionary with market data for all symbols
    """
    try:
        if start and end:
            data = yf.download(symbols, start=start, end=end, interval=interval,
                             group_by=group_by, auto_adjust=auto_adjust, 
                             prepost=prepost, threads=threads)
        else:
            data = yf.download(symbols, period=period, interval=interval,
                             group_by=group_by, auto_adjust=auto_adjust, 
                             prepost=prepost, threads=threads)
        
        if data.empty:
            return {"error": "No data found for the specified symbols"}
        
        result = {
            "symbols": symbols,
            "period": period,
            "interval": interval,
            "group_by": group_by,
            "data": {}
        }
        
        if len(symbols) == 1:
            # Single symbol case
            symbol = symbols[0]
            result["data"][symbol] = {
                "dates": [date.strftime('%Y-%m-%d %H:%M:%S') for date in data.index],
                "open": data['Open'].tolist() if 'Open' in data.columns else [],
                "high": data['High'].tolist() if 'High' in data.columns else [],
                "low": data['Low'].tolist() if 'Low' in data.columns else [],
                "close": data['Close'].tolist() if 'Close' in data.columns else [],
                "volume": data['Volume'].tolist() if 'Volume' in data.columns else []
            }
        else:
            # Multiple symbols case
            for symbol in symbols:
                if symbol in data.columns.get_level_values(1):
                    symbol_data = data.xs(symbol, axis=1, level=1) if group_by == "ticker" else data[symbol]
                    result["data"][symbol] = {
                        "dates": [date.strftime('%Y-%m-%d %H:%M:%S') for date in symbol_data.index],
                        "open": symbol_data['Open'].tolist() if 'Open' in symbol_data.columns else [],
                        "high": symbol_data['High'].tolist() if 'High' in symbol_data.columns else [],
                        "low": symbol_data['Low'].tolist() if 'Low' in symbol_data.columns else [],
                        "close": symbol_data['Close'].tolist() if 'Close' in symbol_data.columns else [],
                        "volume": symbol_data['Volume'].tolist() if 'Volume' in symbol_data.columns else []
                    }
        
        return result
        
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        return {"error": str(e)}

@mcp.tool
def get_financials(
    symbol: str,
    financial_type: str = "financials"
) -> Dict[str, Any]:
    """
    Get financial statements for a stock
    
    Args:
        symbol: Stock ticker symbol
        financial_type: Type of financial data ('financials', 'balance_sheet', 'cashflow')
    
    Returns:
        Dictionary with financial statement data
    """
    try:
        ticker = yf.Ticker(symbol)
        
        if financial_type == "financials":
            quarterly = ticker.quarterly_financials
            yearly = ticker.financials
        elif financial_type == "balance_sheet":
            quarterly = ticker.quarterly_balance_sheet
            yearly = ticker.balance_sheet
        elif financial_type == "cashflow":
            quarterly = ticker.quarterly_cashflow
            yearly = ticker.cashflow
        else:
            return {"error": f"Invalid financial_type: {financial_type}"}
        
        result = {
            "symbol": symbol,
            "financial_type": financial_type,
            "yearly": {},
            "quarterly": {}
        }
        
        # Process yearly data
        if not yearly.empty:
            result["yearly"] = {
                "periods": [date.strftime('%Y-%m-%d') for date in yearly.columns],
                "data": {}
            }
            for idx in yearly.index:
                result["yearly"]["data"][str(idx)] = yearly.loc[idx].tolist()
        
        # Process quarterly data
        if not quarterly.empty:
            result["quarterly"] = {
                "periods": [date.strftime('%Y-%m-%d') for date in quarterly.columns],
                "data": {}
            }
            for idx in quarterly.index:
                result["quarterly"]["data"][str(idx)] = quarterly.loc[idx].tolist()
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching financials for {symbol}: {e}")
        return {"error": str(e)}

@mcp.tool
def get_dividends_and_splits(symbol: str) -> Dict[str, Any]:
    """
    Get dividend and stock split history
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Dictionary with dividend and split history
    """
    try:
        ticker = yf.Ticker(symbol)
        
        dividends = ticker.dividends
        splits = ticker.splits
        
        result = {
            "symbol": symbol,
            "dividends": {},
            "splits": {}
        }
        
        # Process dividends
        if not dividends.empty:
            result["dividends"] = {
                "dates": [date.strftime('%Y-%m-%d') for date in dividends.index],
                "amounts": dividends.tolist()
            }
        
        # Process splits
        if not splits.empty:
            result["splits"] = {
                "dates": [date.strftime('%Y-%m-%d') for date in splits.index],
                "ratios": splits.tolist()
            }
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching dividends/splits for {symbol}: {e}")
        return {"error": str(e)}

@mcp.tool
def get_recommendations(symbol: str) -> Dict[str, Any]:
    """
    Get analyst recommendations for a stock
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Dictionary with analyst recommendations
    """
    try:
        ticker = yf.Ticker(symbol)
        recommendations = ticker.recommendations
        
        if recommendations is None or recommendations.empty:
            return {"error": f"No recommendations found for {symbol}"}
        
        result = {
            "symbol": symbol,
            "recommendations": []
        }
        
        for idx, row in recommendations.iterrows():
            rec_data = {
                "date": idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx),
                "firm": row.get('Firm', ''),
                "to_grade": row.get('To Grade', ''),
                "from_grade": row.get('From Grade', ''),
                "action": row.get('Action', '')
            }
            result["recommendations"].append(rec_data)
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching recommendations for {symbol}: {e}")
        return {"error": str(e)}

@mcp.tool
def search_symbols(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Search for stock symbols and company names
    
    Args:
        query: Search query (company name or symbol)
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary with search results
    """
    try:
        search_results = yf.Search(query, max_results=max_results)
        quotes = search_results.quotes
        
        result = {
            "query": query,
            "results": []
        }
        
        for quote in quotes[:max_results]:
            result["results"].append({
                "symbol": quote.get("symbol", ""),
                "shortname": quote.get("shortname", ""),
                "longname": quote.get("longname", ""),
                "exchange": quote.get("exchange", ""),
                "sector": quote.get("sector", ""),
                "industry": quote.get("industry", ""),
                "market_cap": quote.get("marketCap"),
                "type": quote.get("quoteType", "")
            })
        
        return result
        
    except Exception as e:
        logging.error(f"Error searching for {query}: {e}")
        return {"error": str(e)}

@mcp.tool
def get_earnings_calendar(symbol: str) -> Dict[str, Any]:
    """
    Get earnings calendar for a stock
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Dictionary with earnings calendar data
    """
    try:
        ticker = yf.Ticker(symbol)
        calendar = ticker.calendar
        
        if calendar is None or calendar.empty:
            return {"error": f"No earnings calendar found for {symbol}"}
        
        result = {
            "symbol": symbol,
            "earnings_calendar": []
        }
        
        for idx, row in calendar.iterrows():
            earning_data = {
                "date": idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)
            }
            for col in calendar.columns:
                earning_data[col.lower().replace(' ', '_')] = row[col]
            
            result["earnings_calendar"].append(earning_data)
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching earnings calendar for {symbol}: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()