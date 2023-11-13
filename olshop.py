import requests
from bs4 import BeautifulSoup

def get_shops_in_location(location):
    url = f'https://shopee.co.id/search?keyword={riau}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        shops = soup.find_all('div', class_='shop-item')  # Adjust the class based on the website structure

        for shop in shops:
            shop_name = shop.find('div', class_='shop-item__title').text.strip()
            products = shop.find_all('div', class_='product-item')  # Adjust the class based on the website structure

            print(f'Shop: {shop_name}')
            for product in products:
                product_name = product.find('div', class_='product-item__title').text.strip()
                print(f'  Product: {product_name}')

    else:
        print(f'Error {response.status_code}: Unable to fetch data.')

if __name__ == '__main__':
    location = input('Enter location: ')
    get_shops_in_location(location)
