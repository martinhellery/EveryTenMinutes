from common import *

def fig_10_1():
    p = price()['2015-01-01':]
    ev = [(1, '2017-10-13', 1.9), (2, '2017-12-20', 2.0), (3, '2018-02-02', 0.22), (4, '2018-05-05', 0.07),
          (5, '2022-02-16', 2.0), (6, '2022-11-30', 0.22), (7, '2024-01-10', 0.22), (8, '2024-02-22', 2.0)]
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.plot(p.index, p.values, color=RUST, lw=0.9)
    ax.set_yscale('log')
    ax.set_ylim(150, 400000)
    ax.set_yticks([1000, 10000, 100000])
    ax.yaxis.set_major_formatter(fmt_axis(0))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, q: ''))
    ax.set_ylabel('Prezzo in dollari (scala logaritmica)')
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    for n, d, f in ev:
        t = pd.Timestamp(d); y = p.asof(t)
        ax.plot([t], [y], 'o', color=INK, ms=2.5)
        ax.annotate(str(n), xy=(t, y), xytext=(t, y * (6 if f > 1 and n != 2 else (14 if n == 2 else f))), fontsize=6.5, ha='center', va='center',
                    color=INK, bbox=dict(boxstyle='circle,pad=0.2', fc='white', ec=GREY, lw=0.5),
                    arrowprops=dict(arrowstyle='-', color=GREY, lw=0.4))
    last = p.iloc[-1]
    ax.plot([p.index[-1]], [last], 'o', color=RUST, ms=3)
    ax.text(p.index[-1] - pd.Timedelta(days=120), last * 1.6, '84.800', fontsize=6.3, ha='right', color=RUST)
    save(fig, 'f10_1_sentenze')

def fig_10_2():
    items = [('Rete Bitcoin, Cambridge\n(anno 2024)', 138, 'ink'), ('Rete Bitcoin, Cambridge\n(stima del 4 ottobre 2026)', 158, 'ink'),
             ('Rete Bitcoin, Digiconomist\n(giugno 2025)', 204, 'rust'),
             ('Tutti i data center\ndel mondo, 2024 (IEA)', 415, 'blue'), ('Tutti i data center,\nprevisione IEA per il 2030', 945, 'blue_p')]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ys = list(range(len(items)))[::-1]
    for y, (n, v, c) in zip(ys, items):
        col = {'ink': INK, 'rust': RUST, 'blue': BLUE, 'blue_p': 'white'}[c]
        ax.barh(y, v, color=col, height=0.55, edgecolor=BLUE if c == 'blue_p' else col, lw=0.8, hatch='////' if c == 'blue_p' else None)
        ax.text(v + 12, y, it(v) + ' TWh' + (' (intervallo 81-304)' if v == 158 else ''), va='center', fontsize=6.5)
    ax.set_yticks(ys); ax.set_yticklabels([n for n, _, _ in items], fontsize=6.3)
    ax.set_xlim(0, 1150)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('Consumo annuo di elettricità (terawattora)')
    save(fig, 'f10_2_energia')

if __name__ == '__main__':
    fig_10_1(); fig_10_2()

def fig_11_2():
    fig, ax = plt.subplots(figsize=(W, 1.9))
    ax.barh(1, 2300, color=LIGHT, edgecolor=GREY, lw=0.4, height=0.5)
    ax.text(2300 + 40, 1, '2.300 milioni (totale)', va='center', fontsize=6.3)
    segs = [(285, INK, 'Drift\n285'), (292, '#4A4A4A', 'Kelp\n292'), (66, GREY, ''), (329, RUST_L, 'Altri\n329')]
    x = 0
    for v, c, lab in segs:
        ax.barh(0, v, left=x, color=c, height=0.5, edgecolor='white', lw=0.6)
        if lab:
            ax.text(x + v / 2, 0, lab, ha='center', va='center', fontsize=5.8, color='white' if c != RUST_L else INK)
        x += v
    ax.text(x + 40, 0, '972 milioni (totale)', va='center', fontsize=6.3)
    ax.annotate('Attribuiti alla Corea del Nord: 643 milioni (66%)', xy=(321, -0.28), xytext=(30, -0.62), fontsize=6.2, ha='left',
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.4))
    ax.plot([0, 643], [-0.3, -0.3], color=INK, lw=1.0)
    ax.set_yticks([0, 1]); ax.set_yticklabels(['Primo semestre 2026', 'Primo semestre 2025'], fontsize=6.3)
    ax.set_xlim(0, 2900); ax.set_ylim(-0.85, 1.5)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('Milioni di dollari rubati in attacchi informatici al settore delle cripto')
    ax.xaxis.set_major_formatter(fmt_axis(0))
    save(fig, 'f11_2_furti')

if __name__ == '__main__':
    fig_11_2()
