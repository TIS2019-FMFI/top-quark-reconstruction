import ROOT
import Data
import Layers
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from keras.utils import plot_model
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation
from keras.optimizers import *
from keras.regularizers import l2
from keras.callbacks import EarlyStopping
import time
import os
from datetime import date
import sys


def train():
    config_values = read_config("", "config")
    iteration = config_values[4]
    send_layer = [config_values[3]]
    for i in range(10, len(config_values)):
        send_layer.append(config_values[i])
    model = Layers.add_layers(send_layer)
    model.summary()
    f = ROOT.TFile.Open(os.path.join(config_values[1], config_values[0]))
    scaler = Data.scaling(f, config_values[2], config_values[7], config_values[8], config_values[9])
    x_test, y_test = Data.training_sets(f, config_values[2], iteration, scaler)
    iteration += 1
    print(x_test[:3])

    start = time.time()
    train_h=[]
    while True:
        x_train, y_train = Data.training_sets(f, config_values[2], iteration, scaler)
        es = EarlyStopping(monitor='val_acc', mode='auto', verbose=2, patience=30)
        if x_train is None or y_train is None:
            break
        history = model.fit(x_train, y_train, validation_split=0.2, verbose=2,
                            epochs=200, callbacks=[
                es])  # xtrain je vstup... 20 parametrov v matici a riadkov ma kolko je eventov... a ytrain je vystup ci je dobry alebo zli teda vela riadkov kde bude bud jednotka alebo 0
        iteration += 1
        train_h.append(history)
    end = time.time() - start
    print("TOTAL TIME: " + str(end))

    train_acc=[]
    train_val_acc=[]
    train_loss=[]
    train_val_loss=[]
    for historia in train_h:
        for prvok in historia.history['acc']:
            train_acc.append(prvok)
        for prvok in historia.history['val_acc']:
            train_val_acc.append(prvok)
        for prvok in historia.history['loss']:
            train_loss.append(prvok)
        for prvok in historia.history['val_loss']:
            train_val_loss.append(prvok)

    today = date.today()
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(os.path.join(str(config_values[5]), str(config_values[6]) + '_acc' + str(today) + '.png'))

    plt.close()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(os.path.join(str(config_values[5]), str(config_values[6]) + '_loss' + str(today) + '.png'))

    result = model.predict_proba(x_test)  # predict
    print(result)
    print(model.evaluate(x_test, y_test))
    save_model(model, config_values[5], config_values[6], config_values)


def save_model(model, path_to_save, name, config_values):
    model_json = model.to_json()
    today = date.today()

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    with open(os.path.join(path_to_save, name + "_" + str(today) + ".json"), "w") as json_file:
        json_file.write(model_json)
    with open(os.path.join(path_to_save, name + "_" + str(today) + ".txt"), "w") as config_file:
        config_file.write("filename = " + str(config_values[0]) + "\n")
        config_file.write("file_path = " + str(config_values[1]) + "\n")
        config_file.write("batch_size = " + str(config_values[2]) + "\n")
        config_file.write("alpha = " + str(config_values[3]) + "\n")
        config_file.write("iteration = " + str(config_values[4]) + "\n")
        config_file.write("path_to_save = " + str(config_values[5]) + "\n")
        config_file.write("saved_as = " + str(config_values[6]))
    model.save_weights(os.path.join(path_to_save, name + "_" + str(today) + ".h5"))


def load(file, file_to_predict):
    print("IDEM")
    path = None
    for dirpath, dirnames, files in os.walk('.'):
        for file_name in files:
            if file_name == file + ".json":
                if contains_all(files, file):
                    path = "/home/topqproject/src/palo" + dirpath[1:] + "/" + file
                    break
                else:
                    print("Missing file (name.json, .h5 or .txt)")
                    return
    if path is not None:
        model = get_model(path)

        # dorobit predict filu
        f = ROOT.TFile.Open(file_to_predict)
        config_values = read_config(path, "")
        scaler = Data.scaling(f, config_values[2])
        result = []
        x_test, y_test = Data.training_sets(f, config_values[2], 30, scaler)
        model.compile(optimizer=Adam(lr=config_values[3]),
                      loss='mse',  # mse binarycross...
                      metrics=['accuracy'])
        print(model.evaluate(x_test, y_test))
        iteration = config_values[4]
        while True:
            x_test, y_test = Data.training_sets(f, config_values[2], iteration, scaler)
            if x_test is None or y_test is None:
                break
            iteration += 1
            for i in model.predict_proba(x_test):
                result.append(i[0])
        # print(result)


    else:
        print("File not found")


def get_model(path):
    json_file = open(path + ".json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path + ".h5")
    return loaded_model


def contains_all(files, file):
    return files.__contains__(file + ".json") and files.__contains__(file + ".h5") and files.__contains__(file + ".txt")


def read_config(path, name):
    with open(path + name + ".txt", "r") as file:
        filename = file.readline().split(" = ")[1].strip()
        file_path = file.readline().split(" = ")[1].strip()
        batch_size = int(file.readline().split(" = ")[1].strip())
        alpha = float(file.readline().split(" = ")[1].strip())
        iteration = int(file.readline().split(" = ")[1].strip())
        path_to_save = file.readline().split(" = ")[1].strip()
        name = file.readline().split(" = ")[1].strip()
        minimum = file.readline().split(" = ")[1].strip()
        maximum = file.readline().split(" = ")[1].strip()
        run_minmax = file.readline().split(" = ")[1].strip()
        loss = file.readline().split(" = ")[1].strip()
        metrics = file.readline().split(" = ")[1].strip()
        monitor = file.readline().split(" = ")[1].strip()
        mode = file.readline().split(" = ")[1].strip()

        row = file.readline()
        layers = []
        while row != "":
            layers.append(row)
            row = file.readline()
    return [filename, file_path, batch_size, alpha, iteration, path_to_save, name, minimum, maximum, run_minmax, loss,
            metrics, monitor, mode, layers]


if __name__ == "__main__":
    if sys.argv[1] == "train":
        globals()[sys.argv[1]]()
    elif sys.argv[1] == "load":
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3])
