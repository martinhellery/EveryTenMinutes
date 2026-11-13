from common import *

def fig_9_1():
    items = [('ETF spot USA', 1290304), ('Strategy', 847666), ('Altre società quotate', 1275684 - 847666),
             ('Governi (stima)', 645587), ('di cui El Salvador', 7794)]
    sup = 20093418
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ys = list(range(len(items)))[::-1]
    for y, (n, v) in zip(ys, items):
        col = RUST if n.startswith('ETF') else (INK if n == 'Strategy' else (BLUE if n.startswith('Governi') else GREY))
        ax.barh(y, v / 1e6, color=col, height=0.6)
        lab = f"{it(v / 1e6, 2) if v > 100000 else it(v / 1e6, 3)} milioni  ({it(v / sup * 100, 1 if v > 100000 else 2)}%)"
        ax.text(v / 1e6 + 0.02, y, lab, va='center', fontsize=6.3)
    ax.set_yticks(ys)
    ax.set_yticklabels([n for n, _ in items])
    ax.set_xlim(0, 1.95)
    ax.set_xlabel('Milioni di bitcoin (tra parentesi, quota dei 20,09 milioni in circolazione)')
    ax.grid(axis='y', visible=False)
    ax.xaxis.set_major_formatter(fmt_axis(1))
    save(fig, 'f9_1_chi_detiene')

def fig_9_2():
    h = [('2025-09-28', 640031), ('2025-12-28', 672497), ('2026-02-01', 713502), ('2026-03-08', 738731),
         ('2026-03-31', 762099), ('2026-05-03', 818334), ('2026-05-31', 843706), ('2026-06-14', 846842),
         ('2026-06-28', 847363), ('2026-07-05', 843775), ('2026-08-09', 840447), ('2026-08-30', 845050),
         ('2026-09-27', 847666)]
    d = [pd.Timestamp(a) for a, _ in h]; v = [b / 1000 for _, b in h]
    p = price()['2025-09-28':]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(W, 3.4), sharex=True, gridspec_kw={'height_ratios': [1, 1.2], 'hspace': 0.12})
    a1.step(d, v, where='post', color=INK, lw=1.3)
    a1.plot(d, v, 'o', color=INK, ms=2.2)
    a1.set_ylim(600, 880)
    a1.set_ylabel('Migliaia di BTC')
    a1.yaxis.set_major_formatter(fmt_axis(0))
    a1.annotate('847.666\n(27 settembre)', xy=(d[-1], v[-1]), xytext=(pd.Timestamp('2026-07-10'), 690), fontsize=6.3,
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5))
    a1.annotate('Prime vendite dal 2022\n(da fine maggio 2026)', xy=(pd.Timestamp('2026-06-14'), 846), xytext=(pd.Timestamp('2025-10-25'), 790), fontsize=6.3,
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5))
    a2.plot(p.index, p.values / 1000, color=RUST, lw=1.0)
    a2.axhline(75.437, color=INK, lw=0.7, ls='--')
    a2.annotate('Costo medio di Strategy:\n75.437 dollari', xy=(pd.Timestamp('2026-07-01'), 75.437), xytext=(pd.Timestamp('2026-05-25'), 108), fontsize=6.3, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.5))
    a2.set_ylabel('Prezzo (migliaia di $)')
    a2.set_ylim(50, 135)
    a2.yaxis.set_major_formatter(fmt_axis(0))
    a2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    a2.xaxis.set_major_formatter(it_month_fmt())
    save(fig, 'f9_2_strategy')

def fig_9_3():
    items = [('Stati Uniti', 328372), ('Cina', 190000), ('Regno Unito', 61245), ('Ucraina', 46351),
             ('El Salvador', 7794), ('Emirati Arabi', 6420), ('Kazakistan', 3544), ('Corea del Nord', 803), ('Bhutan', 518)]
    items = items[::-1]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.barh([n for n, _ in items], [v / 1000 for _, v in items], color=BLUE, height=0.62, alpha=0.85)
    for i, (n, v) in enumerate(items):
        ax.text(v / 1000 + 5, i, it(v / 1000, 0 if v >= 10000 else 1) + ' mila', va='center', fontsize=6.3)
    ax.set_xlim(0, 400)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('Migliaia di bitcoin (stime, molto incerte per Cina, Regno Unito e Ucraina)')
    save(fig, 'f9_3_governi')

if __name__ == '__main__':
    for f in [fig_9_1, fig_9_2, fig_9_3]:
        f()
