# under development

import collections
import math

from termcolor import cprint

trainingDataSet = []


def readfile(filename):
    file = open(filename, 'rb')
    data = file.read()
    file.close()
    return data


def init():
    data1 = readfile('training-data/live_mode_training_data1.bin')
    data2 = readfile('training-data/live_mode_training_data2.bin')
    data3 = readfile('training-data/live_mode_training_data3.bin')
    trainingDataSet.append(data1)
    trainingDataSet.append(data2)
    trainingDataSet.append(data3)


def isCompatible(source, target):
    slist = list(bytes(source))
    tlist = list(bytes(target))
    # start = tlist.index(slist[0])
    # comparableLength = len(tlist) - start
    # k = 0
    matches = 0
    # for i in range(start, len(target)):
    #     if slist[k] == tlist[i]:
    #         matches += 1
    #     k += 1
    # cprint(f'{matches}, {comparableLength}', 'blue', attrs=['bold'])

    counts1 = collections.Counter(slist)
    counts2 = collections.Counter(tlist)
    addx1 = []
    addx2 = []
    for (k, v) in counts1.items():
        addx1.append(math.ceil(v / 10) * 10)
    for (k, v) in counts2.items():
        addx2.append(math.ceil(v / 10) * 10)

    print(addx2)

    for ax in addx1:
        if ax in addx2:
            matches += 1

    # for (k, v) in counts1.items():
    #     if math.ceil(counts2[k] / 100) * 100 == math.ceil(v / 100) * 100:
    #         matches += 1
    cprint(f'{matches} out of {len(addx1)}', "red", attrs=['bold'])
    return matches / len(addx1) >= 0.96


def compare(frames):
    target = b''.join(frames)
    for data in trainingDataSet:
        if isCompatible(data, target):
            return True
    return False
