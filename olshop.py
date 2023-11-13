# shopee.py
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=2')
driver = webdriver.Chrome(options=chrome_options)

katakunci = input('Masukkan kata kunci : ')

def search(katakunci):
    links = []
    print('mencari semua product dengan kata kunci ' + katakunci)
    url = 'https://shopee.co.id/search?keyword=' + katakunci
    try:
        driver.get(url)
        time.sleep(5)
        driver.execute_script('window.scrollTo(0, 1500);')
        time.sleep(5)
        driver.execute_script('window.scrollTo(0, 2500);')
        time.sleep(5)
        soup_a = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup_a.find('div', class_='row shopee-search-item-result__items')
        for link in products.find_all('a'):
            links.append(link.get('href'))
            print(link.get('href'))
    except TimeoutException:
        print('failed to get links with query ' + line)
    return links

def get_product(produt_url):
    try:
        url = 'https://shopee.co.id' + produt_url
        driver.get(url)
        time.sleep(3)
        driver.execute_script('window.scrollTo(0, 1500);')
        time.sleep(3)
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'OSgLcw')))
        soup_b = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup_b.find('span', class_='OSgLcw').text
        price = soup_b.find('div', class_='_3n5NQx').text
        try:
            image = soup_b.find('div', class_='_2JMB9h _3XaILN')['style']
            imgurl = re.findall('url\((.*?)\)', image)
        except:
            imgurl = 'none'
        desc = soup_b.find('div', class_='_2u0jt9').text
        print('Scraping ' + title)
        with open('result.csv','a', encoding='utf-8',newline='') as f:
            writer=csv.writer(f)
            writer.writerow([title,price,url,desc,imgurl])

    except TimeoutException:
        print('cant open the link')

products_urls = search(katakunci)

for product_url in products_urls:
    get_product(product_url)

driver.quit()
