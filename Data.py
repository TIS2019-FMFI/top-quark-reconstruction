import ROOT
import numpy as np
import sys
from sklearn.preprocessing import StandardScaler

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(suppress=True)


def dump_root_details(f, batch_size, iteration):
    matica_s = []
    result = []
    for i in range(20):
        matica_s.append([])
    lst = f.GetListOfKeys()

    ratio = 2

    if (lst[0].ReadObj().GetEntries() + lst[1].ReadObj().GetEntries()) // batch_size < iteration:
        return None
    if ((lst[1].ReadObj().GetEntries() // (batch_size / ratio * (ratio - 1))) < iteration):
        return None
    if ((lst[0].ReadObj().GetEntries() // (batch_size / ratio)) < iteration):
        return None

    # naplni maticu a result signal datami
    matica_s, result = get_signal(result, matica_s, lst, iteration, batch_size, ratio)
    if matica_s is None:
        return None
    # naplni maticu a result background datami
    matica_s, result = get_background(result, matica_s, lst, iteration, batch_size, ratio)
    if matica_s is None:
        return None
    train_x = np.array(zip(*matica_s))
    train_y = np.array(result)
    dataset = zip(train_x, train_y)
    np.random.shuffle(dataset)
    train_x, train_y = zip(*dataset)
    return train_x, train_y


def get_signal(result_in, matica_s_in, lst, iteration, batch_size, ratio):
    matica_s = matica_s_in
    result = result_in
    obj = lst[0].ReadObj()
    nEntries = obj.GetEntries()
    listOfBranches = obj.GetListOfBranches()
    jet = 0
    for b in listOfBranches:
        if b.GetName()[:3] == "jet" and not (b.GetName() == "jet_n"):
            i = (iteration * batch_size) / ratio
            while len(matica_s[jet]) < batch_size / ratio and i <= nEntries:
                obj.GetEntry(i)
                leaf_value = getattr(obj, b.GetName())
                matica_s[jet].append(leaf_value)
                if b.GetName() == "jet1_pt":
                    result.append([1])
                i += 1
            if len(matica_s[jet]) < batch_size / ratio:
                return None, None
            jet = jet + 1
    return matica_s, result


def get_background(result_in, matica_s_in, lst, iteration, batch_size, ratio):
    matica_s = matica_s_in
    result = result_in
    obj = lst[1].ReadObj()
    nEntries = obj.GetEntries()
    listOfBranches = obj.GetListOfBranches()
    jet = 0
    for b in listOfBranches:
        if b.GetName()[:3] == "jet" and not (b.GetName() == "jet_n"):
            i = (iteration * batch_size) / ratio * (ratio - 1)
            while len(matica_s[jet]) < batch_size and i <= nEntries:
                obj.GetEntry(i)
                leaf_value = getattr(obj, b.GetName())
                matica_s[jet].append(leaf_value)
                if b.GetName() == "jet1_pt":
                    result.append([0])
                i += 1
            if len(matica_s[jet]) < batch_size:
                return None, None
            jet = jet + 1
    return matica_s, result


def scaling(f, batch_size):
    scaler = StandardScaler()
    iteration = 0
    while True:
        pom = dump_root_details(f, batch_size, iteration)
        if pom is None:
            return scaler
        X,Y = pom
        scaler.fit(X)
        iteration += 1

def training_sets(f, batch_size, iteration, scale):
    XY = dump_root_details(f, batch_size, iteration)

    if XY is None: return None, None
    X = np.array(XY[0])
    Y = np.array(XY[1])
    scaler = scale
    return scaler.fit_transform(X), Y


def minmax(f):
    maximum = 500000
    minimum = -500000
    count = 0
    pom=0
    for prvok in f[0]:
        if 1 == f[1][pom]:
            if min(prvok) < minimum or max(prvok) > maximum:
                count += 1
        pom+=1
    return count
