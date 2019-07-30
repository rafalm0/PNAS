import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


Hdict = {}
file = pd.read_csv('dev/output/translatorALL.csv', sep=';', encoding='utf-8')
for i, line in file.iterrows():
    if (line['H'] == line['H']) and (line['H'] != '-'):
        Hdict.update({line['Editor']: int(line['H'].split('.')[0])})

allAreas = {}
for file in os.listdir('dev/editores/lists/editores,3,2019,7,8'):
    allAreas[file.split('.')[0]] = {}
    arquivo = open('dev/editores/lists/editores,3,2019,7,8/' + file, 'r', encoding = 'utf-8')
    for nome in arquivo:
        nome = nome.rstrip()
        if '\ufeff' in nome:
            nome = nome.replace('\ufeff', '')
        if 'ï»¿' in nome:
            nome = nome.replace('ï»¿', '')
        # if nome in Hdict.keys():
        #     allAreas[file.split('.')[0]][nome] = 0
        allAreas[file.split('.')[0]][nome] = 0

for file in os.listdir('dev/artigos/2019'):
    arquivo = pickle.load(open('dev/artigos/2019/' + file, 'rb'))
    for area in arquivo.keys():
        if area in allAreas.keys():
            for article in arquivo[area]:
                if article[2] in allAreas[area].keys():
                    allAreas[area][article[2]] = allAreas[area][article[2]] + 1


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
