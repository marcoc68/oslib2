import MetaTrader5 as mt5
import oslib2.data.window as window
import oslib2.util.util as utl

class WindowAsset(window.Window):
    """
    Herda de Window e adiciona métodos para gerenciar ativos
    e buscar dados diretamente do terminal MetaTrader 5.
    """

    def __init__(self, symbol: str, timeframe: int = mt5.TIMEFRAME_M1, capacity: int = 10):
        super().__init__(capacity)  # Inicializa o construtor da classe base
        self.symbol = symbol
        self.timeframe = timeframe
        self.timeframe_in_seconds = utl.period_seconds(self.timeframe)
        self.prox_timestamp = 0

    def carregar_historico(self, valor='close') -> bool:
        """
        Obtém e preenche o buffer com o histórico de valores do ativo
        a partir da barra atual (posição 0) até o tamanho da capacidade.
        valor pode ser 'open', 'high', 'low', 'close', 'tick_volume', 'spread' ou 'real_volume'.
        """
        self.clear()

        # Busca as barras do MT5 a partir da posição atual 0
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, self.capacity)

        if rates is None or len(rates) == 0:
            print(f"Erro ao carregar histórico de {valor} para {self.symbol}: {mt5.last_error()}")
            return False

        # Preenche o buffer com os preços de fechamento (close)
        for rate in rates:
            self.add(rate[valor])

        # prox data permitida é a ultima data + timeframe
        self._atualizar_prox_data_permitida(rates)

        print(f"[{self.symbol}] Histórico carregado com sucesso. {self.size} barras inseridas.")
        return True

    def _atualizar_prox_data_permitida(self, rates):
        self.prox_timestamp = rates[-1]['time'] + self.timeframe_in_seconds

    def carregar_ultimo(self, valor='close') -> bool:
        """
        Obtém o preço mais recente do ativo. Se for uma nova barra fechada,
        adiciona ao buffer; se for a mesma barra, atualiza o último valor.
        """
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, 1)

        if rates is None or len(rates) == 0:
            print(f"Erro ao carregar {valor} para {self.symbol}: {mt5.last_error()}")
            return False

        barra_atual = rates[0]
        time_atual  = barra_atual['time']
        valor_atual = barra_atual[valor]

        if self.size > 0 and time_atual < self.prox_timestamp:
            # Mesma barra: apenas atualiza o valor mais recente (tick/atualização)
            self.set_last(valor_atual)
            return True
        else:
            # Nova barra: insere no buffer (o mais antigo é descartado automaticamente pelo deque)
            self.add(valor_atual)
            self._atualizar_prox_data_permitida(rates)
            return True