from common import *
import warnings; warnings.filterwarnings('ignore')


def data():
    p = price(); g = oro(); nq = fred('NASDAQCOM')
    if g is None:
        raise SystemExit('La figura 16.1 richiede data/oro.csv (vedi README).')
    df = pd.concat({'btc': p, 'gold': g, 'nq': nq}, axis=1, sort=True).loc['2024-01-01':'2026-10-02']
    df = df.dropna(subset=['gold', 'nq'])
    return df


def fig_16_1():
    df = data()
    d = df.loc['2024-12-31':]
    idx = d / d.iloc[0] * 100
    wk = df.resample('W-FRI').last().pct_change().dropna()
    roll_n = wk['btc'].rolling(26).corr(wk['nq'])
    roll_g = wk['btc'].rolling(26).corr(wk['gold'])
    roll_n = roll_n.loc['2025-01-01':]; roll_g = roll_g.loc['2025-01-01':]
    fig, (a, b) = plt.subplots(2, 1, figsize=(W, 4.1), sharex=True, gridspec_kw={'height_ratios': [1.55, 1], 'hspace': 0.14})
    a.plot(idx.index, idx['gold'], color=RUST, lw=1.0)
    a.plot(idx.index, idx['nq'], color=BLUE, lw=1.0)
    a.plot(idx.index, idx['btc'], color=INK, lw=1.0)
    a.axhline(100, color=GREY, lw=0.5)
    a.set_ylabel('31 dic 2024 = 100')
    a.yaxis.set_major_formatter(fmt_axis(0))
    last = idx.index[-1]
    for c, col, lab, dy in [('gold', RUST, 'Oro', 0), ('nq', BLUE, 'Nasdaq', 0), ('btc', INK, 'Bitcoin', -4)]:
        a.text(last + pd.Timedelta(days=8), idx[c].iloc[-1] + dy, f'{lab} {it(idx[c].iloc[-1])}', color=col, fontsize=6.2, va='center')
    a.set_xlim(idx.index[0], pd.Timestamp('2026-12-20'))
    b.plot(roll_n.index, roll_n, color=BLUE, lw=1.0)
    b.plot(roll_g.index, roll_g, color=RUST, lw=1.0)
    b.axhline(0, color=GREY, lw=0.5)
    b.set_ylabel('Correlazione di Bitcoin\n(26 settimane)')
    b.set_ylim(-0.5, 0.9)
    b.yaxis.set_major_formatter(fmt_axis(1))
    b.text(roll_n.index[-1] + pd.Timedelta(days=8), roll_n.iloc[-1], f'Nasdaq {it(roll_n.iloc[-1],2)}', color=BLUE, fontsize=6.2, va='center')
    b.text(roll_g.index[-1] + pd.Timedelta(days=8), roll_g.iloc[-1], f'Oro {it(roll_g.iloc[-1],2)}', color=RUST, fontsize=6.2, va='center')
    b.xaxis.set_major_formatter(it_month_fmt())
    b.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    print(roll_n.describe().round(2).to_dict(), roll_g.describe().round(2).to_dict())
    save(fig, 'f16_1_prova')


if __name__ == '__main__':
    fig_16_1()
