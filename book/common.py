import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')) + '/'
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

SP = _ROOT
D = SP + 'data/'
OUT = SP + 'book/fig/'

INK = '#1F1F1F'
GREY = '#7A7A7A'
LIGHT = '#E6E1D8'
RUST = '#B5451B'
RUST_L = '#E9C3B0'
BLUE = '#2B5C7D'

plt.rcParams.update({
    'font.family': 'Inter',
    'font.size': 7,
    'axes.edgecolor': GREY,
    'axes.linewidth': 0.5,
    'axes.labelcolor': INK,
    'axes.titlesize': 7.5,
    'xtick.color': INK,
    'ytick.color': INK,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 2.5,
    'ytick.major.size': 2.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'legend.frameon': False,
    'legend.fontsize': 6.5,
    'axes.grid': True,
    'grid.color': LIGHT,
    'grid.linewidth': 0.5,
    'axes.axisbelow': True,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

W = 3.95  # inches, text block width


def it(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fmt_axis(dec=0, suffix=''):
    return FuncFormatter(lambda v, p: it(v, dec) + suffix)


def price():
    s = pd.read_csv(SP + 'book/price_daily.csv', index_col=0, parse_dates=True)['price']
    return s


def cm():
    return pd.read_csv(SP + 'btc_cm.csv', parse_dates=['time']).set_index('time')


def fred(name):
    df = pd.read_csv(D + name + '.csv', parse_dates=[0], index_col=0)
    s = pd.to_numeric(df.iloc[:, 0], errors='coerce').dropna()
    return s


def oro():
    """Prezzo dell'oro in dollari per oncia da data/oro.csv (colonne: data, prezzo).
    Il file non viene scaricato da scarica_dati.py: vedi il README. Se manca, None."""
    path = D + 'oro.csv'
    if not _os.path.exists(path):
        print("manca data/oro.csv: le parti che usano l'oro vengono saltate (vedi README)")
        return None
    df = pd.read_csv(path, parse_dates=[0], index_col=0)
    return pd.to_numeric(df.iloc[:, 0], errors='coerce').dropna()


def save(fig, name):
    fig.savefig(OUT + name + '.png', bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)
    print('saved', name)


IT_M = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']


def it_month_fmt():
    return FuncFormatter(lambda v, p: IT_M[mdates.num2date(v).month - 1] + '\n' + str(mdates.num2date(v).year))
