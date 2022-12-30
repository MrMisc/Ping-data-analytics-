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
power = int(input("What order of magnitude norm, would you like to test for? Put higher values like 5 or above to test for big, intermittent spikes specifically! 2 would be to replicate typical standard deviation/mean squared error tests..."))
N_TRIES = min(60**2, int(noofpings))
matr = np.zeros([N_TRIES, 30])
def check(name):
    return name[:7] == 'Channel'
row = 0
while row < N_TRIES:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    link_template = f'https://xymu.github.io/maple.watch/#GMS-Reboot'
    driver = webdriver.Chrome(r'CHANGETOPATHHERE', options=options)
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
if int(power)==2:STD = [np.std([ping[channel] for ping in matr if ping[channel]!=0]) for channel in range(len(source))]
else:
    MEAN = [np.mean([ping[channel] for ping in matr if ping[channel]!=0]) for channel in range(len(source))]
    MINUS = [np.array(matr[:, channel]) /MEAN[channel] for channel in range(len(source))]
    def norm(array, dyn):
        sum=0
        for thing in array:
            sum+=thing**dyn
        return sum**(1/dyn)
    STD = [norm(error, int(power)) for error in MINUS]
lowvar_channels = [int((source[channel]).split(" ")[-1]) for channel in range(len(source))]
PARENT = sorted(zip(STD,lowvar_channels))
channelsordered = [lowvar_channels for __,lowvar_channels in PARENT]
testnumbers = [__ for __,lowvar_channels in PARENT]
stringie = ''
for i in range(len(channelsordered)):
    stringie += "Channel " + f"{channelsordered[i]}" +f" : [L{power} norm of {testnumbers[i]}]" '\n'
print(f"{stringie}  ")
