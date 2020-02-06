import ROOT
import Data
import Layers
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

    with open("config.txt", "r") as file:
        filename = file.readline().split(" = ")[1].strip()
        file_path = file.readline().split(" = ")[1].strip()
        batch_size = int(file.readline().split(" = ")[1].strip())
        alpha = float(file.readline().split(" = ")[1].strip())
        iteration = int(file.readline().split(" = ")[1].strip())
        path_to_save = file.readline().split(" = ")[1].strip()
        name = file.readline().split(" = ")[1].strip()

    config_values = [filename,file_path, batch_size, alpha, iteration, path_to_save, name]
    model = Layers.add_layers(alpha)
    model.summary()
    f = ROOT.TFile.Open(os.path.join(file_path, filename))
    scaler = Data.scaling(f, batch_size)
    x_test, y_test = Data.training_sets(f, batch_size, iteration, scaler)
    iteration += 1
    print(x_test[:3])

    start = time.time()
    while True:

        x_train, y_train = Data.training_sets(f, batch_size, iteration, scaler)
        es = EarlyStopping(monitor='val_acc', mode='auto', verbose=2, patience=20)
        if x_train is None or y_train is None:
            break
        model.fit(x_train, y_train, validation_split=0.2, verbose=2,
                  epochs=200, callbacks=[
                es])  # xtrain je vstup... 20 parametrov v matici a riadkov ma kolko je eventov... a ytrain je vystup ci je dobry alebo zli teda vela riadkov kde bude bud jednotka alebo 0
        iteration += 1
    end = time.time() - start
    print("TOTAL TIME: " + str(end))

    result = model.predict_proba(x_test)  # predict
    print(result)
    print(model.evaluate(x_test, y_test))
    save_model(model, path_to_save, name,config_values)


def save_model(model, path_to_save, name,config_values):
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


def load(file,file_to_predict):
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

        #dorobit predict filu
        f = ROOT.TFile.Open(file_to_predict)
        with open(path + ".txt", "r") as predicted_file:
            filename = predicted_file.readline().split(" = ")[1].strip()
            file_path = predicted_file.readline().split(" = ")[1].strip()
            batch_size = int(predicted_file.readline().split(" = ")[1].strip())
            alpha = float(predicted_file.readline().split(" = ")[1].strip())
            iteration = int(predicted_file.readline().split(" = ")[1].strip())
            path_to_save = predicted_file.readline().split(" = ")[1].strip()
            name = predicted_file.readline().split(" = ")[1].strip()
        scaler = Data.scaling(f, batch_size)
        result = []
        x_test, y_test = Data.training_sets(f, batch_size, 30, scaler)
        model.compile(optimizer=Adam(lr=alpha),
                      loss='mse',  # mse binarycross...
                      metrics=['accuracy'])
        print(model.evaluate(x_test,y_test))
        while True:
            x_test, y_test = Data.training_sets(f, batch_size, iteration, scaler)
            if x_test is None or y_test is None:
                break
            iteration += 1
            for i in model.predict_proba(x_test):
                result.append(i[0])
        #print(result)


    else:
        print("File not found")
def get_model(path):
    json_file = open(path + ".json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path + ".h5")
    return loaded_model
def contains_all(files,file):
    return files.__contains__(file + ".json") and files.__contains__(file + ".h5") and files.__contains__(file + ".txt")



if __name__ == "__main__":
    if sys.argv[1] == "train":
       globals()[sys.argv[1]]()
    elif sys.argv[1] == "load":
       globals()[sys.argv[1]](sys.argv[2], sys.argv[3])
