import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')) + '/'
import pandas as pd, numpy as np
SP=_ROOT
price=pd.read_csv('price_daily.csv',index_col=0,parse_dates=True)['price']
cm=pd.read_csv(SP+'btc_cm.csv',parse_dates=['time']).set_index('time')
genesis=pd.Timestamp('2009-01-03')
d=(price.index-genesis).days.values
ok=d>0
# Power law fits
def fit(start,end):
    m=(price.index>=start)&(price.index<=end)
    x=np.log10(d[m]);y=np.log10(price.values[m])
    b,a=np.polyfit(x,y,1)
    r=y-(a+b*x)
    r2=1-r.var()/y.var()
    return a,b,r2,r.std()
for s,e in [('2011-01-01','2026-10-03'),('2011-01-01','2020-12-31'),('2013-01-01','2026-10-03'),('2011-01-01','2024-12-31')]:
    a,b,r2,sd=fit(s,e)
    t=(pd.Timestamp('2026-10-03')-genesis).days
    pred=10**(a+b*np.log10(t))
    print(s,e,'slope %.3f int %.3f R2 %.3f sd(log10) %.3f'%(b,a,r2,sd),'fit today %.0f'%pred,'actual %.0f'%price.iloc[-1],'ratio %.2f'%(price.iloc[-1]/pred),'z %.2f'%(np.log10(price.iloc[-1]/pred)/sd))
    for yr in [2030,2035]:
        tt=(pd.Timestamp(f'{yr}-12-31')-genesis).days
        print('  ',yr,'centre %.0f  -2sd %.0f  +2sd %.0f'%(10**(a+b*np.log10(tt)),10**(a+b*np.log10(tt)-2*sd),10**(a+b*np.log10(tt)+2*sd)))
# in-sample 2011-2020 extrapolated: where was the price vs the line in 2021-2026
a,b,r2,sd=fit('2011-01-01','2020-12-31')
for dt in ['2021-11-08','2022-11-21','2024-03-14','2025-10-06','2026-07-01','2026-10-03']:
    t=(pd.Timestamp(dt)-genesis).days
    pr=price[dt] if dt in price else price.asof(pd.Timestamp(dt))
    print(dt,'price %.0f fit %.0f ratio %.2f'%(pr,10**(a+b*np.log10(t)),pr/10**(a+b*np.log10(t))))
# Stock to flow
sup=cm['SplyCur'];iss=cm['IssTotNtv']
# annual flow = trailing 365d issuance
flow=iss.rolling(365).sum()
sf=(sup/flow).dropna()
mc=(price*sup.reindex(price.index)).dropna()
df=pd.concat([np.log(sf),np.log(mc)],axis=1,keys=['lsf','lmc']).dropna()
df=df[df.index>='2010-10-01']
tr=df[:'2019-03-22']
b,a=np.polyfit(tr['lsf'],tr['lmc'],1)
res=tr['lmc']-(a+b*tr['lsf']);r2=1-res.var()/tr['lmc'].var()
print('S2F fit to 2019-03-22: slope %.3f int %.3f R2 %.3f'%(b,a,r2), 'n',len(tr))
for dt in ['2020-05-11','2021-11-08','2024-04-20','2025-10-06']:
    r=df.loc[dt] if dt in df.index else df.loc[:dt].iloc[-1]
    pred_mc=np.exp(a+b*r['lsf']);act=np.exp(r['lmc']); s=sup.asof(pd.Timestamp(dt))
    print(dt,'SF %.1f pred price %.0f actual %.0f ratio %.2f'%(np.exp(r['lsf']),pred_mc/s,act/s,act/pred_mc))
# drawdowns
rm=price.cummax(); dd=price/rm-1
for a_,b_ in [('2011-06-01','2012-06-01'),('2013-12-01','2015-06-01'),('2017-12-01','2019-01-01'),('2021-11-01','2023-01-01'),('2025-10-01','2026-10-03')]:
    s=dd[a_:b_]; print(a_,b_,'min %.1f%% on %s'%(s.min()*100,s.idxmin().date()))
# fee share
fee=cm['FeeTotNtv'];
