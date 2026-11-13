# Ogni dieci minuti: dati e calcoli

Questo pacchetto accompagna il libro *Ogni dieci minuti. Bitcoin, il debito e il futuro del denaro* di Martin Hellery. Contiene gli script con cui sono stati prodotti i grafici e i calcoli dell'autore, il campione di blocchi costruito per il capitolo 4 e le istruzioni per scaricare le serie di terzi. Le serie storiche, i grafici e le analisi del libro sono aggiornati al 4 ottobre 2026, tranne i grafici del prezzo di Bitcoin (figure 6.1, 6.2, 7.1, 7.3 e 9.2), estesi al 12 novembre 2026. `scarica_dati.py` scarica le serie fino all'ultimo dato disponibile: rieseguendo gli script, le figure che nel libro si fermano a ottobre o a novembre possono mostrare qualche settimana in più.

## Che cosa c'è e che cosa no

| Cartella o file | Contenuto |
|---|---|
| `book/common.py` | Stile dei grafici e funzioni di lettura delle serie (`price`, `fred`, `oro`) |
| `book/prep.py` | Costruisce la serie dei prezzi giornalieri `book/price_daily.csv` |
| `book/charts1.py` ... `charts12.py` | Un file per gruppo di figure (vedi la tabella sotto) |
| `book/analysis.py` | Controlli numerici di supporto |
| `work/runes.py`, `oprsize.py`, `tx_sample.py` | Lettura dei blocchi da mempool.space e classificazione delle transazioni |
| `work/runes_sample.json`, `oprsize.json`, `tx_sample.json` | Risultati del campione di blocchi, ricavati dal registro pubblico di Bitcoin |
| `scarica_dati.py` | Scarica le serie di terzi nelle cartelle attese |

Le serie di terzi (FRED, Coin Metrics, mempool.space, Fondo monetario internazionale) **non sono incluse**, perché i loro termini d'uso non sempre ne permettono la ridistribuzione. `scarica_dati.py` le scarica dalle fonti pubbliche. I fornitori rivedono i dati nel tempo, quindi alcuni valori possono differire di poco da quelli stampati.

## Come si usa

Servono Python 3.10 o successivo con `pandas`, `numpy` e `matplotlib`. I grafici usano il carattere Inter; se non è installato, matplotlib ne usa un altro.

```
python3 scarica_dati.py
cd book
python3 prep.py
python3 charts1.py      # e così via fino a charts12.py
```

Le figure vengono scritte in `book/fig/`.

Alcune serie vanno preparate a mano, perché le fonti non offrono un file diretto:

- **Prezzo dell'oro**: file `data/oro.csv` con due colonne, data e prezzo in dollari per oncia, da una fonte a scelta. Nel libro è il future COMEX sul contratto più vicino. Il pacchetto non lo scarica perché le fonti ufficiali richiedono una registrazione o una licenza (per il prezzo LBMA, una licenza di ICE Benchmark Administration). Lo usano due figure: senza il file, la 7.4 esce senza la barra dell'oro e la 16.1 non viene generata.
- **S&P 500 e dollaro**: vengono da FRED (serie `SP500` e `DTWEXBGS`). Per il dollaro il libro usa l'indice DXY; il pacchetto usa l'indice ampio del dollaro della Federal Reserve, gratuito, che pesa più valute: i valori della figura 7.4 per il dollaro differiscono da quelli stampati.
- **Quote delle valute nelle riserve (COFER, FMI)**: interfaccia SDMX del Fondo monetario internazionale, rilevazione COFER, quote percentuali per valuta, annuali e trimestrali dal 2020. File attesi: `data/cofer_annual_shares.csv` e `data/cofer_quarterly_shares_2020_2026.csv` (colonne: periodo, valuta, quota).
- **Inflazione argentina e cambio**: INDEC e Banco Central de la República Argentina (usate solo nel testo, non nei grafici).
- **M3 dell'area euro**: Banca centrale europea, Data Portal (usata solo nel testo).

## Figure e script

| Figura | File | Script |
|---|---|---|
| 1.1, 1.2 | f1_1_potere_acquisto, f1_2_inflazione | charts3.py |
| 2.1 | f2_0_moltiplicatore | charts3.py |
| 3.1 | f2_1_debito_fed | charts1.py |
| 3.2 | f3_4_debito_paesi | charts3.py |
| 3.3 | f14_1_interessi | charts2.py |
| 3.4 | f2_2_emissione_m2 | charts1.py |
| 4.1, 4.2 | f4_4_intervalli, f4_3_attacco | charts3.py |
| 4.3, 4.4 | f3_1_emissione, f3_2_hashrate | charts1.py |
| 5.1 | f5_0_prezzo_2010_2015 | charts3.py |
| 6.1, 6.2 | f4_1_prezzo_cicli, f4_2_drawdown | charts1.py |
| 6.3 | f6_3_halving_cicli | charts3.py |
| 7.1, 7.2, 7.3 | f5_1_prezzo_2025_26, f5_2_flussi_etf, f5_3_prezzo_tasso_reale | charts1.py |
| 7.4 | f9_2_rendimenti | charts2.py |
| 8.1 | f8_0_pool | charts3.py |
| 8.2 | f11_1_commissioni | charts2.py |
| 9.1, 9.2, 9.3 | f9_1_chi_detiene, f9_2_strategy, f9_3_governi | charts4.py |
| 10.1, 10.2, 11.1 | f10_1_sentenze, f10_2_energia, f11_2_furti | charts5.py |
| 11.2 | f11_1_quota_dollaro (identica a f9_1_quota_dollaro) | charts2.py |
| 12.1, 12.2, 12.3 | f12_1_washington, f12_2_europa, f12_3_mappa | charts6.py |
| 13.1, 13.2 | f7_2_stock_to_flow, f7_1_legge_di_potenza | charts2.py |
| 13.3, 13.4 | f13_4_errori, f13_3_code_grasse | charts7.py |
| 14.1, 14.3 | f14_2_x402, f14_3_hashrate | charts8.py |
| 14.2 | f13_1_strati (schema, non da dati) | charts2.py |
| 15.1, 15.2 | f12_1_coordinamento, f12_2_simulazione | charts2.py |
| 16.1 | f16_1_prova | charts9.py |
| 16.2 | f14_2_prezzo_implicito | charts2.py |
| 17.1, 17.2 | f17_1_scenari, f17_2_sicurezza | charts10.py |
| 18.1 | f18_1_tasso_reale | charts11.py |
| 19.1, 19.2 | f19_1_mappa, f19_2_anelli (schemi, senza dati) | charts12.py |

Le figure costruite su dati raccolti a mano dai documenti citati nelle note (sentenze, furti, mappe delle istituzioni, chi detiene bitcoin, pagamenti x402) hanno i valori scritti direttamente negli script, con la fonte indicata nel libro.

## Formule e scelte principali

**Prezzo giornaliero.** Coin Metrics (`PriceUSD`) fino al 22 maggio 2026, poi la serie Coinbase di FRED (`CBBTCUSD`). Prezzi di chiusura in dollari; massimi e minimi intragiornalieri citati nel testo vengono da fonti di mercato.

**Probabilità di attacco (cap. 4).** Formula della sezione 11 del whitepaper. Con q la quota dell'attaccante, p = 1 − q, z le conferme e λ = z·q/p:
P = 1 − Σ_{k=0..z} (e^(−λ) λ^k / k!) · (1 − (q/p)^(z−k)).
Per z = 6: 0,0002428 con q = 0,1; 0,132 con q = 0,3; 0,504 con q = 0,4.

**Campione di blocchi (cap. 4 e 8).** Un blocco ogni 400 tra le altezze 930.540 e 969.740 (gennaio-ottobre 2026), 99 blocchi, 393.249 transazioni. Quota Runes = transazioni con un'uscita OP_RETURN che inizia con il marcatore Runes (OP_13) / totale delle transazioni del campione (ponderata per numero di transazioni: 53,6%). Media semplice delle quote per blocco: 46,4%. Intervallo: bootstrap con 5.000 ricampionamenti dei blocchi con reinserimento, percentili 2,5 e 97,5 (circa 46,6-60,5%).

**Stock-to-flow (cap. 13).** Regressione ln(capitalizzazione) = a + b · ln(S2F), con S2F = monete esistenti (Coin Metrics `SplyCur`) / (emissione media giornaliera degli ultimi 30 giorni × 365), stimata sui dati dal 1° ottobre 2010 al 22 marzo 2019, poi proiettata in avanti.

**Legge di potenza (cap. 13 e 17).** log10(prezzo) = a + b · log10(giorni dal 3 gennaio 2009), minimi quadrati sui prezzi giornalieri dal 2011 (b ≈ 5,5). La fascia è ± due deviazioni standard dei residui; non è un intervallo di previsione. Prova fuori campione: stessa stima con i dati fino al 22 marzo 2019.

**Code della distribuzione (cap. 13).** Rendimenti logaritmici giornalieri dal 1° gennaio 2014, standardizzati con media e deviazione standard dell'intero periodo. Conteggio dei giorni oltre 3 e 4 deviazioni standard, confrontato con il valore atteso di una normale (n · P(|Z| > k)).

**Modello di soglie (cap. 15).** Una quota ε di persone ha soglia zero; le altre hanno soglie distribuite come una Beta(a, b). La curva è F(x) = ε + (1 − ε) · BetaCDF(x; a, b), cioè la quota di persone con soglia inferiore all'adozione corrente x; gli equilibri sono le intersezioni con la diagonale. Parametri illustrativi, scritti nello script.

**Correlazioni e volatilità (cap. 16).** Rendimenti settimanali semplici (ultima chiusura disponibile di ogni settimana terminante il venerdì) dal 31 dicembre 2024 al 2 ottobre 2026; correlazione di Pearson su finestre mobili di 26 settimane; volatilità annualizzata = deviazione standard settimanale × √52.

**Prezzo implicito rispetto all'oro (cap. 16 e 17).** Prezzo = quota × valore dell'oro / monete in circolazione. Valore dell'oro: 222.600 tonnellate (World Gold Council, fine giugno 2026) × 32.150,7 once per tonnellata × prezzo dell'oro del 2 ottobre 2026 ≈ 29.800 miliardi di dollari. Monete: 20,09 milioni oggi, 20,91 milioni al 1° gennaio 2040.

**Bilancio della sicurezza (cap. 17).** Sussidio annuo = ricompensa per blocco × 52.560 blocchi × prezzo costante di 85.000 dollari; dimezzamenti stimati ad aprile 2028, aprile 2032, marzo 2036 e marzo 2040.

**Tasso reale della Federal Reserve (cap. 18).** FEDFUNDS meno la variazione sui dodici mesi di CPIAUCNS, dati mensili da gennaio 1955.

**Conversione in dollari di oggi (cap. 17).** Valori nominali del 2040 divisi per 1,03^(anni dal 2026), ipotesi di inflazione del 3 per cento annuo.

## Licenza

Gli script e il campione di blocchi possono essere usati e modificati liberamente, citando il libro. Le serie scaricate restano soggette ai termini dei rispettivi fornitori.

## Il foglio degli scenari (capitolo 17)

`scenari_cap17.xlsx` ricostruisce la Tabella 17.1 con formule visibili: valore dell'oro, calendario di emissione fino al 2040 (circa 20,91 milioni di monete) e prezzo di ogni scenario come quota dell'oro moltiplicata per il suo valore e divisa per le monete. Cambiando le ipotesi nelle celle B4, B5 e nelle colonne delle quote si ricalcola tutto.

## Licenza

Il codice è distribuito con licenza MIT, il foglio di calcolo, questo README e i risultati del campione con licenza CC BY 4.0. I dettagli sono nel file `LICENSE`.
