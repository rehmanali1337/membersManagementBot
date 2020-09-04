from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as seleniumExceptions
from configparser import ConfigParser
import logging
import glob
import time
import os

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)


class MemberSpace:
    def __init__(self):
        config = ConfigParser()
        config.read('conf.ini')
        self.email = config['MEMBERSPACE']['email']
        self.password = config['MEMBERSPACE']['password']
        self.driver_path = config['CHROME']['chromedriver_path']
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        preferences = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": os.getcwd()+'/tmps',
            "directory_upgrade": True
        }
        chrome_options.add_experimental_option('prefs', preferences)
        # chrome_options.add_argument("download.default_directory=./tmps")
        self.driver = webdriver.Chrome(
            self.driver_path, options=chrome_options)
        self.login_url = 'https://admin.memberspace.com/member/sign_in'
        self.sites_url = 'https://admin.memberspace.com/sites/'
        self.LOGGED_IN = False

    def login(self):
        if not self.LOGGED_IN:
            logging.info('Logging in to website...')
            self.driver.get(self.login_url)
            email_box = self.driver.find_element_by_xpath('//*[@id="email"]')
            password_box = self.driver.find_element_by_xpath(
                '//*[@id="password"]')
            login_btn = self.driver.find_element_by_class_name('just-login')
            email_box.send_keys(self.email)
            password_box.send_keys(self.password)
            login_btn.click()
            while True:
                try:
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div[1]/div/ul/li/a/strong'))
                    )
                except seleniumExceptions.TimeoutException:
                    logging.info('Timeout waiting for element!')
                    continue
                finally:
                    logging.info('Login Successfull!')
                    self.LOGGED_IN = True
                    break

    def goto_home(self):
        self.driver.get(self.sites_url)
        try:
            site = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/ul/li/a'))
            )
        finally:
            site.click()

    def get_paid_list(self):
        if not self.LOGGED_IN:
            self.login()
        else:
            self.goto_home()
        logging.info('Getting list of paid members ...')
        try:
            paid_members_btn = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/section/h3[1]/a'))
            )
        finally:
            paid_members_btn.click()

        try:
            export_options = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/section[1]/form/div[2]/a'))
            )
        finally:
            export_options.click()

        try:
            condensed_file = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/section[1]/form/section/div[1]/button'))
            )
        finally:
            condensed_file.click()
            time.sleep(2)
            lst = glob.glob(f"{os.getcwd()}/tmps/*")
            for element in lst:
                logging.info(f'Renaming {element}')
                os.rename(element, f"{os.getcwd()}/Members/paidList.csv")

    def get_ontrial_list(self):
        if not self.LOGGED_IN:
            self.login()
        else:
            self.goto_home()
        logging.info('Getting list of on-trial members ...')
        try:
            on_trial_btn = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/section/h3[2]/a'))
            )
        finally:
            on_trial_btn.click()

        try:
            export_options = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/section[1]/form/div[2]/a'))
            )
        finally:
            export_options.click()

        try:
            condensed_file = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/section[1]/form/section/div[1]/button'))
            )
        finally:
            condensed_file.click()
            time.sleep(2)
            lst = glob.glob(f"{os.getcwd()}/tmps/*")
            for element in lst:
                logging.info(f'Renaming {element}')
                os.rename(element, f"{os.getcwd()}/Members/onTrialList.csv")


memberSpace = MemberSpace()
memberSpace.login()
memberSpace.get_paid_list()
memberSpace.get_ontrial_list()
