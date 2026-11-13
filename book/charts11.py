from common import *


def fig_18_1():
    ff = fred('FEDFUNDS'); cpi = fred('CPIAUCSL')
    yoy = cpi.pct_change(12) * 100
    real = (ff - yoy).dropna().loc['1955-01-01':]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.fill_between(real.index, 0, real.values, where=real.values >= 0, color=LIGHT, lw=0, interpolate=True)
    ax.fill_between(real.index, 0, real.values, where=real.values < 0, color=RUST, lw=0, interpolate=True, alpha=0.9)
    ax.plot(real.index, real.values, color=INK, lw=0.5)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_ylabel('Tasso della Fed meno inflazione, punti %')
    ax.set_ylim(-10, 10.5)
    ax.yaxis.set_major_formatter(fmt_axis(1))
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlim(pd.Timestamp('1955-01-01'), pd.Timestamp('2027-06-01'))
    ax.grid(axis='x', visible=False)
    def lab(x, y, s, ha='center'):
        ax.text(pd.Timestamp(x), y, s, fontsize=5.8, color=INK, ha=ha, va='center', linespacing=1.15)
    lab('1976-01-01', -7.2, '1974-77\nfino a -5,0')
    lab('2012-01-01', -6.0, '2009-14\nfino a -3,7')
    lab('2019-03-01', -8.6, '2020-23: fino a -8,4', ha='right')
    lab('1984-01-01', 9.0, 'anni Ottanta: tassi reali\nmolto positivi', ha='left')
    print('share negative', (real < 0).mean())
    save(fig, 'f18_1_tasso_reale')


if __name__ == '__main__':
    fig_18_1()
