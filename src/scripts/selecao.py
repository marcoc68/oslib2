import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

def selecionar_features(dataframe, qtd_features=2):
    """seleção de features"""

    # 1. Definimos X e Y brutos
    X_raw = dataframe.iloc[:, :-1]
    Y_raw = dataframe.iloc[:, -1]

    # 2. Melhoria na limpeza: preenchemos buracos pequenos e removemos o que sobrar
    # Isso evita que uma única falha em um papel em uma data exclua os demais papeis
    X_clean = X_raw.ffill().bfill()
    Y_clean = Y_raw.ffill().bfill()

    # 3. Concatenamos ambos para garantir o alinhamento perfeito pelo índice (Data)
    # e removemos qualquer linha que tenha valor nulo em qualquer uma das colunas
    df_temporary = pd.concat([X_clean, Y_clean], axis=1).dropna()

    # 3. Separamos novamente em X e Y agora perfeitamente alinhados
    X = df_temporary.iloc[:, :-1]
    Y = df_temporary.iloc[:, -1]

    # se a quantidade de features solicitada for muito grande, usamos a quantidade total
    qtd_features = min(qtd_features, X.shape[1])


    bestFeatures = SelectKBest(score_func=f_regression, k=qtd_features)
    fit = bestFeatures.fit(X,Y)
    dfscores = pd.DataFrame(fit.scores_,columns=['Score'])
    dffeatures = pd.DataFrame(X.columns ,columns=['Feature'])
    featureScores = pd.concat([dffeatures,dfscores], axis=1)
    return featureScores.sort_values(by='Score', ascending=False ).head(qtd_features).reset_index(drop=True)


def selecionar_features_correlacionadas(df_features) -> pd.DataFrame:
    """Seleciona features correlacionadas"""
    return df_features.corr().abs().unstack().sort_values(kind="quicksort", ascending=False).reset_index().head(100)

