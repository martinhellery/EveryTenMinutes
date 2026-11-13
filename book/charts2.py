from common import *
from scipy import stats

GEN = pd.Timestamp('2009-01-03')


# ---------- Fig 7.1 legge di potenza ----------
def fig_7_1():
    p = price()['2011-01-01':]
    d = (p.index - GEN).days.values
    x = np.log10(d)
    y = np.log10(p.values)
    b, a = np.polyfit(x, y, 1)
    res = y - (a + b * x)
    sd = res.std()
    xs = np.linspace(x.min(), np.log10((pd.Timestamp('2035-12-31') - GEN).days), 200)
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.plot(x, p.values, color=INK, lw=0.6)
    ax.plot(xs, 10 ** (a + b * xs), color=RUST, lw=1.5)
    ax.fill_between(xs, 10 ** (a + b * xs - 2 * sd), 10 ** (a + b * xs + 2 * sd), color=RUST_L, alpha=0.55, lw=0)
    ax.set_yscale('log')
    ax.set_ylim(0.5, 5e6)
    ax.set_yticks([1, 100, 1e4, 1e6])
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, q: ''))
    yrs = [2012, 2016, 2020, 2024, 2030]
    ax.set_xticks([np.log10((pd.Timestamp(f'{yy}-07-01') - GEN).days) for yy in yrs])
    ax.set_xticklabels([str(yy) for yy in yrs])
    ax.set_ylabel('Dollari per bitcoin (scala log)')
    xe = np.log10((pd.Timestamp('2035-06-01') - GEN).days)
    ax.text(xe, 10 ** (a + b * xe + 2 * sd) * 1.5, 'fascia a 2 deviazioni standard', fontsize=6, color=RUST, ha='right', va='bottom')
    ax.plot([x[-1]], [p.values[-1]], 'o', color=INK, ms=3.5)
    ax.text(np.log10((pd.Timestamp('2013-06-01') - GEN).days), 3e4, 'linea della\nlegge di potenza', fontsize=6.5, color=RUST, fontweight='bold', ha='left')
    print('power law slope %.3f R2 %.3f sd %.3f' % (b, 1 - res.var() / y.var(), sd))
    save(fig, 'f7_1_legge_di_potenza')
    return a, b, sd


# ---------- Fig 7.2 stock to flow ----------
def fig_7_2():
    c = cm()
    sup = c['SplyCur']
    iss = c['IssTotNtv']
    flow = iss.rolling(30).mean() * 365
    sf = (sup / flow)
    p = price()[:'2026-05-22']
    mc = p * sup.reindex(p.index)
    df = pd.concat([np.log(sf), np.log(mc)], axis=1, keys=['lsf', 'lmc']).dropna()
    df = df['2010-10-01':]
    tr = df[:'2019-03-22']
    b, a = np.polyfit(tr['lsf'], tr['lmc'], 1)
    pred = np.exp(a + b * df['lsf']) / sup.reindex(df.index)
    fig, ax = plt.subplots(figsize=(W, 2.7))
    ax.plot(df.index, np.exp(df['lmc']) / sup.reindex(df.index), color=INK, lw=0.8)
    ax.plot(df.index, pred, color=RUST, lw=1.3, ls='--')
    ax.set_yscale('log')
    ax.set_ylim(0.1, 5e6)
    ax.set_yticks([1, 100, 1e4, 1e6])
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, q: ''))
    ax.set_ylabel('Dollari per bitcoin (scala log)')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.axvline(pd.Timestamp('2019-03-22'), color=GREY, lw=0.6, ls=':')
    ax.text(pd.Timestamp('2019-02-01'), 2.5e6, 'dati usati per\ncostruire il modello', fontsize=6, color=GREY, ha='right', va='top')
    ax.text(pd.Timestamp('2022-09-01'), 3.5e6, 'previsione del modello', fontsize=6.5, color=RUST, fontweight='bold', ha='center', va='top')
    ax.text(pd.Timestamp('2022-03-01'), 400, 'prezzo reale', fontsize=6.5, color=INK, fontweight='bold', ha='left', va='top')
    print('s2f slope %.3f int %.3f' % (b, a))
    for dt in ['2020-05-12', '2021-11-08', '2024-04-21', '2025-10-06']:
        t = pd.Timestamp(dt)
        r = df.loc[:t].iloc[-1]
        s = sup.asof(t)
        print(dt, 'SF %.1f pred %.0f actual %.0f' % (np.exp(r['lsf']), np.exp(a + b * r['lsf']) / s, np.exp(r['lmc']) / s))
    save(fig, 'f7_2_stock_to_flow')


# ---------- Fig 8.1 chi detiene ----------
def fig_8_1():
    items = [('ETF spot USA', 1290304), ('Strategy', 847666), ('Altre società quotate', 1275684 - 847666),
             ('El Salvador', 7764), ('Bhutan (stima)', 3100)]
    sup = 20093418
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ys = range(len(items))[::-1]
    for y, (n, v) in zip(ys, items):
        ax.barh(y, v / 1e6, color=RUST if n in ('ETF spot USA',) else (INK if n == 'Strategy' else GREY), height=0.6)
        ax.text(v / 1e6 + 0.02, y, f"{it(v / 1e6, 2) if v > 100000 else it(v / 1e6, 3)} milioni  ({it(v / sup * 100, 1 if v > 100000 else 2)}%)", va='center', fontsize=6.3)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([n for n, _ in items])
    ax.set_xlim(0, 1.9)
    ax.set_xlabel('Milioni di bitcoin (tra parentesi, quota dei 20,09 milioni in circolazione)')
    ax.grid(axis='y', visible=False)
    ax.xaxis.set_major_formatter(fmt_axis(1))
    save(fig, 'f8_1_chi_detiene')


# ---------- Fig 9.1 quota dollaro ----------
def fig_9_1():
    df = pd.read_csv(D + 'cofer_annual_shares.csv').set_index('year')
    q = pd.read_csv(D + 'cofer_quarterly_shares_2020_2026.csv')
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(df.index, df['CI_USD'], color=RUST, lw=1.5)
    ax.plot(df.index, df['CI_EUR'], color=INK, lw=1.1, ls='--')
    ax.plot(df.index, df['CI_CNY'], color=GREY, lw=1.0, ls=':')
    ax.set_ylim(0, 75)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v) + '%'))
    ax.set_ylabel('Quota delle riserve ufficiali')
    ax.set_xlim(2000, 2027.5)
    ax.text(2025.8, df['CI_USD'].iloc[-1] - 3.0, 'Dollaro 56,5% (2025)', fontsize=6.5, color=RUST, fontweight='bold', ha='right', va='top')
    ax.text(2000.4, 71, '69,7%', fontsize=6.5, color=RUST, fontweight='bold', va='bottom')
    ax.text(2025.8, df['CI_EUR'].iloc[-1] - 2.2, 'Euro 20,3%', fontsize=6.5, color=INK, ha='right', va='top')
    ax.text(2025.8, df['CI_CNY'].iloc[-1] + 2.2, 'Yuan 2,0%', fontsize=6.5, color=GREY, ha='right', va='bottom')
    save(fig, 'f9_1_quota_dollaro')


# ---------- Fig 9.2 rendimenti ----------
def fig_9_2():
    btc = price()
    gold = oro()
    sp = fred('SP500')
    nq = fred('NASDAQCOM')
    dxy = fred('DTWEXBGS')  # indice ampio del dollaro della Federal Reserve
    def ret(s, a, b):
        s = s.sort_index()
        va = s.asof(pd.Timestamp(a)); vb = s.asof(pd.Timestamp(b))
        return (vb / va - 1) * 100
    # per il 2025 serve il dato di fine dicembre 2024 in ogni serie
    rows = {}
    serie = [('Bitcoin', btc), ('Oro', gold), ('S&P 500', sp), ('Nasdaq', nq), ('Dollaro (indice Fed)', dxy)]
    for name, s in [(n, s) for n, s in serie if s is not None]:
        r25 = ret(s, '2024-12-31', '2025-12-31')
        r26 = ret(s, '2025-12-31', '2026-10-02' if name != 'Bitcoin' else '2026-10-03')
        rows[name] = (r25, r26)
        print(name, round(r25, 1), round(r26, 1))
    names = list(rows.keys())[::-1]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    h = 0.36
    for i, n in enumerate(names):
        ax.barh(i + h / 2, rows[n][0], height=h, color=INK)
        ax.barh(i - h / 2, rows[n][1], height=h, color=RUST)
        ax.text(rows[n][0] + (1.2 if rows[n][0] >= 0 else -1.2), i + h / 2, it(rows[n][0], 1) + '%', va='center', ha='left' if rows[n][0] >= 0 else 'right', fontsize=6)
        ax.text(rows[n][1] + (1.2 if rows[n][1] >= 0 else -1.2), i - h / 2, it(rows[n][1], 1) + '%', va='center', ha='left' if rows[n][1] >= 0 else 'right', fontsize=6)
    ax.axvline(0, color=INK, lw=0.6)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlim(-22, 78)
    ax.grid(axis='y', visible=False)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v) + '%'))
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=INK, label='2025'), Patch(color=RUST, label='2026 (a inizio ottobre)')], loc='lower right')
    save(fig, 'f9_2_rendimenti')
    return rows


# ---------- Fig 11.1 quota commissioni sui ricavi dei minatori ----------
def fig_11_1():
    c = cm()
    fee = c['FeeTotNtv']
    iss = c['IssTotNtv']
    share = (fee.rolling(90).sum() / (fee.rolling(90).sum() + iss.rolling(90).sum()) * 100)['2013-01-01':'2026-05-20']
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.plot(share.index, share.values, color=RUST, lw=1.3)
    ax.set_ylim(0, 40)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v) + '%'))
    ax.set_ylabel('Commissioni sul totale dei ricavi')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    for dt in ['2016-07-09', '2020-05-11', '2024-04-20']:
        ax.axvline(pd.Timestamp(dt), color=GREY, lw=0.4, ls=':')
    mx = share.idxmax()
    print('fee share max', mx.date(), share.max(), 'last', share.iloc[-1])
    save(fig, 'f11_1_commissioni')
    return share


# ---------- Fig 12.1 e 12.2 coordinamento ----------
def F(x, a, b, eps):
    return eps + (1 - eps) * stats.beta.cdf(x, a, b)


def equilibria(a, b, eps):
    xs = np.linspace(0, 1, 100001)
    g = F(xs, a, b, eps) - xs
    idx = np.where(np.sign(g[:-1]) != np.sign(g[1:]))[0]
    res = []
    for i in idx:
        stable = g[i] > 0 and g[i + 1] < 0
        res.append((xs[i], stable))
    return res


def fig_12_1():
    xs = np.linspace(0, 1, 400)
    A = (3.6, 2.6, 0.015)   # soglie alte
    B = (2.6, 3.6, 0.04)    # soglie basse
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.plot([0, 1], [0, 1], color=GREY, lw=0.8, ls=':')
    ax.plot(xs, F(xs, *A), color=INK, lw=1.2, ls='--')
    ax.plot(xs, F(xs, *B), color=RUST, lw=1.5)
    for (par, col) in [(A, INK), (B, RUST)]:
        eq = equilibria(*par)
        print(par, eq)
        for x0, st in eq:
            ax.plot([x0], [x0], 'o', mfc=col if st else 'white', mec=col, ms=4.5, zorder=5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v * 100) + '%'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v * 100) + '%'))
    ax.set_xlabel('Quota di chi già usa o detiene bitcoin')
    ax.set_ylabel('Quota di chi, a quel punto,\nconviene che lo usi')
    ax.text(0.98, 0.30, 'Soglie di adesione alte\n(costo elevato, poca fiducia)', fontsize=6, color=INK, ha='right', va='top')
    ax.text(0.02, 0.97, 'Soglie più basse\n(ETF, regole chiare, custodia semplice)', fontsize=6.3, color=RUST, fontweight='bold', ha='left', va='top')
    ax.text(0.02, 0.83, 'cerchio pieno: equilibrio stabile\ncerchio vuoto: punto di svolta', fontsize=5.8, color=GREY, ha='left', va='top')
    save(fig, 'f12_1_coordinamento')
    return A, B


def fig_12_2():
    rng = np.random.default_rng(11)
    N = 20000
    a, b, eps = 2.6, 3.6, 0.04
    thr = np.where(rng.random(N) < eps, 0.0, rng.beta(a, b, N))
    starts = [0.05, 0.12, 0.20, 0.30, 0.40]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    for s0 in starts:
        adopt = rng.random(N) < s0
        traj = [adopt.mean()]
        for t in range(30):
            share = adopt.mean()
            adopt = thr <= share
            traj.append(adopt.mean())
        col = RUST if traj[-1] > 0.5 else INK
        ax.plot(range(len(traj)), traj, color=col, lw=1.2, ls='-' if traj[-1] > 0.5 else '--')
        ax.text(-0.5, s0, f'{it(s0 * 100)}%', fontsize=5.8, color=col, va='center', ha='right')
        print(s0, round(traj[-1], 3))
    ax.axhline(0.278, color=GREY, lw=0.6, ls=':')
    ax.text(31, 0.29, 'punto di svolta (circa 28%)', fontsize=5.8, color=GREY, ha='right', va='bottom')
    ax.set_xlim(-3, 33)
    ax.set_ylim(0, 1.02)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v * 100) + '%'))
    ax.set_xlabel('Turni di decisione (una simulazione)')
    ax.set_ylabel('Quota di chi adotta')
    save(fig, 'f12_2_simulazione')


# ---------- Fig 13.1 strati ----------
def fig_13_1():
    from matplotlib.patches import FancyBboxPatch
    fig, ax = plt.subplots(figsize=(W, 2.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    boxes = [
        (8.0, 'RISERVA', 'Bitcoin', 'resta nel tempo, non può essere\ncongelato né diluito', RUST),
        (4.6, 'LIQUIDITÀ DI LAVORO', 'Stablecoin e Lightning', 'prezzo stabile o pagamento\nistantaneo per le spese correnti', INK),
        (1.2, 'SPESA REALE', 'Calcolo, energia, dati', 'ciò che l\'agente consuma\nper produrre valore', GREY),
    ]
    for y, t1, t2, t3, col in boxes:
        ax.add_patch(FancyBboxPatch((0.3, y), 9.4, 2.0, boxstyle='round,pad=0.02,rounding_size=0.15', fc='white', ec=col, lw=1.2))
        ax.text(0.7, y + 1.55, t1, fontsize=6, color=col, fontweight='bold', va='center')
        ax.text(0.7, y + 0.95, t2, fontsize=8.5, color=INK, fontweight='bold', va='center')
        ax.text(9.4, y + 1.0, t3, fontsize=6.3, color=INK, ha='right', va='center')
    for y0, y1, lab in [(8.0, 6.7, 'si converte quando serve'), (4.6, 3.3, 'si spende')]:
        ax.annotate('', xy=(5, y1 + 0.05), xytext=(5, y0 - 0.05), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0))
        ax.text(5.3, (y0 + y1) / 2, lab, fontsize=6.3, color=INK, va='center')
    save(fig, 'f13_1_strati')


# ---------- Fig 14.1 interessi sulle entrate ----------
def fig_14_1():
    i = fred('A091RC1Q027SBEA')
    r = fred('FGRECPT')
    q = (i / r * 100).dropna()['1960-01-01':]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(q.index, q.values, color=RUST, lw=1.4)
    ax.set_ylim(0, 30)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: it(v) + '%'))
    ax.set_ylabel('Interessi in % delle entrate federali')
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    mx = q.idxmax()
    print('interest share max', mx.date(), q.max(), 'last', q.iloc[-1], q.index[-1].date())
    ax.plot([q.index[-1]], [q.iloc[-1]], 'o', color=INK, ms=4)
    ax.text(q.index[-1], q.iloc[-1] + 1.6, f'{it(q.iloc[-1], 1)}%\n2° trim. 2026', ha='right', va='bottom', fontsize=6.3, fontweight='bold')
    save(fig, 'f14_1_interessi')
    return q


# ---------- Fig 14.2 prezzo implicito ----------
def fig_14_2():
    gold_cap = 29.8e12
    sup = 20.09e6
    shares = [5.8, 10, 25, 50, 100]
    prices = [s / 100 * gold_cap / sup for s in shares]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ys = range(len(shares))[::-1]
    for y, s, pr in zip(ys, shares, prices):
        ax.barh(y, pr / 1000, color=GREY if s == 5.8 else RUST, height=0.6)
        ax.text(pr / 1000 + 20, y, f'{it(pr / 1000)}.000 dollari' if pr >= 1000 else '', va='center', fontsize=6.3)
        print(s, round(pr))
    ax.set_yticks(list(ys))
    ax.set_yticklabels(['Oggi (5,8%)', '10%', '25%', '50%', '100%'])
    ax.set_xlim(0, 2300)
    ax.set_xlabel('Prezzo implicito per bitcoin, migliaia di dollari')
    ax.set_ylabel('Quota del valore dell\'oro')
    ax.grid(axis='y', visible=False)
    ax.xaxis.set_major_formatter(fmt_axis(0))
    save(fig, 'f14_2_prezzo_implicito')


if __name__ == '__main__':
    fig_7_1(); fig_7_2(); fig_8_1(); fig_9_1(); fig_9_2(); fig_11_1()
    fig_12_1(); fig_12_2(); fig_13_1(); fig_14_1(); fig_14_2()
