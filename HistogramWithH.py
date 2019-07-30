import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt


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

        valores = list(allAreas[area].values())
        valoresSep = {}
        valoresSep2 = {}
        valoresSep3 = {}
        for a in allAreas[area].keys():

            if a not in Hdict.keys():
                pass
                valoresSep.update({a: 0})
                valoresSep2.update({a: 0})
                valoresSep3.update({a: 0})
            elif 100 >= Hdict[a]:
                valoresSep.update({a: allAreas[area][a]})
            elif 200 >= Hdict[a] > 100:
                valoresSep2.update({a: allAreas[area][a]})
            elif 300 >= Hdict[a] > 200:
                valoresSep3.update({a: allAreas[area][a]})

        f, (ax1, ax2, ax3) = plt.subplots(3, 1)
        ax1.bar(range(0, len(list(valoresSep.keys()))), valoresSep.values())
        ax1.set_title('H < 100')
        ax2.bar(range(0, len(list(valoresSep2.keys()))), valoresSep2.values())
        ax2.set_title('100 < H < 200')
        ax3.bar(range(0, len(list(valoresSep3.keys()))), valoresSep3.values())
        ax3.set_title('200 < H ')
        plt.show()



pass
