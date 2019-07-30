import os
import pickle
import pandas as pd


def histogram_data():
    quantAreas = {}
    for article in os.listdir('2019'):
        revista = pickle.load(open('2019/' + article, 'rb'))
        for subarea in revista.keys():
            if subarea not in quantAreas.keys():
                quantAreas[subarea] = []
            for artigo in revista[subarea]:
                if artigo[2] not in quantAreas[subarea]:
                    quantAreas[subarea].append(artigo[2])

    dicionarioArea = {}

    for file in os.listdir('editores'):
        arquivo = open('editores/' + file, 'r', encoding='utf-8')
        for nome in arquivo:
            nomestriped = nome.rstrip()
            if '\ufeff' in nomestriped:
                nomestriped = nomestriped.replace('\ufeff', '')
            if nomestriped not in dicionarioArea:
                dicionarioArea[nomestriped] = []
            if file not in dicionarioArea[nomestriped]:
                dicionarioArea[nomestriped].append(file.split('.')[0])

    return


def getListedEditors():
    ListedEditors = []
    for file in os.listdir('editores,1,2019,6,24'):
        x = open('editores,1,2019,6,24/' + file, 'r', encoding = 'utf-8')
        for nome in x:
            nomestriped = nome.rstrip()
            if '\ufeff' in nomestriped:
                nomestriped = nomestriped.replace('\ufeff', '')
            if 'ï»¿' in nomestriped:
                nomestriped = nomestriped.replace('ï»¿', '')
            if nomestriped not in ListedEditors:
                ListedEditors.append(nomestriped)
    return ListedEditors


def getArticles2019(asDataFrame = False, ListedEditors = None):

    if asDataFrame:
        x = {}
        ids = []
        editors = []
        edicao = []
        ano = []
        subArea = []
        possivel = []
        for file in os.listdir('2019'):
            dic = pickle.load(open('2019/' + file, 'rb'))
            for subarea in dic.keys():
                if subarea not in x:
                    x[subarea] = []
                for article in dic[subarea]:
                    if article[0] not in x[subarea]:
                        subArea.append(subarea)
                        ids.append(article[0])
                        x[subarea].append(article[0])
                        editors.append(article[2])
                        ano.append(str(int(article[1].split('/')[-3]) + 1903))
                        edicao.append(article[1].split('/')[-2])
                        if ListedEditors is not None:
                            if article[2] in ListedEditors:
                                possivel.append('1')
                            else:
                                possivel.append('0')
        df = pd.DataFrame()
        df['SubArea'] = subArea
        df['ano'] = ano
        df['Edicao'] = edicao
        df['Editor'] = editors
        df['ID'] = ids
        if ListedEditors is not None:
            df['Listado'] = possivel
        return df
    else:
        Articles = []
        for file in os.listdir('2019'):
            dic = pickle.load(open('2019' + file, 'rb'))
            for subsecao in dic.keys():
                for article in dic[subsecao]:
                    Articles.append([subsecao, article[2], article[0]])

        return Articles


if __name__ == '__main__':

    getArticles2019(True, getListedEditors()).to_csv('Articles.csv', sep=';', encoding = 'utf-8', index = False)
    pass


# 10 entraram e 2 sairam

