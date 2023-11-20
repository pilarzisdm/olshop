# streamlit_shopee.py

import streamlit as st
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

# Function to search for products
def search(driver, katakunci):
    links = []
    st.write(f'Mencari semua produk dengan kata kunci: {katakunci}')
    url = 'https://shopee.co.id/search?keyword=' + katakunci

    try:
        driver.get(url)
        
        # Wait for the search results to be visible
        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'shopee-search-item-result__items')))
        
        # Scroll to load more results (if needed)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)  # Adjust the sleep duration if necessary
        
        soup_a = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup_a.find('div', class_='shopee-search-item-result')
        
        if products:
            for link in products.find_all('a'):
                links.append(link.get('href'))
                st.write(link.get('href'))
        else:
            st.write("No products found.")
            
    except TimeoutException:
        st.write(f'Failed to get links with query {katakunci}')

    return links

# Function to get product details
def get_product(driver, product_url):
    try:
        url = 'https://shopee.co.id' + product_url
        driver.get(url)
        time.sleep(3)
        driver.execute_script('window.scrollTo(0, 1500);')
        time.sleep(3)
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, '_44qnta')))
        soup_b = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup_b.find('span', class_='_44qnta').text
        price = soup_b.find('div', class_='pqTWkA').text
        
        desc = soup_b.find('div', class_='_2u0jt9').text
        st.write(f'Scraping {title}')
        with open('result.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([title, price, url, desc, imgurl])

    except TimeoutException:
        st.write('Cannot open the link')

# Streamlit app
st.title("Shopee Scraper")

# WebDriver initialization
from webdriver_manager.chrome import ChromeDriverManager
# WebDriver initialization using webdriver_manager
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=2')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

katakunci = st.text_input('Masukkan kata kunci:')

# Create a button to start the scraping process
if st.button("Cari Produk"):
    st.write("Sedang mencari produk...")
    products_urls = search(driver, katakunci)

    for product_url in products_urls:
        get_product(driver, product_url)

    st.write("Proses selesai.")

# Exception handling for quitting WebDriver
try:
    driver.quit()
except Exception as e:
    st.write(f"Error while quitting WebDriver: {str(e)}")

