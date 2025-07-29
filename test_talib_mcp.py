#!/usr/bin/env python3
"""
Test script for TA-Lib MCP Server
"""

import sys
import numpy as np

def generate_test_data(length=100):
    """Generate sample price data for testing"""
    np.random.seed(42)
    base_price = 100.0
    prices = [base_price]
    
    for i in range(1, length):
        change = np.random.normal(0, 1)
        new_price = prices[-1] + change
        prices.append(max(new_price, 1.0))  # Ensure positive prices
    
    # Generate OHLC data
    opens = [p * (1 + np.random.normal(0, 0.005)) for p in prices]
    highs = [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices]
    lows = [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices]
    volumes = [np.random.randint(1000, 10000) for _ in prices]
    
    return {
        'open': opens,
        'close': prices,
        'high': highs,
        'low': lows,
        'volume': volumes
    }

def test_indicators():
    """Test all implemented indicators"""
    print("Generating test data...")
    data = generate_test_data(100)
    
    try:
        # Import the server functions
        sys.path.append('.')
        from talib_mcp_server import (
            simple_moving_average, exponential_moving_average,
            bollinger_bands, relative_strength_index, macd,
            stochastic_oscillator, average_true_range,
            on_balance_volume, commodity_channel_index,
            williams_percent_r, stochastic_rsi, momentum,
            average_directional_index, double_exponential_moving_average,
            triple_exponential_moving_average, kaufman_adaptive_moving_average,
            normalized_average_true_range, standard_deviation,
            accumulation_distribution_line, chaikin_ad_oscillator,
            money_flow_index, doji_pattern, engulfing_pattern,
            hammer_pattern, shooting_star_pattern, parabolic_sar,
            rate_of_change, percentage_price_oscillator, trix
        )
        
        print("Testing Simple Moving Average...")
        sma = simple_moving_average(data['close'], timeperiod=20)
        print(f"SMA result length: {len(sma)}, sample values: {sma[-5:]}")
        
        print("Testing Exponential Moving Average...")
        ema = exponential_moving_average(data['close'], timeperiod=20)
        print(f"EMA result length: {len(ema)}, sample values: {ema[-5:]}")
        
        print("Testing Bollinger Bands...")
        bb = bollinger_bands(data['close'], timeperiod=20)
        print(f"BB upper sample: {bb['upper'][-5:]}")
        print(f"BB middle sample: {bb['middle'][-5:]}")
        print(f"BB lower sample: {bb['lower'][-5:]}")
        
        print("Testing RSI...")
        rsi = relative_strength_index(data['close'], timeperiod=14)
        print(f"RSI result length: {len(rsi)}, sample values: {rsi[-5:]}")
        
        print("Testing MACD...")
        macd_result = macd(data['close'])
        print(f"MACD line sample: {macd_result['macd'][-5:]}")
        print(f"Signal line sample: {macd_result['signal'][-5:]}")
        
        print("Testing Stochastic Oscillator...")
        stoch = stochastic_oscillator(data['high'], data['low'], data['close'])
        print(f"Stoch %K sample: {stoch['slowk'][-5:]}")
        print(f"Stoch %D sample: {stoch['slowd'][-5:]}")
        
        print("Testing ATR...")
        atr = average_true_range(data['high'], data['low'], data['close'])
        print(f"ATR result length: {len(atr)}, sample values: {atr[-5:]}")
        
        print("Testing OBV...")
        obv = on_balance_volume(data['close'], data['volume'])
        print(f"OBV result length: {len(obv)}, sample values: {obv[-5:]}")
        
        print("Testing CCI...")
        cci = commodity_channel_index(data['high'], data['low'], data['close'])
        print(f"CCI result length: {len(cci)}, sample values: {cci[-5:]}")
        
        print("Testing Williams %R...")
        willr = williams_percent_r(data['high'], data['low'], data['close'])
        print(f"Williams %R result length: {len(willr)}, sample values: {willr[-5:]}")
        
        print("Testing Stochastic RSI...")
        stoch_rsi = stochastic_rsi(data['close'])
        print(f"Stoch RSI fastk sample: {stoch_rsi['fastk'][-5:]}")
        
        print("Testing Momentum...")
        mom = momentum(data['close'])
        print(f"MOM result length: {len(mom)}, sample values: {mom[-5:]}")
        
        print("Testing ADX...")
        adx = average_directional_index(data['high'], data['low'], data['close'])
        print(f"ADX result length: {len(adx)}, sample values: {adx[-5:]}")
        
        print("Testing DEMA...")
        dema = double_exponential_moving_average(data['close'])
        print(f"DEMA result length: {len(dema)}, sample values: {dema[-5:]}")
        
        print("Testing TEMA...")
        tema = triple_exponential_moving_average(data['close'])
        print(f"TEMA result length: {len(tema)}, sample values: {tema[-5:]}")
        
        print("Testing KAMA...")
        kama = kaufman_adaptive_moving_average(data['close'])
        print(f"KAMA result length: {len(kama)}, sample values: {kama[-5:]}")
        
        print("Testing NATR...")
        natr = normalized_average_true_range(data['high'], data['low'], data['close'])
        print(f"NATR result length: {len(natr)}, sample values: {natr[-5:]}")
        
        print("Testing Standard Deviation...")
        stddev = standard_deviation(data['close'])
        print(f"STDDEV result length: {len(stddev)}, sample values: {stddev[-5:]}")
        
        print("Testing AD...")
        ad = accumulation_distribution_line(data['high'], data['low'], data['close'], data['volume'])
        print(f"AD result length: {len(ad)}, sample values: {ad[-5:]}")
        
        print("Testing ADOSC...")
        adosc = chaikin_ad_oscillator(data['high'], data['low'], data['close'], data['volume'])
        print(f"ADOSC result length: {len(adosc)}, sample values: {adosc[-5:]}")
        
        print("Testing MFI...")
        mfi = money_flow_index(data['high'], data['low'], data['close'], data['volume'])
        print(f"MFI result length: {len(mfi)}, sample values: {mfi[-5:]}")
        
        print("Testing Doji Pattern...")
        doji = doji_pattern(data['open'], data['high'], data['low'], data['close'])
        print(f"Doji pattern signals: {[x for x in doji[-10:] if x != 0]}")
        
        print("Testing Engulfing Pattern...")
        engulf = engulfing_pattern(data['open'], data['high'], data['low'], data['close'])
        print(f"Engulfing pattern signals: {[x for x in engulf[-10:] if x != 0]}")
        
        print("Testing Hammer Pattern...")
        hammer = hammer_pattern(data['open'], data['high'], data['low'], data['close'])
        print(f"Hammer pattern signals: {[x for x in hammer[-10:] if x != 0]}")
        
        print("Testing Parabolic SAR...")
        sar = parabolic_sar(data['high'], data['low'])
        print(f"SAR result length: {len(sar)}, sample values: {sar[-5:]}")
        
        print("Testing Rate of Change...")
        roc = rate_of_change(data['close'])
        print(f"ROC result length: {len(roc)}, sample values: {roc[-5:]}")
        
        print("Testing PPO...")
        ppo = percentage_price_oscillator(data['close'])
        print(f"PPO result length: {len(ppo)}, sample values: {ppo[-5:]}")
        
        print("Testing TRIX...")
        trix_result = trix(data['close'])
        print(f"TRIX result length: {len(trix_result)}, sample values: {trix_result[-5:]}")
        
        print("\nAll tests completed successfully!")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure required packages are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_indicators()
    sys.exit(0 if success else 1)