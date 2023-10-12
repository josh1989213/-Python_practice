# %%
import finlab_crypto
finlab_crypto.setup()
import pandas as pd

# %%
#BTCUSDT
ohlcv_BTCUSDT_15m=finlab_crypto.crawler.get_all_binance('BTCUSDT','15m')
ohlcv_BTCUSDT_1h=finlab_crypto.crawler.get_all_binance('BTCUSDT','1h')
ohlcv_BTCUSDT_4h=finlab_crypto.crawler.get_all_binance('BTCUSDT','4h')
ohlcv_BTCUSDT_1d=finlab_crypto.crawler.get_all_binance('BTCUSDT','1d')

#ETHUSDT
ohlcv_ETHUSDT_15m=finlab_crypto.crawler.get_all_binance('ETHUSDT','15m')
ohlcv_ETHUSDT_1h=finlab_crypto.crawler.get_all_binance('ETHUSDT','1h')
ohlcv_ETHUSDT_4h=finlab_crypto.crawler.get_all_binance('ETHUSDT','4h')
ohlcv_ETHUSDT_1d=finlab_crypto.crawler.get_all_binance('ETHUSDT','1d')

#BNBUSDT
ohlcv_BNBUSDT_15m=finlab_crypto.crawler.get_all_binance('BNBUSDT','15m')
ohlcv_BNBUSDT_1h=finlab_crypto.crawler.get_all_binance('BNBUSDT','1h')
ohlcv_BNBUSDT_4h=finlab_crypto.crawler.get_all_binance('BNBUSDT','4h')
ohlcv_BNBUSDT_1d=finlab_crypto.crawler.get_all_binance('BNBUSDT','1d')

df_15m=pd.concat([ohlcv_BTCUSDT_15m,ohlcv_ETHUSDT_15m,ohlcv_BNBUSDT_15m],keys=['BTC','ETH','BNB']).reset_index().rename(columns={'level_0':'name'})
print(df_15m) 
df_1h=pd.concat([ohlcv_BTCUSDT_1h,ohlcv_ETHUSDT_1h,ohlcv_BNBUSDT_1h],keys=['BTC','ETH','BNB']).reset_index().rename(columns={'level_0':'name'})
print(df_1h) 
df_4h=pd.concat([ohlcv_BTCUSDT_4h,ohlcv_ETHUSDT_4h,ohlcv_BNBUSDT_4h],keys=['BTC','ETH','BNB']).reset_index().rename(columns={'level_0':'name'})
print(df_1h) 
df_1d=pd.concat([ohlcv_BTCUSDT_1d,ohlcv_ETHUSDT_1d,ohlcv_BNBUSDT_1d],keys=['BTC','ETH','BNB']).reset_index().rename(columns={'level_0':'name'})
print(df_1d) 
del ohlcv_BTCUSDT_15m
del ohlcv_ETHUSDT_15m
del ohlcv_BNBUSDT_15m
del ohlcv_BTCUSDT_1h
del ohlcv_ETHUSDT_1h
del ohlcv_BNBUSDT_1h
del ohlcv_BTCUSDT_4h
del ohlcv_ETHUSDT_4h
del ohlcv_BNBUSDT_4h
del ohlcv_BTCUSDT_1d
del ohlcv_ETHUSDT_1d
del ohlcv_BNBUSDT_1d
# %%
#雙均線策略
#BTC 20日60日平均移動線
df_btc_4h= df_4h[ df_4h.name=='BTC'].set_index('timestamp')
btc_close=df_btc_4h.close
SMA20=btc_close.rolling(20).mean()
SMA60=btc_close.rolling(60).mean()
entries=(SMA20>SMA60) &(SMA20.shift()<SMA60.shift())
exits=(SMA20<SMA60) & (SMA20.shift()>SMA60.shift())

print(btc_close.plot(color='red'))
print(SMA20.plot())
print(SMA60.plot(color='black'))
#.astype(int)將布林直轉化成數值以便圖表輸出
print(entries.astype(int).plot(secondary_y=True))
print((-exits.astype(int)).plot(secondary_y=True))
# %%
#回測
# vectorbt 回測的程式
import vectorbt as vbt
portfolio=vbt.Portfolio.from_signals(btc_close,entries,exits,freq='4h')
#cumulative_returns()累積報酬率
portfolio.cumulative_returns().plot().set_title('back test')
#紀錄回測中的交易
portfolio.positions.records
# %%
#回撤=最大虧損
portfolio.drawdown().plot().set_title('BTC_drawdown')
# %%
#年報酬率
portfolio.annual_returns().plot().set_title('BTC_annual_returns')
# %%

#打包策略
from finlab_crypto import Strategy
import numpy as np
@Strategy(sma1=20,sma2=60)
def sma_strategy(df_btc_4h):
    df_btc_4h= df_4h[ df_4h.name=='BTC'].set_index('timestamp')
    btc_close=df_btc_4h.close
    SMA20=btc_close.rolling(sma_strategy.sma1).mean()
    SMA60=btc_close.rolling(sma_strategy.sma2).mean()
    entries=(SMA20>SMA60) &(SMA20.shift()<SMA60.shift())
    exits=(SMA20<SMA60) & (SMA20.shift()>SMA60.shift())
    
    figurs={
        'overlaps' :{
            'SMA20':SMA20,
            'SMA60':SMA60
    }
    }

    return entries,exits,figurs
# %%


portfolio=sma_strategy.backtest(df_btc_4h,freq='4h',plot=True)


# %%
variables = {'sma1': np.arange(20,310,10), 'sma2': np.arange(20,310,10)}
portfolio=sma_strategy.backtest(df_btc_4h,variables=variables,freq='4h',plot=True)
# %%
