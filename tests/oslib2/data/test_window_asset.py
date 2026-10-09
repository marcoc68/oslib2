from oslib2.data import fonte_de_dados_mt as fdm
from oslib2.data import window_asset as wass

conectado = False
def conectar():
    global conectado
    if not conectado:
        print("Conectando ao MT5...")
        fdm.conectar_mt5('desen')
        conectado = True

def criar_win_asset(tamanho_janela:int = 3):
    conectar()
    win = wass.WindowAsset("GBPUSD",capacity=tamanho_janela)
    return win

def criar_win_asset_falso(tamanho_janela:int = 3):
    conectar()
    win = wass.WindowAsset("GBPUSDXXXX",capacity=tamanho_janela)
    return win

def test_carregar_historico():
    win = criar_win_asset(4)
    win.carregar_historico()
    assert win.size == 4

def test_carregar_preco_atual():
    win = criar_win_asset(4)
    assert win.carregar_ultimo()
    assert win.size == 1

def test_comparar_preco_atual_com_ultimo_preco_do_historico():
    win_hist  = criar_win_asset(4)
    win_atual = criar_win_asset(4)

    assert win_hist.carregar_historico()
    assert win_atual.carregar_ultimo()

    assert win_hist.at_last() == win_atual.at_last()
    assert win_hist.at_last() == win_atual.at(0)
    assert win_hist.at(3) == win_atual.at(0)


def test_carregar_duas_vezes_antes_da_nova_cotacao():
    win = criar_win_asset(4)
    assert win.size == 0
    assert win.carregar_ultimo()
    assert win.size == 1
    assert win.carregar_ultimo()
    assert win.size == 1

def test_carga_ativo_inexistente_de_retornar_falso_e_janela_vazia():
    win = criar_win_asset_falso(4)
    assert win.size == 0

    assert win.carregar_historico() == False
    assert win.size == 0

    assert win.carregar_ultimo() == False
    assert win.size == 0
