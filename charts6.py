from common import *
from matplotlib.patches import Rectangle
import textwrap


def lane_chart(lanes, events, xlim, key, name, figh, future_from=None, future_label=None, year_step=1):
    """lanes: list of lane names top to bottom. events: (n, date, lane_idx, dy, hollow)."""
    fig = plt.figure(figsize=(W, figh))
    nk = len(key)
    key_h = 0.105 * nk + 0.35
    ax = fig.add_axes([0.2, key_h / figh + 0.02, 0.78, 1 - key_h / figh - 0.04])
    n = len(lanes)
    ax.set_ylim(-0.6, n - 0.4)
    ax.invert_yaxis()
    ax.set_xlim(pd.Timestamp(xlim[0]), pd.Timestamp(xlim[1]))
    ax.set_yticks(range(n))
    ax.set_yticklabels(lanes, fontsize=6.4)
    ax.grid(axis='y', visible=False)
    ax.grid(axis='x', color=LIGHT, lw=0.4)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.xaxis.set_major_locator(mdates.YearLocator(year_step))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    for i in range(n):
        ax.axhline(i, color=LIGHT, lw=0.8, zorder=0)
    if future_from:
        ax.axvspan(pd.Timestamp(future_from), pd.Timestamp(xlim[1]), color='#F4F1EA', zorder=0)
        ax.text(pd.Timestamp(future_from) + pd.Timedelta(days=60), n - 0.5, future_label, fontsize=5.8, color=GREY,
                va='bottom', ha='left', style='italic')
    for num, d, lane, dy, hollow in events:
        t = pd.Timestamp(d)
        ax.plot([t], [lane + dy], 'o', ms=8.2, mfc='white' if hollow else RUST, mec=RUST, mew=0.8, zorder=3)
        ax.text(t, lane + dy, str(num), fontsize=5.6, ha='center', va='center_baseline',
                color=RUST if hollow else 'white', zorder=4, fontweight='bold')
    # key
    for k, txt in enumerate(key):
        row = k
        x = 0.01
        y = (key_h - 0.3 - row * 0.105) / figh
        fig.text(x, y, f'{k + 1}', fontsize=5.8, color=RUST, fontweight='bold', va='top', ha='left')
        fig.text(x + 0.035, y, txt, fontsize=5.8, color=INK, va='top', ha='left')
    save(fig, name)


def fig_12_1():
    lanes = ['Casa Bianca', 'Congresso', 'SEC e CFTC', 'Federal Reserve', 'Stati federati']
    events = [
        (1, '2025-01-23', 0, -0.17, False), (2, '2025-03-06', 0, 0.17, False),
        (3, '2025-07-18', 1, 0, False), (4, '2026-09-15', 1, -0.2, False), (5, '2026-09-16', 1, 0.2, False),
        (6, '2024-01-10', 2, 0, False), (7, '2026-08-18', 2, 0, False),
        (8, '2025-04-24', 3, 0, False), (9, '2025-08-15', 3, 0, False), (10, '2026-05-22', 3, 0, False),
        (11, '2025-11-20', 4, 0, False),
    ]
    key = [
        'Gen 2025: ordine contro un dollaro digitale pubblico',
        'Mar 2025: ordine sulla riserva strategica, senza acquisti',
        'Lug 2025: firmato il GENIUS Act sulle stablecoin',
        'Set 2026: CLARITY Act, voto in Senato fallito 49 a 50',
        'Set 2026: ARMA approvata in commissione, 28 a 21',
        'Gen 2024: i primi fondi spot su bitcoin (SEC)',
        'Ago 2026: la SEC propone la Regulation Crypto Assets',
        'Apr 2025: la Fed ritira le linee guida sulle cripto',
        'Ago 2025: la Fed chiude il programma di vigilanza speciale',
        'Mag 2026: Kevin Warsh presidente della Fed',
        'Nov 2025: il Texas compra 5 milioni di dollari di IBIT',
    ]
    lane_chart(lanes, events, ('2023-11-01', '2026-12-31'), key, 'f12_1_washington', 3.6)


def fig_12_2():
    lanes = ['Regole UE\n(MiCA)', 'BCE', 'Parlamento e\nConsiglio UE']
    events = [
        (1, '2024-06-30', 0, -0.18, False), (2, '2024-12-30', 0, 0.18, False), (3, '2026-07-01', 0, 0, False),
        (4, '2025-01-30', 1, -0.18, False), (5, '2025-10-30', 1, 0.18, False),
        (6, '2027-09-30', 1, -0.18, True), (7, '2029-06-30', 1, 0.18, True),
        (8, '2025-12-15', 2, -0.18, False), (9, '2026-02-10', 2, 0.18, False),
    ]
    key = [
        'Giu 2024: MiCA si applica alle stablecoin',
        'Dic 2024: MiCA si applica ai fornitori di servizi',
        'Lug 2026: finisce il periodo transitorio',
        'Gen 2025: Lagarde esclude bitcoin dalle riserve',
        'Ott 2025: la BCE passa alla fase successiva dell\'euro digitale',
        'Seconda metà 2027: pilota dell\'euro digitale (previsto)',
        '2029: prima emissione, se la legge sarà approvata (previsto)',
        'Dic 2025: il Consiglio sostiene limiti alla detenzione',
        'Feb 2026: il Parlamento a favore dell\'euro digitale',
    ]
    lane_chart(lanes, events, ('2024-01-01', '2030-01-01'), key, 'f12_2_europa', 3.0,
               future_from='2026-10-04', future_label='previsioni', year_step=1)


def fig_12_3():
    cols = ['Riserve in bitcoin', 'Accesso dei risparmiatori', 'Moneta digitale pubblica']
    rows = [
        ('Casa Bianca', [('Ordine, nessun acquisto', 1), ('Favorevole', 2), ('Contraria', 0)]),
        ('Congresso', [('Proposte, nessuna legge', 1), ('GENIUS sì, CLARITY ferma', 1), ('Nessuna legge a favore', 0)]),
        ('SEC e CFTC', [('Non competenti', None), ('Regole in preparazione', 2), ('Non competenti', None)]),
        ('Federal Reserve', [('Non può comprare', 0), ('Vincoli ridotti', 2), ('Contrario il presidente', 0)]),
        ('BCE', [('Esclusa', 0), ('Cauta', 1), ('Favorevole', 2)]),
    ]
    colr = {0: '#D9D4CA', 1: RUST_L, 2: RUST, None: 'white'}
    txtc = {0: INK, 1: INK, 2: 'white', None: GREY}
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.set_xlim(0, 3.0)
    ax.set_ylim(len(rows) + 0.5, -0.8)
    ax.axis('off')
    for j, c in enumerate(cols):
        ax.text(j + 0.5, -0.4, textwrap.fill(c, 20), ha='center', va='center', fontsize=6.4, fontweight='bold', color=INK)
    for i, (rn, cells) in enumerate(rows):
        ax.text(-0.04, i + 0.5, rn, ha='right', va='center', fontsize=6.4, color=INK)
        for j, (t, v) in enumerate(cells):
            ax.add_patch(Rectangle((j + 0.03, i + 0.05), 0.94, 0.9, fc=colr[v], ec='white' if v is not None else LIGHT, lw=0.6))
            ax.text(j + 0.5, i + 0.5, textwrap.fill(t, 17), ha='center', va='center', fontsize=5.7, color=txtc[v], linespacing=1.15)
    # legend
    ly = len(rows) + 0.25
    for k, (lab, v) in enumerate([('chiusa o contraria', 0), ('ambigua', 1), ('aperta o favorevole', 2)]):
        x0 = 0.0 + k * 1.0
        ax.add_patch(Rectangle((x0, ly), 0.09, 0.2, fc=colr[v], ec='none', clip_on=False))
        ax.text(x0 + 0.14, ly + 0.1, lab, fontsize=5.9, va='center', color=INK)
    ax.set_xlim(-0.75, 3.0)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 'f12_3_mappa')


if __name__ == '__main__':
    fig_12_1(); fig_12_2(); fig_12_3()
