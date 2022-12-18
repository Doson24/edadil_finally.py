# на входе список продуктов для поиска на сайте роскачество

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--start-fullscreen')

chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"')
wd = webdriver.Chrome('C:\install\chromedriver.exe', chrome_options=chrome_options)
wd.set_window_size(1920, 1080)
wd.get("https://rskrf.ru/search/")


def add_data(indata, rate, price, link):
    indata['Рейтинг'] = rate
    indata["цена роскачество"] = price
    indata['ссылка роскачество'] = link
    return indata


rate_list, price_list, name_list, link_list = [], [], [], []
data_list = []


def search_ros(search, indata):
    search_button = WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.ID, "top-search-input")))
    search_button.send_keys(Keys.CONTROL + "a")
    search_button.send_keys(Keys.BACKSPACE)
    time.sleep(0.2)
    search_button.send_keys(search, Keys.ENTER)
    one_element = wd.find_elements_by_css_selector(".product-row.row div.search-good-item .card .card-img-wrapper a")
    if len(one_element) == 1:
        link = one_element[0].get_attribute("href")
        rate_price = wd.find_element_by_class_name("card-info").text
        rate = rate_price.split('\n')[0]
        price = rate_price.split('\n')[1]
        link_list.append(link)
        rate_list.append(rate)
        price_list.append(price)
        try:
            # name = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".h5.card-title.with-text a span")))
            name = wd.find_element_by_css_selector(".h5.card-title.with-text a span")
        except Exception:
            name = wd.find_element_by_css_selector('.item-section .product-row .card-body .h5.card-title')
        name = name.text
        name_list.append(name)
    else:
        name, rate, price, link = 'Null', 'Null', 'Null', 'Null'
    data_list.append(add_data(indata, rate, price, link))

    print(name, rate, price)
    print(link)


# search("Молоко ВКУСНОТЕЕВО")
date = datetime.date.today()
city = 'Канск'
data = pd.read_csv(f'data/{city}_data_{date}.csv')
name_search = []
for i in data['Название']:
    p = i.split(',')
    search_ros(p[0], line)
#
# a = pd.concat([i for i in data_list], ignore_index=True) # .loc[:5]
# a.to_csv(f'data/{city}_data_{date}.csv')

wd.close()
# print(name_list, )
