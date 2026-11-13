from common import *
from scipy import stats
import charts2
GEN = charts2.GEN


def pl_fit(end='2019-03-22'):
    p = price()['2011-01-01':]
    tr = p[:end]
    d = (tr.index - GEN).days.values
    b, a = np.polyfit(np.log10(d), np.log10(tr.values), 1)
    return a, b


def s2f_series():
    c = cm()
    sup = c['SplyCur']
    flow = c['IssTotNtv'].rolling(30).mean() * 365
    sf = sup / flow
    p = price()[:'2026-05-22']
    mc = p * sup.reindex(p.index)
    df = pd.concat([np.log(sf), np.log(mc)], axis=1, keys=['lsf', 'lmc']).dropna()['2010-10-01':]
    tr = df[:'2019-03-22']
    b, a = np.polyfit(tr['lsf'], tr['lmc'], 1)
    return df, sup, a, b


DATES = ['2020-05-12', '2021-11-08', '2024-04-21', '2025-10-06']


def ratios():
    a, b = pl_fit()
    p = price()
    df, sup, sa, sb = s2f_series()
    out = []
    for dt in DATES:
        t = pd.Timestamp(dt)
        n = (t - GEN).days
        pl = 10 ** (a + b * np.log10(n))
        act = p.asof(t)
        r = df.loc[:t].iloc[-1]
        s2 = np.exp(sa + sb * r['lsf']) / sup.asof(t)
        out.append((dt, act / pl, act / s2))
    return out


def fig_13_3():
    p = price()['2014-01-01':]
    r = np.log(p).diff().dropna()
    z = (r - r.mean()) / r.std()
    n = len(z)
    big = (z.abs() > 4).sum()
    exp = n * 2 * stats.norm.sf(4)
    print('days', n, 'sd', r.std(), '>4sd', big, 'expected normal', exp, '>3sd', (z.abs() > 3).sum(), n * 2 * stats.norm.sf(3))
    fig, ax = plt.subplots(figsize=(W, 2.5))
    bins = np.linspace(-8, 8, 65)
    h, e = np.histogram(z.clip(-7.9, 7.9), bins=bins, density=True)
    c = (e[1:] + e[:-1]) / 2
    ax.bar(c, h, width=e[1] - e[0], color=INK, alpha=0.85, label='Bitcoin, rendimenti giornalieri')
    xs = np.linspace(-8, 8, 400)
    ax.plot(xs, stats.norm.pdf(xs), color=RUST, lw=1.4, label='curva normale')
    ax.set_yscale('log')
    ax.set_ylim(1e-5, 1)
    ax.set_xlim(-8, 8)
    ax.set_xlabel('Variazione giornaliera, in deviazioni standard dalla media')
    ax.set_ylabel('Frequenza (scala log)')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, q: it(v, 5 if v < 1e-3 else (3 if v < 1e-1 else 0)).rstrip('0').rstrip(',') if v < 1 else '1'))
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2, fontsize=6.3)
    save(fig, 'f13_3_code_grasse')
    return n, big, exp


def fig_13_4():
    rr = ratios()
    fig, ax = plt.subplots(figsize=(W, 2.5))
    xs = np.arange(len(rr))
    ax.axhline(1, color=GREY, lw=0.8)
    ax.plot(xs - 0.07, [r[1] for r in rr], 'o-', color=INK, ms=4.5, lw=0.8, label='Legge di potenza')
    ax.plot(xs + 0.07, [r[2] for r in rr], 's-', color=RUST, ms=4.5, lw=0.8, label='Stock-to-flow')
    ax.set_yscale('log')
    ax.set_ylim(0.1, 5)
    ax.set_yticks([0.1, 0.25, 0.5, 1, 2, 4])
    ax.set_yticklabels(['un decimo', 'un quarto', 'metà', 'giusto', 'doppio', 'quadruplo'], fontsize=6.2)
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, q: ''))
    ax.set_xticks(xs)
    ax.set_xticklabels(['Halving\nmag 2020', 'Massimo\nnov 2021', 'Halving\napr 2024', 'Massimo\nott 2025'], fontsize=6.3)
    ax.set_xlim(-0.4, len(rr) - 0.6)
    ax.set_ylabel('Prezzo reale rispetto al modello')
    ax.grid(axis='x', visible=False)
    ax.legend(loc='lower left', fontsize=6.3)
    for x, r in zip(xs, rr):
        ax.text(x - 0.07, r[1] * (1.25 if r[1] >= 1 else 0.78), it(r[1], 2), ha='center', fontsize=5.6, color=INK, va='center')
        ax.text(x + 0.07, r[2] * (0.78 if r[2] < r[1] else 1.25), it(r[2], 2), ha='center', fontsize=5.6, color=RUST, va='center')
    save(fig, 'f13_4_errori')
    for r in rr:
        print(r)


if __name__ == '__main__':
    print(fig_13_3())
    fig_13_4()
