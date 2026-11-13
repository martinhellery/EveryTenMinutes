import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')) + '/'
import pandas as pd, numpy as np
SP=_ROOT
cm=pd.read_csv(SP+'btc_cm.csv',parse_dates=['time']).set_index('time')
cb=pd.read_csv(SP+'data/CBBTCUSD.csv',parse_dates=['observation_date']).set_index('observation_date')['CBBTCUSD']
cb=pd.to_numeric(cb,errors='coerce').dropna()
p=cm['PriceUSD'].dropna()
p=p[:'2026-05-22']
tail=cb['2026-05-23':]
price=pd.concat([p,tail]).sort_index()
price.name='price'
price.to_csv(_ROOT+'book/price_daily.csv')
print(price.index.min(),price.index.max(),len(price))
# check continuity at join
print(p.iloc[-3:],tail.iloc[:3])
# cb vs cm overlap difference
ov=pd.concat([cm['PriceUSD'],cb],axis=1,keys=['cm','cb']).dropna()
print((ov['cb']/ov['cm']-1).describe())
