import requests
import pandas as pd
import mplfinance as mpf

# 获取比特币K线数据
# url = 'https://api.binance.com/api/v3/klines'
# params = {
#     'symbol': 'BTCUSDT',
#     'interval': '1m',
#     'startTime': "1649193600000",
#     'limit': 1000
# }
# res = requests.get(url, params=params)
# data = res.json()
# df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# df.set_index('timestamp', inplace=True)

# df = df.apply(pd.to_numeric, errors='ignore')

# # 画K线图
# mpf.plot(df, type='candle', volume=True, style='binance')
