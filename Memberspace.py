from selenium import webdriver
from configparser import ConfigParser

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
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            self.driver_path, options=self.chrome_options)
        self.login_url = 'https://admin.memberspace.com/member/sign_in'
        self.LOGGED_IN = False

    def login(self):
        if not self.LOGGED_IN:
            self.driver.get(self.login_url)
            email_box = self.driver.find_element_by_xpath('//*[@id="email"]')
            password_box = self.driver.find_element_by_xpath(
                '//*[@id="password"]')
            login_btn = self.driver.find_element_by_class_name('just-login')
            email_box.send_keys(self.email)
            password_box.send_keys(self.password)
            login_btn.click()


memberSpace = MemberSpace()
memberSpace.login()
