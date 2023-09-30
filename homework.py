
# %%
import finlab_crypto

finlab_crypto.setup()

import pandas as pd

btc = finlab_crypto.crawler.get_all_binance('BTCUSDT', '1d')
eth = finlab_crypto.crawler.get_all_binance('ETHUSDT', '1d')
bnb = finlab_crypto.crawler.get_all_binance('BNBUSDT', '1d')
df = pd.concat([btc, eth, bnb], keys=['BTC', 'ETH', 'BNB']).reset_index().rename(columns={'level_0': 'name'})

del btc
del eth
del bnb
#作業區
# %%
print('前五筆資料')
print(df.head())
# %%
print('每筆資料的[name]名子')
print(df.name)
# %%
print('第100筆資料，以及第100筆資料的[name]')
print(df.iloc[100].loc['name'])
# %%
print('有幾筆BTC的資料')
#df.name=='BTC'，判斷多少個是True,True的值是1，所以加總起來就是答案
print((df.name=='BTC').sum())
# %%
print('所有幣種的平均收盤價')
print(df.close.mean())
# %%
print('承上題，請計算標準差(Standard Deviation)')
print(df.close.std())
# %%
print('請提取所有BTC的資料，並存放在df_btc中')
#將BTC=true的rows提取，並製作新的DataFrame:df_btc
df_btc=df[df.name=='BTC']
print(df_btc)
# %%
print('請繪製出BTC的收盤價')
#index還沒改成日期
#print(df_btc.close.plot())
#index改成日期timestamp
print(df_btc.set_index('timestamp').close.plot())
# %%
print('請將df_btc的開高低收頻率改成「每月」，其他columns可以刪除')
df_btc=df_btc.set_index('timestamp')
#resample=頻率
df_btc_M=df_btc.resample('M').agg({
    'open':'first',#每個月的第一個價格
    'high':'max',#每個月最高的價格
    'low':'min',#每個月最低的價格
    'close':'last',#每個月的收盤價
    'volume':'sum'#總加
})
print(df_btc_M)
# %%
print('請繪製 BTC 的 100 天移動平均線')

print(df_btc.close.plot())
df_btc_100d_Mean=df_btc.close.rolling(100).mean()

print(df_btc_100d_Mean.plot())

# %%
print('請繪製BTC 每年最後一天的收盤價折線圖')


df_btc_Y=df_btc.close.resample('Y').last()
print(df_btc_Y.plot())


# %%
print('請計算BTC每年的平均價格')
df_btc_mean_Y=df_btc.close.resample('Y').mean()
print(df_btc_mean_Y)
# %%
print('請計算並繪製 BTC 的 100 天標準差')
df_btc_100d_std=df_btc.close.rolling(100).std()

print(df_btc_100d_std.plot())
# %%
print('請計算 BTC 的100日布林通道')
ub=df_btc_100d_Mean+2*df_btc_100d_std #Up bound通道上緣
lb=df_btc_100d_Mean-2*df_btc_100d_std #low bound通道下緣

print(df_btc.close.plot(color='black').set_title('Bollinger Band',color='blue'))
#btc的價格是"黑色"線條，並且設定圖表的名稱
print(df_btc_100d_Mean.plot())
print(ub.plot(color='r'))
print(lb.plot(color='g'))
# %%
print('BTC 收盤價大於1萬的資料，共有幾筆？')
(df_btc.close >10000).sum()
# %%
print('BTC 在星期幾持有報酬率最高？')
ret=df_btc.close/df_btc.open -1 #報酬率公式 return=收盤除以開盤-1
ret_week=ret.groupby(ret.index.weekday).sum()
#使用groupby分類group，將每個星期一做一個group,每個星期二做一個，以此類推，最後加總
#weekday，將index用星期一~日做命名
#0是星期一
print(ret.index.weekday)
print(ret_week)
print(ret_week.plot.bar())

# %%
print('BTC 上漲和下跌的天數？')
#shift()前一個資料
print(df_btc.close,df_btc.close.shift())

print('上漲',(df_btc.close>df_btc.close.shift()).sum(),'天')
print('下跌',(df_btc.close<df_btc.close.shift()).sum(),'天')

# %%
print('BTC 最近100天上漲下跌天數？')

print('近100天BTC上漲',(df_btc.close>df_btc.close.shift()).tail(100).sum(),'天')
print('近100天BTC下跌',(df_btc.close<df_btc.close.shift()).tail(100).sum(),'天')
# %%
print('BTC 近100日漲幅？')
df_btc.close.iloc[-1]/df_btc.close.iloc[-101]-1
#用iloc取出檔案中最後1筆跟最後第100筆資料
# %%
print('BTC 近100日最低價格？')
df_btc.low.tail(100).min()
# %%
print('BTC 近100日最高價格？')
df_btc.low.tail(100).max()
# %%
print('BTC 目前價格是否高於100日均價？')
if df_btc.close.iloc[-1]>df_btc.close.tail(100).mean():
    print('YES')
else:
    print('NO')
# %%
print('請從 df 製作一個新表格，columns 為加密貨幣的名稱，index為時間，而表格中的數值為收盤價，叫做df_close')
#reshape中的pivot可將index跟colums等變換成其他DetaFrame
df_close=df.pivot(index='timestamp',columns='name',values='close')
df_close

# %%
print('繪製這三種加密貨幣的收盤價於同一張圖上')
df_close.plot()
# %%
print('繪製BTC與ETH，於同一張圖表上（使用secondary_y=True）')
df_close.BTC.plot(ylabel='BTC')
df_close.ETH.plot(ylabel='ETH',secondary_y=True)
# %%
print('繪製三種加密貨幣從2018年開始的報酬率折線圖')
#loc['2018':] 冒號指的是2018含之後的所有資料都擷取
df_close.pct_change().loc['2018':].plot()

# %%
print('比較三種加密貨幣的每年年報酬（以每年收盤價結算即可）')
df_close.resample('Y').last().pct_change().plot.bar()

# %%
