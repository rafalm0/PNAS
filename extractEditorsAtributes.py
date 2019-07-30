from selenium import webdriver
from selenium.common import exceptions
import time
import pandas as pd
import pickle
import os

def tudo():
    login = 'rafu256'
    key = 'Rafael@1'

    pnasSite = 'https://www.pnascentral.org/cgi-bin/main.plex?form_type=logout'
    # googleSite = 'https://scholar.google.com/citations?hl=pt-BR&view_op=search_authors&mauthors=&btnG='

        # ----------- acessando login ---------------#

    driver = webdriver.Firefox()
    # driverGoogle = webdriver.Firefox()
    # driverGoogle.get(googleSite)
    driver.get(pnasSite)

    driver.maximize_window()

        # ---- limpando verificador de cookie -----#

    driver.implicitly_wait(2)
    continue_button = None
    try:
        continue_button = driver.find_element_by_id('continue-btn')
    except exceptions.NoSuchElementException:
        continue_button = None
    if continue_button is not None:
        continue_button.click()

        # --------- fazendo login -----------------#

    username = driver.find_element_by_id('login')
    password = driver.find_element_by_name('password')
    submit = driver.find_element_by_id('submit_login')

    username.send_keys(login)
    password.send_keys(key)
    submit.click()

        # --------- entrando no artigo incompleto pra ir para a pagina com editores -----------------#

    continue_button = None
    try:
        continue_button = driver.find_element_by_id('DisplayTasks-add_ndt_task-7918-3')
    except exceptions.NoSuchElementException:
        continue_button = None
    if continue_button is not None:
        continue_button.click()

        # --------- entrando no artigo incompleto pra ir para a pagina com editores -----------------#

    continue_button = None
    try:
        continue_button = driver.find_element_by_id('ViewMs-vms_add_task_expandable-20799-3')
    except exceptions.NoSuchElementException:
        continue_button = None
    if continue_button is not None:
        continue_button.click()

        # --------- entrando no artigo incompleto pra ir para a pagina com editores -----------------#

    continue_button = None
    try:
        continue_button = driver.find_element_by_css_selector('#tab_suggestions > span:nth-child(2)')
    except exceptions.NoSuchElementException:
        continue_button = None
    if continue_button is not None:
        continue_button.click()
    driver.implicitly_wait(5)

        # --------- entrou na pagina com os editores, iniciando a extracao de dados -----------------#

    searchButton = driver.find_element_by_id('potmes_include_searchlink_sa')
    tabSearchButton = driver.find_element_by_css_selector('#potmes_include_dualselect > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)')

        # --------- pegando quantidade de subareas que precisam ser iteradas  -----------------#

    searchButton.click()
    subAreasList = tabSearchButton.find_element_by_class_name('salist').find_elements_by_class_name('sa')
    viewMenbers = driver.find_element_by_id('potmes_include_search_sa_view')
    for element in subAreasList:
        translatorListed = []
        translatorOrganized = []
        translatorInstitution = []
        time.sleep(1)
        subAreaName = element.text
        if os.path.exists('dev/editores/tradutor/' + subAreaName + '.csv'):
            continue
        element.click()
        viewMenbers.click()
        listaEditores = driver.find_element_by_id('potmes_include_item_list').find_elements_by_class_name('item')
        time.sleep(0.5)
        for editor in listaEditores:

            time.sleep(2)
            NomeListado = editor.text
            # try:
            #     NomeListado = editor.text
            # except exceptions.StaleElementReferenceException:
            #     print('acabou o ' + subAreaName)
            #     break

            if NomeListado in translatorListed:
                continue
            openButton = editor.find_element_by_class_name('info')
            openButton.click()
            time.sleep(0.2)
            newWindow = driver.find_element_by_id('vsubmitlayer')
            try:
                nomeOrdenado = newWindow.find_element_by_css_selector('table.detailsTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text.split('\n')[0]
                instituicao = newWindow.find_element_by_css_selector('table.detailsTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text
            except exceptions.NoSuchElementException:
                nomeOrdenado = '-'
                instituicao = '-'
            except exceptions.StaleElementReferenceException:
                nomeOrdenado = ':'
                instituicao = ':'
            # closeButton = newWindow.find_element_by_class_name('close')
            translatorListed.append(NomeListado)
            translatorOrganized.append(nomeOrdenado)
            translatorInstitution.append(instituicao)
            time.sleep(1.5)
            # closeButton = driver.implicitly_wait(1.5)
            # closeButton = driver.implicitly_wait(5).until(find("vsubmit_member_info_close"))
            try:
                closeButton = driver.find_element_by_css_selector("#vsubmit_member_info_close")
            except exceptions.NoSuchElementException:
                try:
                    closeButton = driver.find_element_by_id("vsubmit_member_info_close")
                except exceptions.NoSuchElementException:
                    closeButton = driver.find_element_by_class_name("close")
            closeButton.click()
        df = pd.DataFrame()
        df['Ordenavel'] = translatorOrganized
        df['NomeListado'] = translatorListed
        df['Instituicao'] = translatorInstitution
        df.to_csv('dev/editores/tradutor/' + subAreaName + '.csv', sep = ';', encoding = 'utf-8', index = False)
        # file = open('dev/editores/lists/editores/' + subAreaName + '.txt', encoding = 'utf-8', mode = 'w')
        # for nome in translatorListed:
        #     file.write(nome + '\n')
        # file.close()
        time.sleep(0.3)
        searchButton.click()
        time.sleep(0.3)
        element.click()

    # df = pd.DataFrame()
    # df['Ordenavel'] = translatorOrganized
    # df['NomeListado'] = translatorListed
    # df['Instituicao'] = translatorInstitution
    # df.to_csv('translator.csv', sep=';', encoding = 'utf-8', index = False)
    driver.close()


if __name__ == '__main__':
    while True:
        try:
            tudo()
            break
        except exceptions.StaleElementReferenceException:
            continue
