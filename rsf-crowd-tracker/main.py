from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import datetime
import time

url = "https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
repeat = 10 # number of minutes

options = webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(options=options)
browser.get(url)

while True:
    dt = datetime.datetime.now()
    try:
        containers = WebDriverWait(browser, 10).until(lambda x: x.find_elements(By.CLASS_NAME, "styles_fullness__rayxl"))
        container = containers[0]
        spans = container.find_elements(By.TAG_NAME, 'span')
        span = spans[0]
        fullness = int(span.text.split(' ')[0].split('%')[0])

        with open('log.txt', 'a') as f:
            dow = weekdays[dt.weekday()]
            hour = dt.hour
            min = dt.minute
            f.write('{},{},{}:{},{}\n'.format(str(dt), dow, hour, min, fullness))
        print('[{}] Logged fullness.'.format(str(dt)))

    except TimeoutException:
        print('[{}] Logging failed. Took too much time.'.format(str(dt)))

    time.sleep(repeat * 60)
