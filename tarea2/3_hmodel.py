import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D, AveragePooling2D
from keras.optimizers import SGD, Adadelta, Adagrad

train_data = sio.loadmat('train_32x32.mat')
test_data = sio.loadmat('test_32x32.mat')

# Cargar set de entrenamiento
X_train = train_data['X'].T
y_train = train_data['y'] - 1

# Cargar set de test
X_test = test_data['X'].T
y_test = test_data['y'] - 1

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

# Numero de clases
n_classes = len(np.unique(y_train))

# Numero de ejemplos
n_train = len(X_train)
n_test = len(X_test)

# Normalizar imagenes
X_train /= 255
X_test /= 255

Y_train = np_utils.to_categorical(y_train, n_classes)
Y_test = np_utils.to_categorical(y_test, n_classes)

(n_channels, n_rows, n_cols) = np.shape(X_train[0])

model = Sequential()

model.add(Convolution2D(16, 5, 5, border_mode='same', input_shape=(n_channels, n_rows, n_cols)))
convout1 = Activation('relu')
model.add(convout1)

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(512, 7, 7, border_mode='same', activation='relu', name='conv2'))
convout2 = Activation('relu')
model.add(convout2)

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(20, activation='relu'))
model.add(Dense(n_classes, activation='softmax'))

model.compile(loss='binary_crossentropy', optimizer="adagrad", metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=1280, nb_epoch=12, verbose=1, validation_data=(X_test, Y_test))

model.save('model_h.h5')
