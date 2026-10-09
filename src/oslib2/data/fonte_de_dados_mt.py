from typing import Any

import MetaTrader5 as mt5
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

# from sklearn.linear_model import LinearRegression
from statsmodels.tsa.stattools import adfuller

from matplotlib import pyplot
import seaborn as sns

TIMEFRAME_DEFAULT = mt5.TIMEFRAME_M3
SYMBOLS_BLACKLIST = ['USDAED']

def conectar_mt5(local='desen'):
    """Inicializa a conexão com o MetaTrader5 no local especificado."""
    # exibimos dads sobre o pacote MetaTrader5
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # Initializing MT5 connection
    if not mt5.initialize(path=f"D:\\programs\\mt5\\{local}\\terminal64.exe", portable=True):
        print("initialize() failed, error code =",mt5.last_error())
        print("Tentando conectar em uma instancia aberta...")
        if mt5.initialize():
            print("Conectado em uma instancia aberta!")
        else:
            print("Nenhuma instancia aberta encontrada.")
            quit()

    # imprimimos informacoes sobre o estado da conexao, o nome do servidor e a conta de negociacao
    print('MT5 conectado :-)')
    print(mt5.terminal_info())
    print(mt5.version()      )


def get_ticker_data(symbol, dt=None, qtd_barras=60, timeframe=TIMEFRAME_DEFAULT) -> DataFrame | None:
    """Retornamos um dataframe com os preços do ativo desde a data informada...
    A partir da data informada, busca ´qtd´ barras do timeframe informado pra tras."""
    if symbol in SYMBOLS_BLACKLIST:
        print(f"Symbol {symbol} is in the blacklist.")
        return None

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is not None:
        # importamos o módulo pytz para trabalhar com o fuso horário
        import pytz  # definimos o fuso horário como UTC
        timezone = pytz.timezone("Etc/UTC")

        # recebemos qtd barras de symbol a partir de dt no fuso horário UTC. As barras contam desde dt pra tras
        if dt is None:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, qtd_barras)
        else:
            rates = mt5.copy_rates_from(symbol, timeframe, dt, qtd_barras)

        # a partir dos dados recebidos criamos o DataFrame
        rates_frame = pd.DataFrame(rates)
        # convertemos o tempo em segundos para o formato datetime
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
        rates_frame["ticker"] = symbol
        return rates_frame
    return None


def get_all_ticker_data(symbols, col_values='close', dt=None, qtd=60, timeframe=TIMEFRAME_DEFAULT, verbose=False) -> DataFrame | None:
    """Retornando um dataframe com os precos dos ativos informados em symbols
    A partir da data informada, busca ´qtd´ barras do timeframe informado pra tras."""
    dfall = None
    i = 0
    tot_symbols = len(symbols)

    for symb in symbols:
        if verbose: print(f"Obtendo cotacoes de {symb} {i + 1} de {tot_symbols} ...")
        dfs = get_ticker_data(symb, dt=dt, qtd_barras=qtd, timeframe=timeframe)
        if i > 0:
            dfall = pd.concat([dfall, dfs])
        else:
            dfall = dfs
        i = i + 1
    print(f'Finalizado a importacao de dados de {tot_symbols} ativos.')
    return dfall.pivot(index='time', columns='ticker', values=col_values)


def get_symbols_list(categ=None):
    """Retorna uma lista com os nomes dos simbolos"""
    if categ: return get_symbol_info(categ)['name'].tolist()
    return get_symbol_info()['name'].tolist()


def get_symbol_info(categ=None, debug=False):
    """obtendo os dados dos símbolos na corretora."""
    # obtemos todos os símbolos
    symbols = mt5.symbols_get()
    qtd_symb = len(symbols)
    count = 0

    vals = []
    cols = []
    for s in symbols:
        count += 1
        # if count > 3: break
        # print("Importando {} {}/{}".format(s.name, count, qtd_symb))

        # exibimos as propriedades do símbolo como uma lista
        symbol_info_dict = s._asdict()
        if count == 1:
            cols = symbol_info_dict.keys()
            if debug: print(cols)
        vals.append(symbol_info_dict.values())

    # criando coluna extra com a categoria...
    dfs = pd.DataFrame(data=vals, columns=cols)
    dfs["categ"] = dfs["path"].str.split("\\").str.get(0)

    # eliminando a coluna com path...
    # dfs.drop(["path", "page", "session_volume", "session_interest"], axis=1, inplace=True)
    dfs.drop(["page", "session_volume", "session_interest"], axis=1, inplace=True)

    for col in dfs.columns:
        if dfs[col].max() == dfs[col].min():
            if debug: print("Elimanado a coluna ", col, " tipo:", dfs[col].dtype, " max:", dfs[col].max(), " min:", dfs[col].min())
            dfs.drop([col], axis=1, inplace=True)

    if categ is not None:
        dfs = dfs[dfs["categ"] == categ]

    return dfs
