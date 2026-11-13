from common import *
from matplotlib.patches import Rectangle

GOLD = 29.8e12
SUPPLY40 = 20.911e6


def fig_17_1():
    sc = [
        ("1  L'oro lento", 0.05, 0.12, RUST),
        ("2  L'ancora addomesticata", 0.12, 0.30, RUST),
        ("3  La prova superata", 0.30, 0.70, RUST),
        ("4  Il rifugio mancato", 0.01, 0.03, GREY),
    ]
    fig, ax = plt.subplots(figsize=(W, 2.55))
    ax.set_xscale('log')
    ax.set_xlim(8e3, 4e6)
    n = len(sc)
    ax.set_ylim(n - 0.35, -0.95)
    ax.grid(axis='y', visible=False)
    ax.set_yticks(range(n))
    ax.set_yticklabels([s[0] for s in sc], fontsize=6.6)
    ax.tick_params(axis='y', length=0)
    ax.spines['left'].set_visible(False)
    for i, (lab, lo, hi, col) in enumerate(sc):
        pl, ph = lo * GOLD / SUPPLY40, hi * GOLD / SUPPLY40
        ax.add_patch(Rectangle((pl, i - 0.28), ph - pl, 0.56, fc=col, ec='none', alpha=0.9 if col == RUST else 0.8))
        txt = f"{it(round(pl, -3))} – {it(round(ph, -3))}".replace('.000', '.000')
        if i == 2:
            ax.text(pl * 0.9, i, txt, va='center', ha='right', fontsize=6.2, color=INK, bbox=dict(fc='white', ec='none', pad=0.8), zorder=5)
            ax.text(pl * 0.9, i + 0.3, f"{it(lo*100)}–{it(hi*100)}% dell'oro", va='center', ha='right', fontsize=5.4, color=GREY, bbox=dict(fc='white', ec='none', pad=0.8), zorder=5)
        else:
            ax.text(ph * 1.12, i, txt, va='center', fontsize=6.2, color=INK, bbox=dict(fc='white', ec='none', pad=0.8), zorder=5)
            ax.text(ph * 1.12, i + 0.3, f"{it(lo*100)}–{it(hi*100)}% dell'oro", va='center', fontsize=5.4, color=GREY, bbox=dict(fc='white', ec='none', pad=0.8), zorder=5)
    ax.axvline(71000, color=INK, lw=0.7, ls=(0, (3, 2)))
    ax.text(71000 * 0.93, -0.62, '12 nov. 2026\n71.000', ha='right', va='center', fontsize=5.8, color=INK, linespacing=1.1)
    full = GOLD / SUPPLY40
    ax.axvline(full, color=BLUE, lw=0.7, ls=(0, (3, 2)))
    ax.text(full * 0.94, 3.05, "tutto l'oro\nal 2 ott. 2026", ha='right', va='center', fontsize=5.8, color=BLUE, linespacing=1.1)
    ax.plot([1.91e6], [-0.62], marker='>', color=RUST, ms=4, clip_on=False)
    ax.text(1.91e6 * 0.9, -0.62, "retta della legge di potenza\n(in dollari di oggi, inflazione 3%)", ha='right', va='center', fontsize=5.8, color=RUST, linespacing=1.1, bbox=dict(fc='white', ec='none', pad=0.8), zorder=6)
    ax.set_xticks([1e4, 1e5, 1e6])
    ax.xaxis.set_major_formatter(fmt_axis(0))
    ax.xaxis.set_minor_formatter(FuncFormatter(lambda v, q: ''))
    ax.set_xlabel('Dollari di oggi per bitcoin al 1° gennaio 2040 (scala logaritmica)')
    save(fig, 'f17_1_scenari')


def fig_17_2():
    price0 = 85000
    ep = [('2026-28', 3.125), ('2028-32', 1.5625), ('2032-36', 0.78125), ('2036-40', 0.390625), ('dal 2040', 0.1953125)]
    mc = 20.09e6 * price0
    vals = [r * 52560 * price0 / 1e9 for _, r in ep]
    fig, ax = plt.subplots(figsize=(W, 2.35))
    xs = np.arange(len(ep))
    ax.bar(xs, vals, color=RUST, width=0.6)
    fees = 0.08
    ax.plot([-0.4, len(ep) - 0.6], [fees, fees], color=BLUE, lw=0.9, ls=(0, (3, 2)))
    ax.text(0.98, 0.9, 'linea tratteggiata: commissioni\nnel 2026, circa 0,08 miliardi', transform=ax.transAxes, ha='right', va='top', fontsize=5.9, color=BLUE, linespacing=1.2)
    for x, v, (_, r) in zip(xs, vals, ep):
        ax.text(x, v + 0.3, f"{it(v, 1)}", ha='center', va='bottom', fontsize=6.6, color=INK, fontweight='bold')
        ax.text(x, v + 1.55, f"{it(r*52560/20.09e6*100, 2)}% del valore", ha='center', va='bottom', fontsize=5.5, color=GREY)
    ax.set_xticks(xs)
    ax.set_xticklabels([e[0] for e in ep])
    ax.set_ylim(0, 17.5)
    ax.grid(axis='x', visible=False)
    ax.set_ylabel('Miliardi di dollari l\'anno')
    ax.set_xlabel('Periodo tra due dimezzamenti (date approssimate)')
    print(vals)
    save(fig, 'f17_2_sicurezza')


if __name__ == '__main__':
    fig_17_1(); fig_17_2()
