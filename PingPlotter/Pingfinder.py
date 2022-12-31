from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import random
import matplotlib.pyplot as plt
def check(name):
    return name[:7] == 'Channel'


noofpings = int(input("How many pings would you like to make?"))

N_TRIES = min(60**2, noofpings)
matr = np.zeros([N_TRIES, 30])
def check(name):
    return name[:7] == 'Channel'
row = 0
while row < N_TRIES:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    link_template = f'https://xymu.github.io/maple.watch/#GMS-Reboot'
    driver = webdriver.Chrome(r'chromedriver.exe', options=options) ###########################THIS IS WHERE YOU EDIT THE FILE PATH TO BE FOR YOUR CHROMEDRIVER
    driver.get(link_template)
    no = 4.5
    try:
        WebDriverWait(driver, no).until(EC.presence_of_element_located((By.CLASS_NAME, 'container item__body--uZhP-')))
    except TimeoutException:
        print(f'Page timed out after {no} secs.')
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()
    LEN = len(soup.find_all("article", {"class":"slow"}))
    source = [soup.find_all("article", {"class":"slow"})[x].span.text for x in range( LEN) if check(soup.find_all("article", {"class":"slow"})[x].span.text)]
    PING = [int(soup.find_all("article", {"class":"slow"})[x].find('div', {'class':'time'}).text[:-2]) for x in range(LEN) if check(soup.find_all("article", {"class":"slow"})[x].span.text)]
    channels = []
    counterofchannels = 0
    for i in source:
        if check(i):
            counterofchannels += 1
            channels.append(int(i.split(' ')[-1]))
    # min(channels)
    try:
        number = min(channels)-1
        for j in channels:
            try:matr[row][j-1] += PING[number]
            except:print(f"row is {row}, j-1 is {j-1}, number is {number}, length of matr is {len(matr)}, len(PING) is {len(PING)}")
            # print(len(PING), max(channels))
            number+=1
        row+=1
    except:
        pass
STD = [np.std([ping[channel] for ping in matr if ping[channel]!=0]) for channel in range(len(source))]
std = int(input("What standard deviation cap do you want to filter through the channels, shisho? o3o"))
lowvar_channels = [int((source[channel]).split(" ")[-1]) for channel in range(len(source)) if STD[channel]<std ]
x_axis = np.arange(1,N_TRIES+1) #####################
linestyle_tuple = [
 ((0, (1, 10))),
 ((0, (1, 1))),
 ((0, (1, 1))),
 ((0, (5, 10))),
 ((0, (5, 5))),
 ((0, (5, 1))),
 ((0, (3, 10, 1, 10))),
 ((0, (3, 5, 1, 5))),
 ((0, (3, 1, 1, 1))),
 ((0, (3, 5, 1, 5, 1, 5))),
 ((0, (3, 10, 1, 10, 1, 10))),
 ((0, (3, 1, 1, 1, 1, 1)))]
if int(noofpings)<21:plt.figure(figsize=(15,8))
else:plt.figure(figsize=(25,10))
plt.clf()
plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for idx, row in enumerate(np.transpose(matr[:,[int(x-1) for x in lowvar_channels]])): #@@7z Note lowvar_channels is a list of channels that are NOT indices but actual channel numbers
    plt.grid(color='#2A3459')
    tem = " "
    for i in lowvar_channels:tem+=str(i) + ", "
    plt.title(f"Channels {tem}")
    number_of_colors = len(source)
    C0L = random.choice(["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])for i in range(number_of_colors)])
    MARK = random.choice([".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "d", "D", "|", "_"])
    size = 12 #marker size
    plt.plot(x_axis, row, label = f" Ch {lowvar_channels[idx]}", linestyle = random.choice(linestyle_tuple), marker = MARK, linewidth = 2.5, color = C0L, ms = size)
    n_lines = 15
    diff_linewidth = 1.02
    alpha_value = 0.02 #0.03
    for n in range(1, n_lines+1):
        plt.plot(x_axis,row,
                linewidth=2+(diff_linewidth*n),
                alpha=alpha_value,
                color=C0L, ms = size)
    leg = plt.legend(loc='best', ncol=2, shadow=True, fancybox=True, prop={'size': 15})
    leg.get_frame().set_alpha(0.7)
    plt.xlabel("Ping attempts")
    plt.ylabel("User localized ping/ms")
plt.savefig(fname='plot')
plt.show()
# os.remove('plot.png') ############
