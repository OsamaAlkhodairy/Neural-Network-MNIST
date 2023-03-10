import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils

from Dense import Dense
from Activations import Tanh
from Losses import mse, mse_prime
from Network import train, predict

def preprocess_data(x, y, limit):
    x = x.reshape(x.shape[0], 28 * 28, 1)
    x = x.astype("float32") / 255

    y = np_utils.to_categorical(y)
    y = y.reshape(y.shape[0], 10, 1)
    return x[:limit], y[:limit]

(x_train, y_train), (x_test, y_test) = mnist.load_data()
(x_train, y_train) = preprocess_data(x_train, y_train, 10000)
(x_test, y_test) = preprocess_data(x_test, y_test, 100)

network = [
    Dense(28 * 28, 40),
    Tanh(),
    Dense(40, 10),
    Tanh()
]

train(network, mse, mse_prime, x_train, y_train, epochs=100, learning_rate=0.01)

guessed_correctly = 0
total = 0

for x, y in zip(x_test, y_test):
    output = predict(network, x)
    prediction = np.argmax(output)
    actual = np.argmax(y)
    if prediction == actual:
        guessed_correctly += 1
    total += 1
    print('pred:', np.argmax(output), '\ttrue:', np.argmax(y))

print('total accuracy: ', guessed_correctly, '/', total)
