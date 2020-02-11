from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation
from keras.optimizers import *
from keras.regularizers import l2
from keras.callbacks import EarlyStopping

def add_layers(config_values):
    model = Sequential()

    first_layer = True
    for i in config_values[-1]:
        pole = i.split(",")
        activation_value = pole[1]
        if activation_value[-1] == "\n":
            activation_value = activation_value[:-1]
        if first_layer:
            model.add(Dense(int(pole[0]), input_shape=(20,), activation=activation_value))
            first_layer = False
        else:
            if len(pole) > 2:
                model.add(Dense(int(pole[0]), input_shape=(20,), activation=activation_value, activity_regularizer=l2(float(pole[2][:-1]))))
            else:
                model.add(Dense(int(pole[0]), activation=activation_value))
    model.compile(optimizer=Adam(lr=config_values[0]),
                  loss=config_values[1],  # mse binarycross...
                  metrics=[config_values[2]])  # mse accuracy
    es = EarlyStopping(monitor=config_values[3], mode=config_values[4], verbose=2, patience=20)
    return model
