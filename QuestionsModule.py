from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from xlwt import Workbook
import time
import os

def FindQuestions (driver,sheet,page):
    clicked_options=[]
    questions_df = pd.DataFrame(columns=['Name','ID','Value','Title'])
    website = bs(driver.page_source, 'html.parser')
    form = website.find('form')
    all_forms=website.findAll("div", {"class": "survey-page "})
    q_per_page=[]
    for f in all_forms:
        question_text = f.find_all('label', {"class": 'question-label'})
        q_per_page.append(len(question_text))

    questions = form.find_all('input')
    question_text= form.find_all('label',{"class" : 'question-label'})
    no_questions=len(question_text)
    english=np.empty([no_questions,3], dtype=object)
    for row in questions:
        name=row['name']
        title=row['title']
        id=row['id']
        value=row['data-value']
        questions_df= questions_df.append({'Name':name,'ID':id,'Value':value,'Title':title}, ignore_index=True)
    df = questions_df.groupby('Name')
    dfs=[df.get_group(x) for x in df.groups]
    i = 0

    for text in question_text:
        question_number = text['for']
        question_desc = text.get_text()
        english[i][0] = question_number
        english[i][1] = question_desc.replace('\r','').replace('\t','').replace('\n','')
        for options in dfs:
            if question_number in options.values:
                english[i][2]=options
        i += 1
    for checkbox in english:
        clicked_options.append(random_choice(checkbox[2])[0])

    print(clicked_options)
    welcome_text=website.find("div", {"class": "welcomeContainer"})
    welcome_text=welcome_text.find("div", {"class": "text"}).get_text(separator=" ").strip()
    print(welcome_text)
    pause_text=website.find(id="PausePage")
    pause_text=pause_text.find("div", {"class": "text"}).get_text(separator=" ").strip()
    print(pause_text)
    sheet.write(0,0,welcome_text)
    sheet.write(1,0,pause_text)
    for i in range(np.shape(english)[0]):
        k = 0
        question = english[i][1]
        question_options=english[i][2]
        sheet.write(i+3,k,question)
        print(np.shape(question_options))
        print(question_options['Title'])
        k=1
        for option in question_options['Title']:
            sheet.write(i+3, k, option)
            k+=1
    return clicked_options,q_per_page

'''
    english_language = pd.DataFrame(columns=['Text','Number'])
    for text in question_text:
        question_text =text.get_text()
        question_number = text['for']
        english_language = english_language.append({'Text':question_text,'Number':question_number}, ignore_index=True)
'''

def random_choice (options):
    box = options.sample()['ID']
    choice = box.values
    return choice.astype(str)

def Select_language (driver,link):
    website = bs(driver.page_source, 'html.parser')
    languages_list = website.find_all('button', attrs={'data-action':"selectLanguage"})
    wb = Workbook()
    if languages_list != [] :
        languages_list = languages_list
        for language in languages_list:
            sheet = wb.add_sheet(language['name'])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, language['id']))).click()
            Fill_Survey(driver, sheet)
            time.sleep(2)
            driver.get(link)
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
            time.sleep(2)

    else:
        sheet = wb.add_sheet("English")
        Fill_Survey(driver, sheet)

    driver.close()
    wb.save(os.getcwd()+'/Survey_Link_Questionnaire.xls')


def Fill_Survey(driver,sheet):
    page=0
    submit = "/html/body/div[2]/main/div[2]/div/div/form/div[2]/div/div/div[2]/a[2]"
    time.sleep(2)
    button_list,q_per_page = FindQuestions(driver, sheet, page)
    continue_btn = '/html/body/div[2]/main/div[2]/div/div/form/div[1]/div/div/div/div[3]/a[2]'
    continue_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, continue_btn)))
    survey_pages=driver.find_elements_by_class_name('survey-page')
    find_continues = driver.find_elements_by_tag_name("a")
    continue_buttons=[]
    for element in find_continues:
        if element.text == "CONTINUE":
            continue_buttons.append(element)
    print(continue_buttons)
    continue_btn.location_once_scrolled_into_view
    continue_btn.click()

    i=0
    for n in q_per_page:
        print(n)
        for k in range(n):
            print('The button is')
            print(button_list[i])
            test = '// *[ @ id = "q_77480_101"]'
            checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.ID, button_list[i])))
            time.sleep(0.5)
            # checkbox.find_element_by_xpath('..').click()
            checkbox = WebDriverWait(checkbox, 10).until(EC.visibility_of_element_located((By.XPATH, ('..')))).click()
            i=i+1
        find_continues = driver.find_elements_by_tag_name("a")
        for element in find_continues:
            if element.text == "CONTINUE":
                element.click()

    find_continues = driver.find_elements_by_tag_name("a")
    for element in find_continues:
        if element.text == "SUBMIT":
            element.click()
    time.sleep(2)
    submit_text=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text"))).text
    print(submit_text)
    sheet.write(2,0,submit_text)

def Compare_files():
    pd.ExcelFile('Survey_Link_Questionnaire.xls')
