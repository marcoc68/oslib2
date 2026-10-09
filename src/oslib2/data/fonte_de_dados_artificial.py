import numpy as np

def criar_dados(qtd_linhas, qtd_features):
    x = np.random.rand(qtd_linhas, qtd_features)
    y = np.random.randint(2, size=(qtd_linhas, 1))
    return x, y

