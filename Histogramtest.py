import pickle
import os
import matplotlib.pyplot as plt
import math


allAreas = {}
for file in os.listdir('dev/editores/lists/editores'):
    allAreas[file.split('.')[0]] = {}
    arquivo = open('dev/editores/lists/editores/' + file, 'r', encoding = 'utf-8')
    for nome in arquivo:
        nome = nome.rstrip()
        if '\ufeff' in nome:
            nome = nome.replace('\ufeff', '')
        if 'ï»¿' in nome:
            nome = nome.replace('ï»¿', '')
        allAreas[file.split('.')[0]][nome] = 0


for file in os.listdir('dev/artigos/2019'):
    arquivo = pickle.load(open('dev/artigos/2019/' + file, 'rb'))
    for area in arquivo.keys():
        if area in allAreas.keys():
            for article in arquivo[area]:
                if article[2] in allAreas[area].keys():
                    allAreas[area][article[2]] = allAreas[area][article[2]] + 1


k = 10
for area in allAreas.keys():
    if not sum(list(allAreas[area].values())) == 0:
        valores = list(allAreas[area].values())
        # quantDeEditores = len(list(allAreas[area].keys()))
        # plt.bar(list(range(quantDeEditores)), valores)

        quantDeEditores = math.ceil(len(list(allAreas[area].keys()))/k)

        novosValores = []
        for numero in list(range(quantDeEditores)):
            novosValores.append(0)

        for i, valor in enumerate(valores):
            novosValores[i//k] += valor
        plt.bar(list(range(quantDeEditores)), novosValores)
        plt.title(area)
        plt.show()

pass


