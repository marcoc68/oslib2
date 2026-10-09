from matplotlib import pyplot
from pandas.plotting import scatter_matrix
import seaborn as sns


def plotar_grafico_temporal(dataframe):
    dataframe.plot(subplots=True)
    pyplot.show()


def plotar_histograma(dataframe):
    """univariado: histograma"""
    dataframe.hist(sharex=False, sharey=False, xlabelsize=1, ylabelsize=1, figsize=(18, 10))
    pyplot.show()


def plotar_matrix_correlacao(dataframe):
    """multivariado: matriz de correlação"""

    # calculando a matriz de correlação...
    corr = dataframe.corr(method='spearman', numeric_only=True)

    # calculando o tamanho da figura...
    qtd_features = len(dataframe.columns)
    tamanho_horizontal = max(8,qtd_features *0.8)
    tamanho_vertical   = max(7,qtd_features *0.6)

    fig, ax = pyplot.subplots(figsize=(tamanho_horizontal,tamanho_vertical))
    ax = sns.heatmap(corr, annot=True, linewidths=.5, fmt=".2f", cmap="YlGnBu")


def plotar_grafico_densidade(dataframe):
    """univariado: grafico de densidade"""
    dataframe.plot(kind='density', subplots=True, sharey=False, legend=True, fontsize=1, figsize=(18, 10))
    pyplot.show()

def plotar_matrix_dispersao(dataframe):
    """multivariado: gráfico de dispersão"""
    scatter_matrix(dataframe)