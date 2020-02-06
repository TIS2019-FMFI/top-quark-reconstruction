from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation
from keras.optimizers import *
from keras.regularizers import l2

def add_layers(alpha):
    model = Sequential()

    model.add(Dense(512, input_shape=(20,), activation='relu'))
    model.add(Dense(256, activation='relu', activity_regularizer=l2(10e-9)))  # ,activity_regularizer=l2(10e-9)
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(lr=alpha),
                  loss='mse',  # mse binarycross...
                  metrics=['accuracy'])  # mse accuracy
    return model
