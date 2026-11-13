"""Scarica le serie di terzi usate nel libro "Ogni dieci minuti".

Le serie non sono incluse nel pacchetto perché appartengono ai rispettivi
fornitori (FRED, Coin Metrics, mempool.space, FMI): questo
script le scarica dalle fonti pubbliche nelle cartelle che gli script si
aspettano. I valori possono differire di poco da quelli del libro, perché
le fonti rivedono i dati nel tempo. Il libro usa i dati al 4 ottobre 2026,
tranne i grafici del prezzo (figure 6.1, 6.2, 7.1, 7.3 e 9.2), estesi al
12 novembre 2026. Il prezzo dell'oro non viene scaricato: vedi il README.

Uso:  python3 scarica_dati.py
"""
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')
UA = {'User-Agent': 'Mozilla/5.0'}

FRED = ['A091RC1Q027SBEA', 'CBBTCUSD', 'CPIAUCNS', 'CPIAUCSL', 'DCOILBRENTEU',
        'DFEDTARL', 'DFEDTARU', 'DFII10', 'DGS10', 'DTWEXBGS', 'FEDFUNDS',
        'FGEXPND', 'FGRECPT', 'FPCPITOTLZGARG', 'FPCPITOTLZGEUU', 'FPCPITOTLZGTUR',
        'FYGFDPUN', 'FYOINT', 'FYONET', 'GDP', 'GDPA', 'GFDEBTN', 'GFDEGDQ188S',
        'IRLTLT01DEM156N', 'IRLTLT01FRM156N', 'IRLTLT01GBM156N', 'IRLTLT01ITM156N',
        'IRLTLT01JPM156N', 'M2SL', 'MABMM301EZM189S', 'MORTGAGE30US', 'MTSO133FMS',
        'NASDAQ100', 'NASDAQCOM', 'RESBALNS', 'SP500', 'T10YIE', 'TOTRESNS', 'WALCL']

def get(url, headers=UA):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60).read()
        except Exception as e:  # rete instabile: riprova
            print('  riprovo', url, e)
            time.sleep(3 * (i + 1))
    raise RuntimeError(url)


def save(path, data):
    with open(path, 'wb') as f:
        f.write(data)
    print('ok', os.path.relpath(path, ROOT))


def main():
    os.makedirs(DATA, exist_ok=True)
    for sid in FRED:
        save(os.path.join(DATA, sid + '.csv'),
             # FRED chiude la connessione se la richiesta si presenta come browser
             get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + sid, headers={}))
    save(os.path.join(ROOT, 'btc_cm.csv'),
         get('https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv'))
    save(os.path.join(ROOT, 'hr_all.json'),
         get('https://mempool.space/api/v1/mining/hashrate/all'))
    save(os.path.join(DATA, 'imf_GGXWDG_NGDP.json'),
         get('https://www.imf.org/external/datamapper/api/v1/GGXWDG_NGDP'))
    print('\nSerie da preparare a mano (vedi README): COFER (quote delle valute '
          'nelle riserve), prezzo dell\'oro (data/oro.csv), inflazione argentina INDEC, '
          'cambio ARS, M3 BCE.')


if __name__ == '__main__':
    main()
