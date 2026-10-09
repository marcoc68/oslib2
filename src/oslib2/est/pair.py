import MetaTrader5 as mt5
import oslib2.data.window_asset as win
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

class Pair:
    """
    Dados estatisticos para PairTrading
    """
    def __init__(self, asset1: str, asset2: str, timeframe: int = mt5.TIMEFRAME_M1, win_len: int = 10):
        self.win_asset1 = win.WindowAsset(asset1, timeframe, win_len, with_log=True)
        self.win_asset2 = win.WindowAsset(asset2, timeframe, win_len, with_log=True)
        self.timeframe = timeframe

        self.coef_correlacao = 0.0
        self.par_eh_cointegrado = False
        self.zscore = 0.0
        self.beta = 0.0
        self.intercept = 0.0
        self.spread_med = 0.0
        self.spread_std = 0.0

    def carregar_historico(self, valor='close', analizar_cointegracao=True) -> bool:
        """
        Carrega o histórico de valores dos ativos
        valor pode ser 'open', 'high', 'low', 'close', 'tick_volume', 'spread' ou 'real_volume'.
        """
        if not (self.win_asset1.carregar_historico(valor) and self.win_asset2.carregar_historico(valor) ):
            print(f"Erro ao carregar histórico de {valor} para {self.win_asset1.symbol} ou {self.win_asset2.symbol}: {mt5.last_error()}")
            return False

        # calculado beta/correlacao e cointegracao...
        if analizar_cointegracao: return self.analizar_cointegracao()
        return True

    def carregar_ultimo(self, valor='close', analizar_cointegracao=False) -> bool:
        """
        Carrega o preço mais recente dos ativos. Se for uma nova barra fechada,
        adiciona ao buffer; se for a mesma barra, atualiza o último valor.
        """
        if not (self.win_asset1.carregar_ultimo(valor) and self.win_asset2.carregar_ultimo(valor) ):
            print(f"Erro ao carregar último {valor} para {self.win_asset1.symbol} ou {self.win_asset2.symbol}: {mt5.last_error()}")
            return False

        if analizar_cointegracao: return self.analizar_cointegracao()
        return True

    def analizar_cointegracao(self):
        p1 = self.win_asset1.to_numpy()
        p2 = self.win_asset2.to_numpy()

        # 1. Correlação de Pearson
        self.coef_correlacao = np.corrcoef(p1, p2)[0, 1]

        # 2. Regressão OLS (Engle-Granger) para encontrar Beta e Intercepto
        X = sm.add_constant(p2)
        model = sm.OLS(p1, X).fit()
        self.beta = model.params[1]
        self.intercept = model.params[0]

        # 3. Teste de Cointegração ADF via statsmodels
        score, p_value, _ = coint(p1, p2)
        self.par_eh_cointegrado = (p_value < 0.05)

        # 4. Geração do Spread (Resíduos da Regressão) e Estatísticas
        spread = p1 - (self.beta * p2 + self.intercept)
        self.spread_med = np.mean(spread)
        self.spread_std = np.std(spread, ddof=1)

        # Spread atual (último elemento)
        spread_atual = spread[-1]
        if self.spread_std > 0:
            self.zscore = (spread_atual - self.spread_med) / self.spread_std
        else:
            self.zscore = 0.0

        return True
