import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pickle
import os


subareadict = {}

for filepath in os.listdir('dev/areas-subarea'):
    file = open('dev/areas-subarea/' + filepath, 'r', encoding = 'utf-8')
    for line in file:
        line = line.replace('\ufeff', '')
        subareadict[line.rstrip()] = filepath.split('.')[0]

allAreas = {}
for file in os.listdir('dev/editores/lists/editores,3,2019,7,8'):
    if file.split('.')[0] not in subareadict.keys():
        print(file.split('.')[0])
        continue
    if subareadict[file.split('.')[0]] not in allAreas.keys():
        allAreas[subareadict[file.split('.')[0]]] = {}
    arquivo = open('dev/editores/lists/editores,3,2019,7,8/' + file, 'r', encoding = 'utf-8')
    for nome in arquivo:
        nome = nome.rstrip()
        if '\ufeff' in nome:
            nome = nome.replace('\ufeff', '')
        if 'ï»¿' in nome:
            nome = nome.replace('ï»¿', '')
        allAreas[subareadict[file.split('.')[0]]][nome] = 0

for file in os.listdir('dev/artigos/2019'):
    arquivo = pickle.load(open('dev/artigos/2019/' + file, 'rb'))
    for area in arquivo.keys():
        for article in arquivo[area]:
            if article[2] in allAreas[subareadict[area]].keys():
                allAreas[subareadict[area]][article[2]] = allAreas[subareadict[area]][article[2]] + 1

# for area in allAreas.keys():
#     if not sum(list(allAreas[area].values())) == 0:
#
#         nomesSorted = [[nome, nome.split(' ')[-1]] for nome in list(allAreas[area].keys())]
#         nomesSorted.sort(key= lambda a: a[1])
#         x = list(range(len(allAreas[area].keys())))
#         y = []
#         for nome in nomesSorted:
#             if allAreas[area][nome[0]] != 0:
#                 y.append(allAreas[area][nome[0]])
#         x = list(range(len(y)))
#         slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
#         mn = np.min(x)
#         mx = np.max(x)
#         x1 = np.linspace(mn, mx, len(x))
#         y1 = slope * x1 + intercept
#         plt.plot(x, y, 'ob')
#         if x1 is not None:
#             plt.plot(x1, y1, '-r')
#         plt.show()

for area in allAreas.keys():
    if not sum(list(allAreas[area].values())) == 0:
        valoresSep = {}
        for codLetra in range(65, 91):
            valoresSep[chr(codLetra)] = 0
        valores = list(allAreas[area].values())
        for a in allAreas[area].keys():
            # if a in Hdict.keys():
            letra = a.split(' ')[-1][0]
            if letra not in valoresSep.keys():
                print("letra nao registrada %c" % letra)
                continue
            quantidade = allAreas[area][a]
            valoresSep[letra] += quantidade

        xoriginal = list(range(0, len(list(valoresSep.keys()))))
        yoriginal = list(valoresSep.values())
        xletras = []
        y = []
        for key in valoresSep.keys():
            xletras.append(key)
            y.append(valoresSep[key])
            # if valoresSep[key] != 0:
            #     xletras.append(key)
            #     y.append(valoresSep[key])
        x = list(range(0, len(xletras)))
        x1 = None
        if not len(x) <= 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            mn = np.min(x)
            mx = np.max(x)
            x1 = np.linspace(mn, mx, 500)
            y1 = slope * x1 + intercept
        plt.title('Escolhas de editores por letra (%s)' % area)
        # plt.plot(list(valoresSep.keys()), y, 'ob')
        plt.plot(xletras, y, 'ob')
        if x1 is not None:
            plt.plot(x1, y1, '-r')
        plt.show()




pass
