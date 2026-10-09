import datetime

from oslib2.data.fonte_de_dados_mt import mt5
from oslib2.data import fonte_de_dados_mt as fdm
from oslib2.data import selecao as sel

def buscar_features(dt=None, qtd=60, timeframe=fdm.TIMEFRAME_DEFAULT, symbols_group=None):
    """Busca e seleciona features"""
    print("Buscando features...")
    return fdm.get_symbol_info(categ=symbols_group)

if __name__ == '__main__':

    print("Conectando ao MT5...")
    fdm.conectar_mt5('modal')

    df_ativos = buscar_features()
    df_ativos.to_excel("tickers_mt5_b3.xlsx")

