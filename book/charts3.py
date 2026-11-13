from common import *
import math

def fig_1_1():
    c = fred('CPIAUCNS')
    c = c['1913-01-01':]
    pa = 1 / (c / c.iloc[0])  # potere d'acquisto, 1913 = 1 dollaro
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(pa.index, pa.values * 100, color=RUST, lw=1.3)
    ax.set_yscale('log')
    ax.set_ylim(2, 130)
    ax.set_yticks([3, 10, 30, 100])
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, p: ''))
    ax.set_ylabel('Centesimi di dollaro del 1913 (scala log)')
    ax.xaxis.set_major_locator(mdates.YearLocator(20))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    marks = [('1913-12-23', 'Nasce la Federal\nReserve (1913)', 13), ('1971-08-15', 'Fine della convertibilità\nin oro (1971)', 70)]
    for d, lab, y in marks:
        t = pd.Timestamp(d)
        ax.axvline(t, color=GREY, lw=0.5, ls=':')
        ax.text(t + pd.Timedelta(days=700), y, lab, fontsize=6, color=INK, va='top')
    last = pa.iloc[-1] * 100
    ax.plot([pa.index[-1]], [last], 'o', color=INK, ms=3.5)
    ax.text(pa.index[-1] - pd.Timedelta(days=500), 2.45, f'Oggi: circa {it(last,1)} centesimi', fontsize=6.5, ha='right', color=INK)
    save(fig, 'f1_1_potere_acquisto')
    print(last)

def fig_1_2():
    c = fred('CPIAUCSL')
    y = (c.pct_change(12) * 100).dropna()['1960-01-01':]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.fill_between(y.index, 0, y.values, where=y.values >= 0, color=RUST_L, lw=0)
    ax.plot(y.index, y.values, color=RUST, lw=0.9)
    ax.axhline(0, color=GREY, lw=0.5)
    ax.set_ylabel('Inflazione annua (%)')
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ymax = y['1979':'1982'].idxmax(); ax.annotate(f'{it(y[ymax],1)}%\n({ymax.strftime("%m/%Y")})', xy=(ymax, y[ymax]), xytext=(pd.Timestamp('1987-01-01'), 13.5), fontsize=6.5, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5))
    y2 = y['2021':'2023'].idxmax(); ax.annotate(f'{it(y[y2],1)}%\n({y2.strftime("%m/%Y")})', xy=(y2, y[y2]), xytext=(pd.Timestamp('2008-06-01'), 10.5), fontsize=6.5, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5))
    ax.axvline(pd.Timestamp('1971-08-15'), color=GREY, lw=0.5, ls=':')
    save(fig, 'f1_2_inflazione')
    print(ymax, y[ymax], y2, y[y2])

def fig_2_0():
    r = 0.10
    n = 20
    cum = [1000 * (1 - (1 - r) ** k) / r for k in range(1, n + 1)]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.bar(range(1, n + 1), cum, color=RUST_L, edgecolor=RUST, lw=0.4, width=0.75)
    ax.axhline(10000, color=INK, lw=0.7, ls='--')
    ax.text(n + 0.4, 10150, 'Limite teorico: 10.000 euro', ha='right', va='bottom', fontsize=6.5, color=INK)
    for k in [1, 2, 5, 10, 20]:
        ax.text(k, cum[k - 1] + 180, it(cum[k - 1]), ha='center', fontsize=5.8, color=INK)
    ax.set_ylim(0, 11500)
    ax.set_xlabel('Numero di passaggi (deposito, prestito, nuovo deposito)')
    ax.set_ylabel('Depositi complessivi (euro)')
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.set_xticks([1, 5, 10, 15, 20])
    save(fig, 'f2_0_moltiplicatore')

def fig_3_4():
    v = json.load(open(D + 'imf_GGXWDG_NGDP.json'))['values']['GGXWDG_NGDP']
    items = [('Giappone', 'JPN'), ('Italia', 'ITA'), ('Grecia', 'GRC'), ('Stati Uniti', 'USA'), ('Francia', 'FRA'), ('Cina', 'CHN'), ('Regno Unito', 'GBR'), ('Spagna', 'ESP'), ('Germania', 'DEU')]
    items = sorted([(n, v[c]['2026']) for n, c in items], key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(W, 2.5))
    cols = [RUST if n == 'Stati Uniti' else RUST_L for n, _ in items]
    ax.barh([n for n, _ in items], [x for _, x in items], color=cols, edgecolor=RUST, lw=0.4, height=0.65)
    for i, (n, x) in enumerate(items):
        ax.text(x + 2, i, it(x, 0) + '%', va='center', fontsize=6.5, color=INK)
    ax.set_xlim(0, 235)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('Debito pubblico lordo in percentuale del PIL, stime 2026')
    save(fig, 'f3_4_debito_paesi')

def fig_4_3():
    def P(q, z):
        p = 1 - q
        lam = z * q / p
        s = 1.0
        for k in range(0, z + 1):
            pois = math.exp(-lam) * lam ** k / math.factorial(k)
            s -= pois * (1 - (q / p) ** (z - k))
        return s
    zs = list(range(0, 13))
    fig, ax = plt.subplots(figsize=(W, 2.5))
    for q, col in [(0.10, BLUE), (0.30, RUST), (0.40, INK)]:
        ys = [max(P(q, z), 1e-9) if z > 0 else 1.0 for z in zs]
        ax.plot(zs, ys, color=col, lw=1.2, marker='o', ms=2.5, label=f'{int(q*100)}%')
    ax.set_yscale('log')
    ax.set_ylim(1e-5, 1.6)
    ax.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: ('100%' if v == 1 else it(v * 100, 3 if v < 1e-3 else (2 if v < 1e-2 else (1 if v < 1e-1 else 0))) + '%')))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, p: ''))
    ax.set_xlim(0, 12.5)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel('Conferme ricevute dalla transazione (blocchi successivi)')
    ax.set_ylabel("Probabilità di riuscita dell'attacco (log)")
    ax.axvline(6, color=GREY, lw=0.5, ls=':')
    ax.text(6.15, 1.2e-3, '6 conferme,\ncirca un\'ora', fontsize=6, color=GREY)
    ax.legend(title="Potenza di calcolo\ndell'attaccante", loc='lower right', title_fontsize=6.3)
    save(fig, 'f4_3_attacco')

def fig_4_4():
    lam = 1 / 10
    edges = [0, 1, 5, 10, 20, 30, 60, 1e9]
    labs = ['meno di\n1 min', '1-5', '5-10', '10-20', '20-30', '30-60', 'oltre\n1 ora']
    sh = [(math.exp(-lam * a) - math.exp(-lam * b)) * 100 for a, b in zip(edges[:-1], edges[1:])]
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ax.bar(labs, sh, color=RUST_L, edgecolor=RUST, lw=0.4, width=0.7)
    for i, s in enumerate(sh):
        ax.text(i, s + 0.8, it(s, 1) + '%', ha='center', fontsize=6.3, color=INK)
    ax.set_ylim(0, 36)
    ax.set_ylabel('Quota dei blocchi (%)')
    ax.set_xlabel('Minuti tra un blocco e il successivo (distribuzione teorica)')
    ax.grid(axis='x', visible=False)
    save(fig, 'f4_4_intervalli')
    print(sh)

def fig_5_0():
    p = price()['2010-07-18':'2015-12-31']
    fig, ax = plt.subplots(figsize=(W, 2.8))
    ax.plot(p.index, p.values, color=INK, lw=0.8)
    ax.set_yscale('log')
    ax.set_ylim(0.04, 3000)
    ax.set_yticks([0.1, 1, 10, 100, 1000])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, q: it(v, 1) if v < 1 else it(v, 0)))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, q: ''))
    ax.set_ylabel('Dollari per bitcoin (scala log)')
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ev = [('2011-06-08', '2011: fino a 30\ne poi 2', '2010-12-01', 120),
          ('2013-03-01', 'Cipro,\nmarzo 2013', '2012-08-01', 90),
          ('2013-11-29', '1.000 dollari,\nnovembre 2013', '2012-12-01', 1500),
          ('2014-02-24', 'Fallimento di\nMt. Gox', '2015-03-01', 1500),
          ('2014-12-15', 'Minimo\ndel 2015', '2015-09-01', 50)]
    for d, lab, tx, ty in ev:
        t = pd.Timestamp(d)
        v = float(p.asof(t))
        ax.plot([t], [v], 'o', color=RUST, ms=3.5)
        ax.annotate(lab, xy=(t, v), xytext=(pd.Timestamp(tx), ty), fontsize=6, ha='center', color=INK, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.4))
    save(fig, 'f5_0_prezzo_2010_2015')

def fig_6_3():
    cyc = ['2013', '2017', '2021', '2025']
    h2p = []
    hal = ['2012-11-28', '2016-07-09', '2020-05-11', '2024-04-20']
    pk = ['2013-11-29', '2017-12-17', '2021-11-10', '2025-10-06']
    for a, b in zip(hal, pk):
        h2p.append((pd.Timestamp(b) - pd.Timestamp(a)).days / 30.44)
    p2t = [410 / 30.44, 363 / 30.44, 376 / 30.44, 268 / 30.44]
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.bar(x - 0.19, h2p, 0.36, color=INK, label='Dal halving al massimo')
    ax.bar(x + 0.19, p2t, 0.36, color=RUST, label='Dal massimo al minimo')
    for i in range(4):
        ax.text(x[i] - 0.19, h2p[i] + 0.3, it(h2p[i], 0), ha='center', fontsize=6.3)
        ax.text(x[i] + 0.19, p2t[i] + 0.3, it(p2t[i], 0), ha='center', fontsize=6.3)
    ax.set_xticks(x)
    ax.set_xticklabels([f'Ciclo del {c}' for c in cyc])
    ax.set_ylabel('Mesi')
    ax.set_ylim(0, 24)
    ax.grid(axis='x', visible=False)
    ax.legend(loc='upper right', ncol=1)
    save(fig, 'f6_3_halving_cicli')
    print(h2p, p2t)


def fig_5_2_new():
    labs = ['novembre 2025\n(30 giorni)', 'dicembre 2025\n(31 giorni)', '1 gen - 13 lug 2026\n(194 giorni)', '14 lug - 24 set 2026\n(73 giorni)']
    tot = [-3.48, -1.09, -5.69, 6.58]
    days = [30, 31, 194, 73]
    vals = [t * 1000 / d for t, d in zip(tot, days)]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    cols = [RUST if v < 0 else INK for v in vals]
    ax.bar(range(4), vals, color=cols, width=0.55)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xticks(range(4)); ax.set_xticklabels(labs, fontsize=6.0)
    ax.set_ylim(-155, 125)
    ax.set_ylabel('Milioni di dollari al giorno')
    ax.grid(axis='x', visible=False)
    for i, v in enumerate(vals):
        lab = ('+' if v > 0 else '') + it(v, 0) + '\n(' + ('+' if tot[i] > 0 else '') + it(tot[i], 2) + ' mld)'
        ax.text(i, v + (6 if v >= 0 else -6), lab, ha='center', va='bottom' if v >= 0 else 'top', fontsize=6.3)
    save(fig, 'f5_2_flussi_etf')

def fig_8_pool():
    items = [('Foundry USA', 28.3), ('AntPool', 18.1), ('F2Pool', 12.5), ('ViaBTC', 9.8), ('SpiderPool', 8.9), ('MARA Pool', 5.0), ('SECPOOL', 4.2), ('Tutti gli altri', 13.2)]
    items = items[::-1]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    cols = [LIGHT if n == 'Tutti gli altri' else RUST_L for n, _ in items]
    ax.barh([n for n, _ in items], [v for _, v in items], color=cols, edgecolor=RUST, lw=0.4, height=0.65)
    for i, (n, v) in enumerate(items):
        ax.text(v + 0.5, i, it(v, 1) + '%', va='center', fontsize=6.5)
    ax.set_xlim(0, 34)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('Quota dei blocchi trovati negli ultimi 12 mesi (%)')
    save(fig, 'f8_0_pool')

if __name__ == '__main__':
    for f in [fig_8_pool, fig_5_2_new, fig_1_1, fig_1_2, fig_2_0, fig_3_4, fig_4_3, fig_4_4, fig_5_0, fig_6_3]:
        f()
