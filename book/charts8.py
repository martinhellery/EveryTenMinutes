from common import *
import json


def fig_14_2():
    fig, ax = plt.subplots(figsize=(W, 1.7))
    items = [('Volume x402 dichiarato\n(mag 2025 - set 2026)', 52.7, INK), ('Dopo la pulizia di test,\nauto-pagamenti e flussi in blocco', 25.6, RUST)]
    ys = [1, 0]
    for y, (n, v, c) in zip(ys, items):
        ax.barh(y, v, color=c, height=0.5)
        ax.text(v + 1, y, it(v, 1) + ' milioni di dollari', va='center', fontsize=6.5)
    ax.set_yticks(ys); ax.set_yticklabels([n for n, _, _ in items], fontsize=6.3)
    ax.set_xlim(0, 80)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('Pagamenti con il protocollo x402 (milioni di dollari)')
    save(fig, 'f14_2_x402')


def fig_14_3():
    j = json.load(open(SP + 'hr_all.json'))
    h = pd.DataFrame(j['hashrates'])
    h['t'] = pd.to_datetime(h['timestamp'], unit='s').dt.normalize()
    s = h.set_index('t')['avgHashrate'] / 1e18
    s = s[~s.index.duplicated()]
    s = s['2025-01-01':].rolling(7, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(s.index, s.values, color=INK, lw=0.9)
    ax.set_ylim(500, 1300)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(it_month_fmt())
    ax.set_ylabel('Potenza della rete (exahash al secondo)')
    pk = s['2025-09-01':'2025-12-31']
    pt = pk.idxmax()
    ax.plot([pt], [pk.max()], 'o', color=RUST, ms=3.5)
    ax.annotate('massimo, circa %s EH/s' % it(round(pk.max(), -1)), xy=(pt, pk.max()), xytext=(pd.Timestamp('2025-02-20'), 1230), fontsize=6.3, color=RUST,
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.4))
    ax.plot([s.index[-1]], [s.iloc[-1]], 'o', color=RUST, ms=3.5)
    ax.text(s.index[-1] + pd.Timedelta(days=5), 790, 'oggi\ncirca %s' % it(round(s.iloc[-1], -1)), fontsize=6.3, color=RUST, ha='right', va='top')
    ax.plot([s.index[-1]] * 2, [s.iloc[-1] - 15, 800], color=GREY, lw=0.4)
    for d, lab, y in [('2026-07-06', 'TeraWulf e Anthropic\n(6 luglio)', 640), ('2026-08-11', 'Riot e Anthropic\n(11 agosto)', 560)]:
        t = pd.Timestamp(d)
        ax.axvline(t, color=GREY, lw=0.5, ls=':')
    ax.text(pd.Timestamp('2026-07-02'), 600, 'contratti con\nAnthropic\n(6 lug, 11 ago)', fontsize=5.8, color=GREY, ha='right', va='center')
    print(s.iloc[-1], pk.max(), pt)
    save(fig, 'f14_3_hashrate')


if __name__ == '__main__':
    fig_14_2(); fig_14_3()
