from collections import deque
import numpy as np

class Window:
    """Buffer circular genérico reutilizável, construído nativamente com collections.deque."""
    def __init__(self, capacity: int = 10):
        self.capacity = capacity if capacity > 0 else 10
        # O deque com maxlen descarta automaticamente o elemento mais antigo ao estourar a capacidade
        self.buffer = deque(maxlen=self.capacity)

    def add(self, value: float):
        """Adiciona um novo elemento ao final do buffer. Se estiver cheio, o mais antigo é descartado."""
        self.buffer.append(value)

    def set(self, ind: int, value: float):
        """Atualiza o valor do elemento em ind."""
        self.buffer[ind] = value

    def set_last(self, value: float):
        """Atualiza o valor do elemento mais recente (último adicionado)."""
        self.buffer[-1] = value

    def at(self, index: int) -> float:
        """Acessa o elemento por índice lógico (0 = mais antigo, size-1 = mais recente)."""
        return self.buffer[index]

    def at_last(self) -> float:
        """Retorna o último elemento. Mais recente."""
        return self.buffer[-1]

    def to_numpy(self) -> np.ndarray:
        """Retorna os dados convertidos para um array NumPy ordenado (do mais antigo para o mais recente)."""
        return np.array(self.buffer, dtype=np.float64)

    def clear(self):
        """Limpa o buffer."""
        self.buffer.clear()

    def is_full(self) -> bool:
        """Retorna True se o buffer atingiu a capacidade máxima."""
        return len(self.buffer) == self.capacity

    @property
    def size(self) -> int:
        """Retorna a quantidade atual de elementos."""
        return len(self.buffer)

