import datetime

from oslib2.fonte_de_dados_mt import mt5
from oslib2 import fonte_de_dados_mt as fdm
from oslib2 import selecao as sel

def buscar_features_e_retornar_as_correlacionadas(dt=None, qtd=60, timeframe=fdm.TIMEFRAME_DEFAULT, symbols_group='Forex'):
    """Busca e seleciona features"""
    # tickers = ['EURUSD','GBPUSD','AUDUSD','NZDUSD','EURCHF','NZDCHF','AUDCHF','EURGBP','AUDCAD','GBPCHF','CADCHF','AUDNZD','EURCAD','NZDCAD','EURNZD','AUDJPY','NZDJPY','GBPNZD','GBPCAD','EURJPY','CADJPY','EURAUD','GBPJPY','CHFJPY','GBPAUD','USDCHF','USDJPY','USDCAD']
    print("Buscando features...")
    tickers_list = fdm.get_symbols_list(symbols_group)

    print("Buscando dados...")
    tickers_data = fdm.get_all_ticker_data(tickers_list, dt=dt, qtd=qtd, timeframe=timeframe, verbose=True)
    tickers_data.to_excel("dados_tickers_mt5_ICMarkets.xlsx")

    print("Calculando correlação...")
    return tickers_data.corr()


if __name__ == '__main__':

    print("Conectando ao MT5...")
    fdm.conectar_mt5('desen')

    corr = buscar_features_e_retornar_as_correlacionadas()

    print("Salvando correlação...")
    corr.to_excel("correlacao_tickers_mt5_ICMarkets.xlsx")

    print(corr)
