import pandas_datareader as web

def baixar_dados_ccy(tickers=None, start="2020-12-18"):
    ccy_tickers = ['DEXJPUS', 'DEXUSUK']
    if tickers:
        ccy_tickers = tickers
    return web.DataReader(ccy_tickers, 'fred', start)


def baixar_dados_idx(tickers=None, start="2020-12-18"):
    idx_tickers = ['SP500', 'DJIA', 'VIXCLS']
    if tickers:
        idx_tickers = tickers
    return web.DataReader(idx_tickers, 'fred', start)