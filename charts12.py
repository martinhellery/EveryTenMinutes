from common import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

END_C, HYB_C, EXO_C = '#F3DDD2', '#D6E3EC', '#ECEAE5'


def fig_19_1():
    fig, ax = plt.subplots(figsize=(W, 3.9))
    ax.set_xlim(0, 100); ax.set_ylim(-4, 100); ax.axis('off')
    rows = [  # y, livello, titolo, [(nome, tipo)]
        (86, '4', 'Ambiente globale', [('Macroeconomia: liquidità, tassi,\ndebito, regole', 'exo')]),
        (68, '3', 'Infrastruttura finanziaria', [('Piatta-\nforme', 'hyb'), ('Derivati', 'hyb'), ('Fondi e\nistituzioni', 'hyb'), ('Lightning', 'hyb'), ('Informa-\nzione', 'hyb')]),
        (50, '2', 'Reti native', [('Miner', 'end'), ('Nodi', 'end'), ('Utenti', 'end'), ('Possessori', 'end')]),
        (32, '1', 'Protocollo', [('Consenso, emissione, registro', 'end')]),
        (10, '0', 'Fisica', [('Energia e semiconduttori', 'exo')]),
    ]
    col = {'end': END_C, 'hyb': HYB_C, 'exo': EXO_C}
    x0, x1 = 36, 100
    for y, lv, tit, boxes in rows:
        ax.text(0, y + 2.2, f'Livello {lv}', fontsize=5.8, color=GREY, va='center')
        ax.text(0, y - 2.6, tit, fontsize=6.4, color=INK, va='center', fontweight='bold' if lv == '1' else 'normal')
        n = len(boxes); gap = 1.4; w = (x1 - x0 - gap * (n - 1)) / n
        for i, (nm, t) in enumerate(boxes):
            bx = x0 + i * (w + gap)
            ec = RUST if lv == '1' else 'none'
            ax.add_patch(FancyBboxPatch((bx, y - 6), w, 12, boxstyle='round,pad=0,rounding_size=1.2', fc=col[t], ec=ec, lw=1.0))
            ax.text(bx + w / 2, y, nm, ha='center', va='center', fontsize=(5.0 if n > 4 else 5.7) if n > 3 else 6.2, color=INK, linespacing=1.05)
    # annotations
    ax.text(0, 60.6, 'qui si forma il prezzo', fontsize=5.4, color=BLUE, style='italic')
    ax.text(0, 24.6, 'cambia solo con un\naccordo vastissimo', fontsize=5.4, color=RUST, style='italic', va='top', linespacing=1.05)
    # legend
    ly = -3.5
    for i, (lab, t) in enumerate([('nasce con Bitcoin', 'end'), ('ibrida', 'hyb'), ('esterna', 'exo')]):
        lx = [36, 64, 80][i]
        ax.add_patch(FancyBboxPatch((lx, ly), 3.2, 3.2, boxstyle='round,pad=0,rounding_size=0.5', fc=col[t], ec='none'))
        ax.text(lx + 4.4, ly + 1.6, lab, fontsize=5.6, va='center', color=INK)
    save(fig, 'f19_1_mappa')


def fig_19_2():
    # anelli: tre circuiti che attraversano i livelli
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.set_xlim(0, 100); ax.set_ylim(0, 72); ax.axis('off')
    loops = [
        ('Sicurezza', ['prezzo', 'ricavi dei\nminer', 'potenza di\ncalcolo', 'costo di\nun attacco', 'fiducia'], RUST),
        ('Adozione', ['prezzo', 'nuovi\nutenti', 'mercati più\nprofondi', 'nuovi\npossessori', 'fiducia'], BLUE),
        ('Leva', ['calo del\nprezzo', 'liquidazioni', 'vendite\nforzate', 'nuovo\ncalo', ''], GREY),
    ]
    for r, (name, steps, c) in enumerate(loops):
        y = 64 - r * 24
        ax.text(0, y, name, fontsize=6.6, color=c, fontweight='bold', va='center')
        steps = [s for s in steps if s]
        n = len(steps); xs = [26 + i * (68 / (n - 1)) for i in range(n)]
        for i, (x, s) in enumerate(zip(xs, steps)):
            ax.text(x, y, s, ha='center', va='center', fontsize=5.8, color=INK, linespacing=1.05,
                    bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=c, lw=0.6))
            if i < n - 1:
                ax.annotate('', xy=(xs[i + 1] - 7.2, y), xytext=(x + 7.2, y), arrowprops=dict(arrowstyle='-|>', color=c, lw=0.7, mutation_scale=6))
        ax.annotate('', xy=(xs[0], y - 7.5), xytext=(xs[-1], y - 7.5), arrowprops=dict(arrowstyle='-|>', color=c, lw=0.6, ls=(0, (2, 1.5)), mutation_scale=6, connectionstyle='arc3,rad=-0.08'))
        ax.text((xs[0] + xs[-1]) / 2, y - 12.5, 'e il circuito ricomincia' if name != 'Leva' else 'finché non si esaurisce la leva', ha='center', fontsize=5.2, color=c, style='italic')
    save(fig, 'f19_2_anelli')


if __name__ == '__main__':
    fig_19_1(); fig_19_2()
