#!/usr/bin/env python3
"""
Test script for Yahoo Finance MCP Server
"""

import sys
import json
from datetime import datetime, timedelta

def test_yfinance_tools():
    """Test all implemented yfinance tools"""
    print("Testing Yahoo Finance MCP Tools...")
    
    # Test symbols
    test_symbols = ['AAPL', 'MSFT', 'GOOGL']
    single_symbol = 'AAPL'
    
    try:
        # Import the server functions
        sys.path.append('.')
        from yfinance_mcp_server import (
            get_stock_history, get_stock_info, get_multiple_quotes,
            download_market_data, get_financials, get_dividends_and_splits,
            get_recommendations, search_symbols, get_earnings_calendar
        )
        
        print("Testing Stock History...")
        history = get_stock_history(single_symbol, period="5d")
        if "error" not in history:
            print(f"✓ Stock history for {single_symbol}: {history['count']} data points")
            print(f"  Date range: {history['data']['dates'][0]} to {history['data']['dates'][-1]}")
            print(f"  Latest close: ${history['data']['close'][-1]:.2f}")
        else:
            print(f"✗ Error getting stock history: {history['error']}")
        
        print("\nTesting Stock Info...")
        info = get_stock_info(single_symbol)
        if "error" not in info:
            print(f"✓ Stock info for {single_symbol}:")
            print(f"  Company: {info['basic_info']['longName']}")
            print(f"  Sector: {info['basic_info']['sector']}")
            print(f"  Current Price: ${info['market_data']['current_price']:.2f}")
            print(f"  Market Cap: ${info['market_data']['market_cap']:,}")
            print(f"  P/E Ratio: {info['valuation_metrics']['pe_ratio']}")
        else:
            print(f"✗ Error getting stock info: {info['error']}")
        
        print("\nTesting Multiple Quotes...")
        quotes = get_multiple_quotes(test_symbols)
        if "error" not in quotes:
            print("✓ Multiple quotes retrieved:")
            for symbol, data in quotes.items():
                if "error" not in data:
                    print(f"  {symbol}: ${data['current_price']:.2f} "
                          f"(Change: {data['change_percent']:.2f}%)")
                else:
                    print(f"  {symbol}: Error - {data['error']}")
        else:
            print(f"✗ Error getting multiple quotes: {quotes['error']}")
        
        print("\nTesting Market Data Download...")
        market_data = download_market_data(test_symbols[:2], period="1mo")
        if "error" not in market_data:
            print(f"✓ Downloaded market data for {len(market_data['symbols'])} symbols")
            for symbol in market_data['symbols']:
                if symbol in market_data['data']:
                    count = len(market_data['data'][symbol]['dates'])
                    print(f"  {symbol}: {count} data points")
        else:
            print(f"✗ Error downloading market data: {market_data['error']}")
        
        print("\nTesting Financials...")
        financials = get_financials(single_symbol, "financials")
        if "error" not in financials:
            yearly_periods = len(financials['yearly'].get('periods', []))
            quarterly_periods = len(financials['quarterly'].get('periods', []))
            print(f"✓ Financials for {single_symbol}:")
            print(f"  Yearly periods: {yearly_periods}")
            print(f"  Quarterly periods: {quarterly_periods}")
        else:
            print(f"✗ Error getting financials: {financials['error']}")
        
        print("\nTesting Dividends and Splits...")
        div_splits = get_dividends_and_splits(single_symbol)
        if "error" not in div_splits:
            div_count = len(div_splits['dividends'].get('dates', []))
            split_count = len(div_splits['splits'].get('dates', []))
            print(f"✓ Dividends and splits for {single_symbol}:")
            print(f"  Dividend payments: {div_count}")
            print(f"  Stock splits: {split_count}")
            if div_count > 0:
                print(f"  Latest dividend: ${div_splits['dividends']['amounts'][-1]:.4f} "
                      f"on {div_splits['dividends']['dates'][-1]}")
        else:
            print(f"✗ Error getting dividends/splits: {div_splits['error']}")
        
        print("\nTesting Analyst Recommendations...")
        recommendations = get_recommendations(single_symbol)
        if "error" not in recommendations:
            rec_count = len(recommendations['recommendations'])
            print(f"✓ Recommendations for {single_symbol}: {rec_count} entries")
            if rec_count > 0:
                latest = recommendations['recommendations'][0]
                print(f"  Latest: {latest['firm']} - {latest['to_grade']} ({latest['date']})")
        else:
            print(f"✗ Error getting recommendations: {recommendations['error']}")
        
        print("\nTesting Symbol Search...")
        search_results = search_symbols("Apple", max_results=5)
        if "error" not in search_results:
            result_count = len(search_results['results'])
            print(f"✓ Search results for 'Apple': {result_count} matches")
            for i, result in enumerate(search_results['results'][:3]):
                print(f"  {i+1}. {result['symbol']} - {result['shortname']}")
        else:
            print(f"✗ Error searching symbols: {search_results['error']}")
        
        print("\nTesting Earnings Calendar...")
        earnings = get_earnings_calendar(single_symbol)
        if "error" not in earnings:
            earnings_count = len(earnings['earnings_calendar'])
            print(f"✓ Earnings calendar for {single_symbol}: {earnings_count} entries")
            if earnings_count > 0:
                next_earning = earnings['earnings_calendar'][0]
                print(f"  Next earnings: {next_earning['date']}")
        else:
            print(f"✗ Error getting earnings calendar: {earnings['error']}")
        
        print("\n" + "="*50)
        print("✓ All Yahoo Finance MCP tests completed!")
        print("="*50)
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure required packages are installed: pip install -r yfinance_requirements.txt")
        return False
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_yfinance_tools()
    sys.exit(0 if success else 1)