# -*- coding: utf-8 -*-
from __future__ import print_function


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import io
import urllib.request 
import pymysql
import validators

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
print("Initializing Script")



class DBConnection():

    def __init__(self):

        #Add mysql database or creds here [USERNAME; PASSWORD; DATABASE]
        self.db = pymysql.connect(host="localhost", 
                     user="root",        
                     password="root",  
                     db="whatsapp",
                     use_unicode=True,
                     charset='utf8mb4') 
        self.cursor = self.db.cursor()
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute("SET CHARACTER SET utf8mb4")
        self.cursor.execute("SET character_set_connection=utf8mb4")
        self.USER_LIST = []
    
    def close_connection(self):
        self.db.close()


class ChromeBrowser():

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage");
        self.chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

        #Add google_chrome here
        self.chrome_options.add_argument("user-data-dir=/home/dexter/.config/google-chrome/") 
        
        #Add Chrome Driver Path here
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path="/home/dexter/chromedriver")

        self.driver.get('http://web.whatsapp.com')
        time.sleep(10)

    def check_connection(self):
        for el in range(5):
            try:
                ele = self.driver.find_element_by_xpath('//span[@data-icon = "{}"]'.format('alert-phone'))
                time.sleep(5)
                if el == 9:
                    print("closing connection!!")
                    self.driver.close()
            except Exception as e:
                break

    def close_driver(self):
        self.driver.close()

    def send_msg(self, text):
        msg_box = self.driver.find_element_by_class_name('_2S1VP')
        for part in text.split('\n'):
            msg_box.send_keys(part)
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
        button = self.driver.find_element_by_class_name('_35EW6')
        button.click()


def get_messages(connection, browser):
    browser.check_connection()
    unread_msg_users = browser.driver.find_elements_by_class_name('OUeyt')
    for unread_msg_user in unread_msg_users:
        no_of_msgs = int(unread_msg_user.text)
        unread_msg_user.find_element_by_xpath('../../../../..').click()

        already_loaded_msg = 3

        if(no_of_msgs > already_loaded_msg ):
            
            t_c = len(browser.driver.find_elements_by_class_name('vW7d1'))

            while(t_c<no_of_msgs):
                #Scroll down
                scrn = browser.driver.find_element_by_class_name('_2nmDZ')
                scrn.send_keys(Keys.END)

                #check total count
                t_c = len(browser.driver.find_elements_by_class_name('vW7d1'))

            import pdb; pdb.set_trace()

        srn_t_c = browser.driver.find_elements_by_class_name('message-in')
        srn_t_c = srn_t_c[::-1]

        m_no = no_of_msgs

        while(0 < m_no):
            m_no= m_no-1
            msg = srn_t_c[m_no]
            
            try:
                in_text = msg.find_element_by_class_name('selectable-text').text

                #TODO CFG Grammer to find suitable answer for question
                if(in_text != '' ):
                    reply = connection.cursor.execute("SELECT output_val FROM reply_user where input_val LIKE '%{0}%';".format(in_text))

                    if(reply != 0):
                        row = connection.cursor.fetchone()
                        text = row[0].lower()
                        browser.send_msg(text)

            except Exception as e:
                print("Error Occur >>", e)
                continue

    print("All work done.")


if __name__ == '__main__':
    browser = ''
    connection = ''

    connection = DBConnection()
    browser = ChromeBrowser()

    get_messages(connection, browser)

    if browser:
        browser.close_driver()
    connection.close_connection()
    print("End Script >> Connections Closed.")
