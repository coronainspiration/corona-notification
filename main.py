'''
Project Name : corona_notification
Technology : Python Webscrapping
Packages : selenium(for web scrapping)
            plyer(for notification)
            gtts(for text to speech conversion)
            pyglet(for playing sound in playback)
            pandas(for storing data in csv format)
Author : Chintan A Bhatt
Date : 05/12/2020(dd/mm/yy)
'''

from plyer import notification
from gtts import gTTS
import pyglet
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
from time import sleep

def notify_me(msg):
    message = 'State : ' + msg[0] + 'Number of Active Cases : ' + msg[1] + 'Number of Deaths : ' + msg[2] + 'Source : ' + msg[3]
    language ='en'

    output = gTTS(text=message, lang=language, slow = False)
    output.save('output.mp3')
    music = pyglet.media.load('output.mp3', streaming=False)
    music.play()
    notification.notify(
        title='State : ' + msg[0],
        message='Number of Active Cases : ' + msg[1] + '\nNumber of Deaths : ' + msg[2] + '\nSource :' + msg[3],
        app_icon='stopcorona.ico',
        app_name = 'corona_notification',
        ticker = 'Chintan A Bhatt',
        timeout = 50
    )
    sleep(music.duration)
    os.remove('output.mp3')


if __name__ == "__main__":

    #below three code for hide chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver',options=options)

    url = 'https://covidindia.org/'
    driver.get(url)
    timeout = 60
    try:
        WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.ID, "tablepress-96")))
    except TimeoutException:
        driver.quit()

    ###Select 50 value in select option###
    #open dropdown
    dropdown = driver.find_element_by_xpath('//*[@id="tablepress-96_length"]/label/select')
    dropdown.click()
    #select value
    item = dropdown.find_element_by_xpath('//*[@id="tablepress-96_length"]/label/select/option[3]')
    item.click()

    case_status = driver.find_element_by_id('tablepress-96')
    case_status1 = case_status.find_element_by_xpath('//*[@id="tablepress-96"]/tbody')
    case_status2 = case_status1.find_elements_by_xpath('//*[@id="tablepress-96"]/tbody/tr')
    states = []
    cases = []
    recoveries = []
    deths = []
    msg = []
    for c in case_status2:
        get_state = c.find_element_by_class_name('column-1').text
        get_cases = c.find_element_by_class_name('column-2').text
        get_recoveries = c.find_element_by_class_name('column-3').text
        get_deths = c.find_element_by_class_name('column-4').text
        if (get_state == 'Gujarat'):
            msg.append(get_state)
            msg.append(get_cases)
            msg.append(get_deths)
            msg.append(url)

        states.append(get_state)
        cases.append(get_cases)
        recoveries.append(get_recoveries)
        deths.append(get_deths)

    #close and quit browser
    driver.close()
    driver.quit()

    data = {'State':states,'Cases':cases,'Recover':recoveries,'Deths':deths}
    notify_me(msg)
    df = pd.DataFrame.from_dict(data)
    df.to_csv('cases.csv')