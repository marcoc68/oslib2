
import yfinance as yf
def baixar_dados_ibv (tickers=None, start="2024-12-18"):
    ''' Baixa os dados de uma lista de tickers do IBV'''
    ibv_tickers = ['^BVSP',
    # 'BRPR3.SA',
    # 'ELET3.SA',
    # 'EMBR3.SA',
    'CMIG4.SA',
    # 'CPLE6.SA',
    'BBAS3.SA',
    'BBDC4.SA',
    'BBDC3.SA',
    'BBSE3.SA',
    'CPFE3.SA',
    'ABEV3.SA',
    'CSNA3.SA',
    'BRAP4.SA',
    'CYRE3.SA',
    'BRKM5.SA',
    'GGBR4.SA',
    'ECOR3.SA',
    'EQTL3.SA',
    'CSAN3.SA']
    if tickers:
        ibv_tickers = tickers
    return yf.download(ibv_tickers, start)['Close']


