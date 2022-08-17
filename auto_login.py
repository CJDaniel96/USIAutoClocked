import argparse
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AutoLogin:
    def __init__(self, login_url='https://eip.usiglobal.com/home', driver_path=r'D:\ChromeDriver\chromedriver.exe'):
        self.login_url = login_url
        self.driver = webdriver.Chrome(driver_path)

    def login(self, user_name, user_password):
        self.driver.get(self.login_url)

        time.sleep(2)

        user = self.driver.find_element_by_id('_58_login')
        password = self.driver.find_element_by_id('_58_password')
        user.send_keys(user_name)
        password.send_keys(user_password)
        password.send_keys(Keys.RETURN)
        time.sleep(2)

    def clock_in(self):
        self.driver.get('https://eip.usiglobal.com/group/tw/tac-')
        time.sleep(2)
        button = self.driver.find_element_by_id('_USIClockInOut_WAR_USIIDLOTportlet_clockInBtn')
        button.click()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        alert.accept()

        return datetime.now()

    def clock_out(self):
        self.driver.get('https://eip.usiglobal.com/group/tw/tac-')
        time.sleep(2)
        button = self.driver.find_element_by_id('_USIClockInOut_WAR_USIIDLOTportlet_clockOutBtn')
        button.click()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        alert.accept()

        return datetime.now()

    def logout(self):
        time.sleep(2)
        self.driver.close()
        self.driver.quit()

def main(username, password, clock_in_time='08:20:00', clock_out_time='17:40:00', work_start_time='08:30:00', work_end_time='17:30:00'):
    clock_in = datetime.strptime(clock_in_time, '%H:%M:%S')
    clock_out = datetime.strptime(clock_out_time, '%H:%M:%S')
    work_start = datetime.strptime(work_start_time, '%H:%M:%S')
    work_end = datetime.strptime(work_end_time, '%H:%M:%S')
    while True:
        print('Waiting for clocked time ...')
        if datetime.now().time() > clock_in.time() and datetime.now().time() < work_start.time():
            auto_login = AutoLogin()
            auto_login.login(
                username,
                password
            )
            clock_time = auto_login.clock_in()
            auto_login.logout()
            print(clock_time + ' Clocked in finish!')
            time.sleep(60 * 60 * 8)

        elif datetime.now().time() < clock_out.time() and datetime.now().time() > work_end.time():
            auto_login = AutoLogin()
            auto_login.login(
                username,
                password
            )
            clock_time = auto_login.clock_out()
            auto_login.logout()
            print(clock_time + ' Clocked out finish!')
            time.sleep(60 * 60 * 14)

        time.sleep(60 * 5)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse()
    main(args.username, args.password)
