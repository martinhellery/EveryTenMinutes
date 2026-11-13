from common import *

# ---------- Fig 2.1 debito federale USA e bilancio Fed ----------
def fig_2_1():
    debt = fred('GFDEBTN') / 1e6  # trilioni
    debt = debt['2000-01-01':]
    fed = fred('WALCL') / 1e6
    fed = fed['2003-01-01':]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(debt.index, debt.values, color=RUST, lw=1.4)
    ax.plot(fed.index, fed.values, color=INK, lw=1.1, ls='--')
    ax.set_ylim(0, 42)
    ax.set_ylabel('Trilioni di dollari')
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.text(debt.index[-1], debt.values[-1] + 1.5, 'Debito federale USA\n39,5', color=RUST, ha='right', va='bottom', fontsize=6.5, fontweight='bold')
    ax.text(pd.Timestamp('2026-06-01'), 10.3, 'Bilancio della Fed\n(massimo 8,97 ad aprile 2022)', color=INK, ha='right', va='bottom', fontsize=6.5)
    for dt, lab in [('2008-09-15', 'Lehman'), ('2020-03-15', 'Covid')]:
        ax.axvline(pd.Timestamp(dt), color=GREY, lw=0.5, ls=':')
        ax.text(pd.Timestamp(dt), 41, lab, rotation=0, ha='center', va='top', fontsize=6, color=GREY,
                bbox=dict(fc='white', ec='none', pad=0.5))
    save(fig, 'f2_1_debito_fed')


# ---------- Fig 2.2 emissione Bitcoin vs crescita M2 ----------
def fig_2_2():
    c = cm()
    iss = c['IssTotNtv']
    sup = c['SplyCur']
    rate = (iss.rolling(30).mean() * 365 / sup * 100)['2013-02-01':'2026-05-20']
    m2 = fred('M2SL')
    yoy = (m2.pct_change(12) * 100).dropna()['2012-12-01':]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(rate.index, rate.values, color=RUST, lw=1.5)
    ax.plot(yoy.index, yoy.values, color=INK, lw=1.1, ls='--')
    ax.axhline(0, color=INK, lw=0.5)
    ax.set_ylim(-6, 28)
    ax.set_yticks([-5, 0, 5, 10, 15, 20, 25])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v) + '%'))
    ax.set_ylabel('Crescita annua dell\'offerta')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.text(pd.Timestamp('2013-03-01'), 17.2, 'Nuovi bitcoin, in percentuale\ndello stock esistente', color=RUST, fontsize=6.5, fontweight='bold', va='bottom')
    ax.text(pd.Timestamp('2021-10-01'), 15.5, 'Moneta M2 negli USA\n(variazione sui 12 mesi)', color=INK, fontsize=6.5, ha='left', va='bottom')
    for dt in ['2016-07-09', '2020-05-11', '2024-04-20']:
        ax.axvline(pd.Timestamp(dt), color=GREY, lw=0.4, ls=':')
    ax.text(pd.Timestamp('2024-04-20'), 27.5, 'halving 2024 ', fontsize=5.8, color=GREY, ha='right', va='top')
    save(fig, 'f2_2_emissione_m2')


# ---------- Fig 3.1 curva di emissione ----------
def fig_3_1():
    # schedule teorica
    years = []
    supply = []
    reward = 50.0
    total = 0.0
    blocks_per_epoch = 210000
    t0 = pd.Timestamp('2009-01-03')
    # approx anno per blocco: usa halving reali e poi 4 anni
    halv = [pd.Timestamp('2009-01-03'), pd.Timestamp('2012-11-28'), pd.Timestamp('2016-07-09'),
            pd.Timestamp('2020-05-11'), pd.Timestamp('2024-04-20')]
    # epoche future ogni ~4 anni
    for k in range(5, 34):
        halv.append(halv[-1] + pd.Timedelta(days=int(210000 * 10 / 60 / 24)))
    xs = []
    ys = []
    cum = 0.0
    for k in range(len(halv) - 1):
        r = 50.0 / (2 ** k)
        n = 210000
        for f in np.linspace(0, 1, 30, endpoint=False):
            xs.append(halv[k] + (halv[k + 1] - halv[k]) * f)
            ys.append((cum + r * n * f) / 1e6)
        cum += r * n
    xs.append(halv[-1]);
    ys.append(cum / 1e6)
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(xs, ys, color=RUST, lw=1.5)
    ax.set_ylim(0, 22)
    ax.set_xlim(pd.Timestamp('2009-01-01'), pd.Timestamp('2142-01-01'))
    ax.axhline(21, color=GREY, lw=0.6, ls=':')
    ax.text(pd.Timestamp('2141-01-01'), 21.3, 'Tetto: 21 milioni', ha='right', va='bottom', fontsize=6.5, color=INK)
    ax.set_ylabel('Bitcoin emessi (milioni)')
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.xaxis.set_major_locator(mdates.YearLocator(20))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # oggi
    today = pd.Timestamp('2026-10-04')
    ax.plot([today], [20.09], 'o', color=INK, ms=4)
    ax.annotate('Oggi: 20,09 milioni\n(95,7% del totale)', xy=(today, 20.09), xytext=(pd.Timestamp('2050-01-01'), 11.5),
                fontsize=6.5, color=INK, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5), ha='left')
    # 90% rimasto
    ax.text(pd.Timestamp('2012-06-01'), 3.0, '50% del totale\nentro il 2012', fontsize=6, color=GREY, ha='left')
    ax.text(pd.Timestamp('2094-01-01'), 18.3, 'L\'ultimo bitcoin intorno al 2140', fontsize=6, color=GREY, ha='center')
    save(fig, 'f3_1_emissione')


# ---------- Fig 3.2 hashrate ----------
def fig_3_2():
    c = cm()
    h = (c['HashRate'].dropna() / 1e6)  # TH/s -> EH/s
    h = h['2012-01-01':].rolling(14).mean()
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.plot(h.index, h.values, color=RUST, lw=1.3)
    ax.set_yscale('log')
    ax.set_ylim(1e-4, 3e3)
    ax.set_yticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v, 3 if v < 0.01 else (2 if v < 0.1 else (1 if v < 1 else 0)))))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, p: ''))
    ax.set_ylabel('Exahash al secondo (scala log)')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.annotate('Massimo: circa 1.150\nad ottobre 2025', xy=(pd.Timestamp('2025-10-25'), 1100), xytext=(pd.Timestamp('2018-08-01'), 450),
                fontsize=6.5, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5))
    ax.plot([pd.Timestamp('2026-10-04')], [0.92 * 1000], 'o', mfc='white', mec=INK, ms=3.5)
    ax.text(pd.Timestamp('2026-08-01'), 300, 'ottobre 2026:\ncirca 920', ha='right', va='top', fontsize=6, color=INK)
    save(fig, 'f3_2_hashrate')


# ---------- Fig 4.1 prezzo log con cicli ----------
def fig_4_1():
    p = price()
    p = p[p > 0.5]
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.plot(p.index, p.values, color=INK, lw=0.8)
    ax.set_yscale('log')
    ax.set_ylim(0.5, 400000)
    ax.set_yticks([1, 10, 100, 1000, 10000, 100000])
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, p: ''))
    ax.set_ylabel('Dollari per bitcoin (scala log)')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    peaks = [('2011-06-08', 31, '2011'), ('2013-12-04', 1135, '2013'), ('2017-12-16', 19641, '2017'),
             ('2021-11-08', 67542, '2021'), ('2025-10-06', 124824, '2025')]
    troughs = [('2011-11-18', 2.3), ('2015-01-14', 170), ('2018-12-15', 3200), ('2022-11-09', 15758), ('2026-06-30', 58586)]
    for dt, v, lab in peaks:
        ax.plot([pd.Timestamp(dt)], [v], 'o', color=RUST, ms=3.5)
        ax.text(pd.Timestamp(dt), v * 1.5, lab, color=RUST, fontsize=6.5, ha='center', va='bottom', fontweight='bold')
    for dt, v in troughs:
        ax.plot([pd.Timestamp(dt)], [v], 'o', mfc='white', mec=INK, ms=3.5)
    save(fig, 'f4_1_prezzo_cicli')


# ---------- Fig 4.2 drawdown ----------
def fig_4_2():
    p = price()
    p = p['2011-01-01':]
    dd = (p / p.cummax() - 1) * 100
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.fill_between(dd.index, dd.values, 0, color=RUST_L, lw=0)
    ax.plot(dd.index, dd.values, color=RUST, lw=0.7)
    ax.set_ylim(-100, 3)
    ax.set_xlim(pd.Timestamp('2010-09-01'), pd.Timestamp('2027-03-01'))
    ax.set_yticks([0, -20, -40, -60, -80, -100])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v) + '%'))
    ax.set_ylabel('Distanza dal massimo precedente')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    marks = [('2011-11-18', -92.7, '-93%', 'c'), ('2015-01-14', -84.5, '-85%', 'c'), ('2018-12-15', -83.8, '-84%', 'r'),
             ('2022-11-09', -76.7, '-77%', 'c'), ('2026-06-30', -53.1, '-54%', 'l')]
    for dt, v, lab, al in marks:
        ax.text(pd.Timestamp(dt), v - 3.5, lab, ha='center' if al == 'c' else ('right' if al == 'r' else 'center'),
                va='top', fontsize=6.5, fontweight='bold', color=INK)
    save(fig, 'f4_2_drawdown')


# ---------- Fig 5.1 prezzo 2025-26 con eventi ----------
def fig_5_1():
    p = price()['2025-09-20':]
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.plot(p.index, p.values / 1000, color=INK, lw=0.9)
    ax.set_ylim(40, 140)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, q: it(v) + 'k'))
    ax.set_ylabel('Migliaia di dollari per bitcoin')
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(it_month_fmt())
    ev = [
        ('2025-10-06', 1, 'up'), ('2025-10-10', 2, 'down'), ('2026-02-05', 3, 'down'),
        ('2026-02-28', 4, 'up'), ('2026-05-22', 5, 'up'), ('2026-07-01', 6, 'down'), ('2026-09-16', 7, 'up')
    ]
    for dt, n, d in ev:
        t = pd.Timestamp(dt)
        v = p.asof(t) / 1000
        off = 8 if d == 'up' else -9
        ax.annotate(str(n), xy=(t, v), xytext=(t, v + off), ha='center', va='center', fontsize=6.5, color='white', fontweight='bold',
                    bbox=dict(boxstyle='circle,pad=0.25', fc=RUST, ec='none'),
                    arrowprops=dict(arrowstyle='-', color=RUST, lw=0.6, shrinkA=3, shrinkB=0))
    save(fig, 'f5_1_prezzo_2025_26')


# ---------- Fig 5.2 flussi ETF ----------
def fig_5_2():
    months = ['ott\n2025', 'nov', 'dic', 'gen\n2026', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set']
    vals = [3.4, -3.5, -1.1, -1.6, -0.21, 1.3, 2.0, -2.4, -4.5, 0.17, 3.5, 2.65]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    cols = [INK if v >= 0 else RUST for v in vals]
    ax.bar(range(len(vals)), vals, color=cols, width=0.65)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(months, fontsize=6.3)
    ax.set_ylim(-5.6, 4.6)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, q: it(v, 0)))
    ax.set_ylabel('Miliardi di dollari')
    ax.grid(axis='x', visible=False)
    for i, v in enumerate(vals):
        ax.text(i, v + (0.2 if v >= 0 else -0.2), it(v, 1), ha='center', va='bottom' if v >= 0 else 'top', fontsize=6)
    save(fig, 'f5_2_flussi_etf')


# ---------- Fig 5.3 prezzo vs tasso reale ----------
def fig_5_3():
    p = price()['2025-09-20':] / 1000
    ry = fred('DFII10')['2025-09-20':]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(W, 3.3), sharex=True, gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.12})
    a1.plot(p.index, p.values, color=INK, lw=0.9)
    a1.set_ylabel('Bitcoin\n(migliaia di dollari)')
    a1.set_ylim(40, 135)
    a2.plot(ry.index, ry.values, color=RUST, lw=1.1)
    a2.set_ylabel('Rendimento reale\nUSA a 10 anni (%)')
    a2.set_ylim(1.4, 3.1)
    a2.yaxis.set_major_formatter(FuncFormatter(lambda v, q: it(v, 1)))
    a2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    a2.xaxis.set_major_formatter(it_month_fmt())
    save(fig, 'f5_3_prezzo_tasso_reale')


if __name__ == '__main__':
    for f in [fig_2_1, fig_2_2, fig_3_1, fig_3_2, fig_4_1, fig_4_2, fig_5_1, fig_5_2, fig_5_3]:
        f()
