from oslib2.data import window
import numpy as np

def criar_window_1_2():
    win = window.Window(2)
    win.add(1)
    win.add(2)
    return win

def test_window_at():
    win = criar_window_1_2()
    assert win.at(0) == 1
    assert win.at(1) == 2

def test_window_add_rotacao():
    win = criar_window_1_2()
    win.add(3)
    assert win.at(0) == 2
    assert win.at(1) == 3

def test_window_set():
    win = criar_window_1_2()
    win.set(0,3)
    win.set(1,4)
    assert win.at(0) == 3
    assert win.at(1) == 4

def test_window_set_last():
    win = criar_window_1_2()
    win.set_last(3)
    assert win.at(0) == 1
    assert win.at(1) == 3

def test_window_is_full():
    win = criar_window_1_2()
    assert win.is_full() == True

def test_window_clear():
    win = criar_window_1_2()
    assert win.is_full() == True

    win.clear()
    assert win.is_full() == False

    win.add(3)
    assert win.is_full() == False

def test_window_size():
    win = criar_window_1_2()
    assert win.size == 2

    win.clear()
    assert win.size == 0

    win.add(3)
    assert win.size == 1

def test_window_to_numpy():
    win = criar_window_1_2()

    vet = np.array([1,2])
    assert (win.to_numpy() == vet).all()

def test_capacidade_deve_retornar_capacidade_correta():
    win = criar_window_1_2()
    assert win.capacity == 2

    win.clear()
    assert win.capacity == 2
    assert win.size == 0



