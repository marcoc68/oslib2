from collections import deque
from oslib2.data import window_asset as wass
from oslib2.data import fonte_de_dados_mt as fdm

def t1_deque():
    # Cria um buffer com capacidade máxima de 3 elementos
    buffer = deque(maxlen=3)

    # Adicionando elementos
    buffer.append(10.0)
    buffer.append(20.0)
    buffer.append(30.0)

    print("Buffer atual:", list(buffer))  # [10.0, 20.0, 30.0]

    # Adicionando um 4º elemento. O '10.0' (mais antigo) é descartado automaticamente:
    buffer.append(40.0)

    print("Após adicionar 40.0:", list(buffer))  # [20.0, 30.0, 40.0]

    # Acesso direto por índice (0 = mais antigo, -1 = mais recente)
    print("Mais antigo (índice 0):", buffer[0])   # 20.0
    print("Mais recente (último):", buffer[-1])  # 40.0

def t2_window_asset():
    print("Conectando ao MT5...")
    fdm.conectar_mt5('desen')

    win = wass.WindowAsset("GBPUSD",capacity=3)
    win.carregar_historico()
    vet = win.to_numpy()
    print(f'Precos: {vet}')

    win.carregar_ultimo()
    print(f'Ultimo preco: {win.at_last()}')



if __name__ == '__main__':

    t2_window_asset()