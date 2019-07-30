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
        time.sleep(1)
        subAreaName = element.text
        if os.path.exists('dev/editores/lists/editores/' + subAreaName + '.txt'):
            continue
        element.click()
        viewMenbers.click()
        time.sleep(2)
        listaEditores = driver.find_element_by_id('potmes_include_item_list').find_elements_by_class_name('item')
        nomes = []
        for editor in listaEditores:
            nomes.append(editor)
        file = open('dev/editores/lists/editores/' + subAreaName + '.txt', encoding = 'utf-8', mode = 'w')
        first = True
        for editor in nomes:
            if first:
                file.write(editor.text)
                first = False
            else:
                file.write('\n' + editor.text)
        file.close()
        time.sleep(0.3)
        searchButton.click()
        time.sleep(0.3)
        element.click()
    driver.close()


if __name__ == '__main__':
    tudo()
    exit()
    while True:
        try:
            tudo()
            break
        except exceptions.StaleElementReferenceException:
            continue
