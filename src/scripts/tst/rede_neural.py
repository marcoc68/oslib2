from keras.models import Sequential
from keras.layers import Dense
import numpy as np

def criar_modelo():
    model = Sequential()
    model.add(Dense(32, input_shape=10, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def treinar_modelo(model, x, y, epocas=10, tamanho_lote=32):
    model.fit(x, y, epochs=epocas, batch_size=tamanho_lote)

def avaliar_modelo(model, x, y):
    _, accuracy = model.evaluate(x, y)
    print(f"{model.metrics_names[1]}: {accuracy*100:.2f}%")
    return accuracy
