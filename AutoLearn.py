import itertools
import sys
import threading
import time
from os import system
from random import uniform

import inquirer
import pandas as pd
import six
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import warnings
from pyfiglet import figlet_format, fonts
from PyInquirer import Token, prompt, style_from_dict

warnings.filterwarnings(action='ignore')

import colorama

colorama.init()
from termcolor import colored

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

def ask_pill():
    questions = [
        inquirer.List('pill',

                      choices=['\033[1;34mBLUE PILL', '\033[1;31mRED PILL'],
                      ),
    ]

    return inquirer.prompt(questions)['pill']


def typewriter(lines):
    print('\033[1;32m')
    system('cls')
    for line in lines:
        print(line, end='')

        sys.stdout.flush()
        sleep(uniform(0, 0.3))

        if line == '\n':
            system('cls')
    system('cls')
    print('\033[0;0m')


def ending(lines):
    print('\033[1;32m')

    try:
        system('cls')
        for line in lines:
            print(line, end='')

            sys.stdout.flush()
            sleep(uniform(0, 0.3))

            if line == '\n':
                system('cls')

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:

        print('\033[0;0m')
        system('cls')
        sys.exit()

def wake_up_neo(lines):
    print('\033[1;32m')

    try:
        system('cls')
        for line in lines:
            print(line, end='')

            sys.stdout.flush()
            sleep(uniform(0, 0.3))

            if line == '\n':
                system('cls')

        answer = ask_pill()

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:

        sys.exit() if answer == '\033[1;34mBLUE PILL' else 1
        print('\033[0;0m')
        system('cls')




def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def askAccountInformation():
    questions = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'ID',
            'default': '12113952'
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Password',
            'default': 'Asdasd!@3'
        }
    ]

    answers = prompt(questions, style=style)
    return answers


def get_sec(time_str):
    """Get Seconds from time."""
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)


def waiting():

    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r             ')

def class_attend(a):
    link = a['href']
    class_id = link[link.find('id=') + len('id='):]
    class_name = a.select('div.course-name > div.course-title > h3')[0].contents[0]
    br.get(link)
    try:
        WebDriverWait(br, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
        alert = br.switch_to.alert
        alert.accept()
    except TimeoutException:
        pass

    sleep(0.1)
    html = br.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select(
        'div.course_box.course_box_current > ul > li> div.content > ul > li.activity.vod.modtype_vod > div > div > div:nth-child(2) > div')

    try:
        week_text = soup.select('div.course_box.course_box_current > ul > li> div.content >h3>span>a')[0]['href']
        week = week_text[week_text.find('section-') + len('section-'):]
        br.get(f'https://learn.inha.ac.kr/report/ubcompletion/user_progress_a.php?id={class_id}')
        html = br.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find_all('table')
        attend_df = pd.read_html(str(table))[1]
        attend_df = attend_df[attend_df.iloc[:, 0] == int(week)]
        attend_list = attend_df['출석'].tolist()
        done = True
        sleep(0.1)
        system('cls')

        print(class_name, 'for this week :\n')
        links_to_attend = []
        # print title, duration of vid
        for link, attend in zip(links, attend_list):
            color = 'green' if attend == 'O' else 'red'
            if attend == 'O':
                color = 'green'
            else:
                color = 'red'
                links_to_attend.append(link)
            title = link.find('span').contents[0]
            duration = link.find_all('span')[-1].text.split()[-1]
            log(f'강의명 : {title}, 시간 :{duration}, 출석여부 : {attend}', color)
    except:
        print('출석 에러')


done = False
lines = 'Welcome to Coursemos'
typewriter(lines)

log("Coursemos", color='red', figlet=True)
# accountInfo = askAccountInformation()
# USERNAME = accountInfo.get("username")
# PASSWORD = accountInfo.get("password")

f = open("account.txt", "r")
lines = f.readlines()

USERNAME = lines[0].replace("\n", '')
PASSWORD = lines[1].replace("\n", '')

f.close()



chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

br = webdriver.Chrome('./chromedriver', options=chrome_options)  # 드라이버 로드
# br = webdriver.Chrome('./driver/chromedriver')  # 드라이버 로드
br.get('https://learn.inha.ac.kr/login.php')  # 해당 url로 이동

# 이메일과 비밀번호를 입력
br.find_element(by='name',value='username').send_keys('12113952')
br.find_element(by='name', value='password').send_keys('Asdasd!@3')
br.find_element(by='name',value='loginbutton').click()

html = br.page_source
soup = BeautifulSoup(html, 'html.parser')

username = soup.select('li.user_department.hidden-xs')[0].text

lines = f"""Wake up, {username}...
The Matrix has you...
Follow the white rabbit.
Knock, knock, {username}.
Remember, all I’m offering is the truth, nothing more."""

# t = threading.Thread(target=wake_up_neo(lines))
# t.start()


# sentence = 'Welcome to Inha University'
# #log('\nWelcome to Inha University', 'green')
# i = 0
# while i <= len(sentence):
#     log('\r'+sentence[:i], 'green')
#     sys.stdout.flush()
#     sleep(0.1)
#     i += 1


# get class id
for a in soup.select('div.course_lists > ul')[0].find_all('a', href=True):


    link = a['href']
    class_id = link[link.find('id=') + len('id='):]
    class_name = a.select('div.course-name > div.course-title > h3')[0].contents[0]
    br.get(link)
    try:
        WebDriverWait(br, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
        alert = br.switch_to.alert
        alert.accept()
    except TimeoutException:
        pass

    sleep(0.1)
    html = br.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select(
        'div.course_box.course_box_current > ul > li> div.content > ul > li.activity.vod.modtype_vod > div > div > div:nth-child(2) > div')

    try:

        week_text = soup.select('div.course_box.course_box_current > ul > li> div.content >h3>span>a')[0]['href']
        week = week_text[week_text.find('section-') + len('section-'):]
        links_to_attend = [0]

        while len(links_to_attend) > 0:
            br.get(f'https://learn.inha.ac.kr/report/ubcompletion/user_progress_a.php?id={class_id}')
            try:
                WebDriverWait(br, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')
                alert = br.switch_to.alert
                alert.accept()
            except TimeoutException:
                pass
            html = br.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find_all('table')
            attend_df = pd.read_html(str(table))[1]
            attend_df = attend_df[attend_df.iloc[:, 0] == int(week)]
            attend_list = attend_df['출석'].tolist()
            done = True
            sleep(0.1)
            system('cls')

            print(class_name, 'for this week :\n')
            links_to_attend = []
            # print title, duration of vid
            for link, attend in zip(links, attend_list):
                color = 'green' if attend == 'O' else 'red'
                if attend == 'O':
                    color = 'green'
                else:
                    color = 'red'
                    links_to_attend.append(link)
                title = link.find('span').contents[0]
                duration = link.find_all('span')[-1].text.split()[-1]
                log(f'강의명 : {title}, 시간 :{duration}, 출석여부 : {attend}', color)


            # open vid link and play each

            i = links_to_attend[0]

            title = i.find('span').contents[0]
            duration = i.find_all('span')[-1].text.split()[-1]
            remaining_time = 1000

            link = i.findChild("a").attrs["href"]
            link = link.replace("view", "viewer")

            br.get(link)
            done = False
            t = threading.Thread(target=waiting)
            t.start()

            try:
                WebDriverWait(br, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')
                alert = br.switch_to.alert
                alert.accept()
            except TimeoutException:
                pass
            try:
                WebDriverWait(br, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')
                alert = br.switch_to.alert
                alert.accept()
            except TimeoutException:
                pass

            WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#my-video > button')))

            br.find_element(By.CSS_SELECTOR,'#my-video > button').click()

            WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#my-video > div.vjs-control-bar > div.vjs-remaining-time.vjs-time-control.vjs-control > span.vjs-remaining-time-display')))
            done = True
            sleep(0.1)

            print()
            while remaining_time > 0:
                html = br.page_source
                soup = BeautifulSoup(html, 'html.parser')
                remaining_time = soup.select('#my-video > div.vjs-control-bar > div.vjs-remaining-time.vjs-time-control.vjs-control > span.vjs-remaining-time-display')[-1].text
                remaining_time = remaining_time.replace('-', '')

                print(f"현재 재생중 : {title}, 남은시간 : {colored(remaining_time, 'green')}", end='\r')
                remaining_time = get_sec(remaining_time)

                '''
                try:  # used try so that if user pressed other than the given key error will not be shown
                    if keyboard.is_pressed(' '):  # if key space is pressed.You can also use right,left,up,down and others like a,b,c,etc.
                        print('\n 다음 동영상으로 넘어갑니다.')
                        i=10000
                        break  # finishing the loop
                except:
                    pass
                '''
            sleep(0.5)
    except:
        system('cls')
        print(class_name, 'no class for this week :\n')
        sleep(2)

lines = """I know you're out there. 
I can feel you now. 
I know that you're afraid. 
You're afraid of us. 
You're afraid of change. 
I don't know the future. 
I didn't come here to tell you how this is going to end. 
I came here to tell you how it's going to begin. 
I'm going to hang up this phone, and then I'm going to show these people what you don't want them to see. 
I'm going to show them a world.. without you. 
A world without rules or controls, without borders or boundaries. 
A world where anything is possible. 
Where we go from there is a choice I leave to you."""
# ending(lines)
br.close()
