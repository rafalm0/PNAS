from selenium import webdriver
from selenium.common import exceptions
import pickle
import os


driver = webdriver.Firefox()

join = False

inicio = 2019
fim = 2020

# apartir do volume 101 tem 52 issues, antes disso , 26

issues = ['biological', 'social', 'physical']

Content_numbers = [[str(b-1903), [str(issue_int) for issue_int in list(range(1, 27 if b-1903 < 101 else 53))]] for b in list(range(inicio, fim))]

links_selector_geral = ".issue-toc-section[class*='physical'] .toc-section a.highwire-cite-linked-title,.issue-toc-section[class*='social'] .toc-section a.highwire-cite-linked-title,.issue-toc-section[class*='biological'] .toc-section a.highwire-cite-linked-title"
# links_selector_physical = ".issue-toc-section[class*='physical'] .toc-section a.highwire-cite-linked-title"
# links_selector_social = ".issue-toc-section[class*='social'] .toc-section a.highwire-cite-linked-title"
# links_selector_biological = ".issue-toc-section[class*='biological'] .toc-section a.highwire-cite-linked-title"

article_classification_selector = '.pane-highwire-article-cat-hierarchy > div:nth-child(2)'

contents = {}

if not os.path.exists('articles'):
    os.mkdir('articles')

for content in Content_numbers:
    if content[0] not in contents:
        contents[content[0]] = {}
    for issue in content[1]:
        if os.path.exists('dev/artigos/all/articles_' + content[0] + '_' + issue + '.pickle'):
            print('-')
            continue
        if issue not in contents[content[0]].keys():
            contents[content[0]][issue] = {}
        try:
            driver.get('https://www.pnas.org/content/' + content[0] + '/' + issue)

            # -------------------------------------------------------------------------------------------------------------#
            geral_elements_list = driver.find_elements_by_css_selector(links_selector_geral)
            geral_link_list = []

            # physical_elements_list = driver.find_elements_by_css_selector(links_selector_physical)
            # physical_link_list = []
            #
            # social_elements_list = driver.find_elements_by_css_selector(links_selector_social)
            # social_link_list = []
            #
            # biological_elements_list = driver.find_elements_by_css_selector(links_selector_biological)
            # biological_link_list = []

            # -----------------------------------------------------------------------------------------------------------#

            for element in geral_elements_list:
                element_link = element.get_attribute('href')
                geral_link_list.append(element_link)

            # for element in physical_elements_list:
            #     element_link = element.get_attribute('href')
            #     physical_link_list.append(element_link)
            #
            # for element in biological_elements_list:
            #     element_link = element.get_attribute('href')
            #     biological_link_list.append(element_link)
            #
            # for element in social_elements_list:
            #     element_link = element.get_attribute('href')
            #     social_link_list.append(element_link)

            # -----------------------------------geral----------------------------------------------------#

            for link in geral_link_list:
                article_editor = None
                article_sections = []
                article_ID = link.split('/')[-1]
                article_link = link

                try:
                    driver.get(link)
                except exceptions.TimeoutException:
                    driver.get(link)
            #  ----------------------- conseguindo nome do editor ------------------------------------#

                # try:
                #     text = driver.find_element_by_css_selector('#p-1').text
                # except exceptions.NoSuchElementException:
                #     try:
                #         text = driver.find_element_by_css_selector('#p-2').text
                #     except exceptions.NoSuchElementException:
                #         text = None
                # if text is None:
                #     continue
                # else:
                #     if ('Edited by' in text) and (', and approved' in text):
                #         article_editor = text.split(', and approved')[0].split('Edited by ')[1].split(',')[0]
                #     else:
                #         try:
                #             text = driver.find_element_by_css_selector('#p-2').text
                #         except exceptions.NoSuchElementException:
                #             continue
                text = None
                tentativa = 0
                while text is None:
                    if tentativa == 0:
                        try:
                            text = driver.find_element_by_css_selector('#p-1').text
                            if ('Edited by' in text) and ((', and approved' in text) or (', and accepted' in text)):
                                if ', and approved' in text:
                                    article_editor = text.split(', and approved')[0].split('Edited by ')[1].split(',')[0]
                                else:
                                    article_editor = text.split(', and accepted')[0].split('Edited by ')[1].split(',')[0]
                            else:
                                tentativa = tentativa + 1
                                text = None
                        except exceptions.NoSuchElementException:
                            tentativa = tentativa + 1
                            text = None
                    elif tentativa == 1:
                        try:
                            text = driver.find_element_by_css_selector('#p-2').text
                            if ('Edited by' in text) and ((', and approved' in text) or (', and accepted' in text)):
                                if ', and approved' in text:
                                    article_editor = text.split(', and approved')[0].split('Edited by ')[1].split(',')[0]
                                else:
                                    article_editor = text.split(', and accepted')[0].split('Edited by ')[1].split(',')[0]
                            else:
                                tentativa = tentativa + 1
                                text = None
                        except exceptions.NoSuchElementException:
                            tentativa = tentativa + 1
                            text = None
                    elif tentativa > 1:
                        break
                if text is None:
                    continue
                #  ---------------------------------------------------------------------------------------#

                try:
                    sectionbox = driver.find_element_by_css_selector(article_classification_selector)
                except exceptions.NoSuchElementException:
                    sectionbox = None

                if sectionbox is not None:
                    try:
                        sections = sectionbox.find_elements_by_tag_name('a')
                    except exceptions.NoSuchElementException:
                        sections = []

                    for section in sections:
                        article_sections.append(section.text)
                        if section.text not in contents[content[0]][issue].keys():
                            contents[content[0]][issue][section.text] = []

                for section in article_sections:
                    contents[content[0]][issue][section].append([article_ID, article_link, article_editor])
        except exceptions.NoSuchWindowException:
        # except:
            driver = webdriver.Firefox()
            continue

        # ------------------------------------------------------------------------------------------------------------#

        if len(list(contents[content[0]][issue].keys())) == 0:
            break
        pickle.dump(contents[content[0]][issue], open('dev/artigos/all/articles/articles_' + content[0] + '_' + issue + '.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)

    # ------------------------------------------------------------------------------------------------------------#

if join:
    contents = {}
    for content in Content_numbers:
        if content[0] not in contents:
            contents[content[0]] = {}
        for issue in content[1]:
            contents[content[0]][issue] = pickle.load(open('dev/artigos/all/articles/articles_' + content[0] + '_' + issue + '.pickle', 'rb'))

    pickle.dump(contents, open('dev/artigos/all/articles/allArticles.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)

driver.close()



# quantAreas = {}
# for article in os.listdir('articles'):
#     revista = pickle.load(open('articles/' + article,'rb'))
#     for subarea in revista.keys():
#         if subarea not in quantAreas.keys():
#             quantAreas[subarea] = []
#         for artigo in revista[subarea]:
#             if artigo[2] not in quantAreas[subarea]:
#                 quantAreas[subarea].append(artigo[2])

# dicionarioArea = {}
# for file in os.listdir('editores'):
#     arquivo = open('editores/' + file ,'r',encoding='utf-8')
#     for nome in arquivo:
#         nomestriped = nome.rstrip()
#         if '\ufeff' in nomestriped:
#             nomestriped = nomestriped.replace('\ufeff','')
#         if nomestriped not in dicionarioArea:
#             dicionarioArea[nomestriped] = []
#         if file not in dicionarioArea[nomestriped]:
#             dicionarioArea[nomestriped].append(file.split('.')[0])
