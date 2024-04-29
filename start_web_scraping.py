import csv
import logging
import os
import random
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from config import csv_file_name, log_file_name, product_groups_list, site


class Data:

    def __init__(self):
        self.csv_file_fields = [
            'name',
            'sku',
            'brand',
            'market',
            'category',
            'price',
            'currency',
            'material',
            'color',
            'url'
        ]
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]


class ScraperClient(Data):

    def __init__(self):
        super(ScraperClient, self).__init__()
        self.headers = {
            'user-agent': random.choice(self.user_agents)
        }

    def _get_pagination_numbers_list(self, url):
        pagination_numbers_list = []
        paginator_number = 1
        while True:
            data_scraper_page = requests.get(f'{url}?page={paginator_number}', headers=self.headers)
            if data_scraper_page.status_code == 200:
                pagination_numbers_list.append(paginator_number)
            else:
                break
            paginator_number += 1
        return pagination_numbers_list

    def _get_product_details(self, url):
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        price_details = soup.find('span', class_='notranslate')
        try:
            sku = soup.find(class_='lv-product__sku overline').text.strip()
        except AttributeError:
            sku = ''
        try:
            product_details = soup.find(
                'div', class_='lv-product-detailed-features__description body-s').find('ul').find_all('li')
            color = product_details[0].text.strip()
            material = product_details[1].text.strip()
        except AttributeError:
            color = ''
            material = ''
        return {
            'sku': sku,
            'brand': soup.find(class_='lv-logo lv-header__logo').find(class_='sr-only').text.strip(),
            'market': soup.find('span', class_='-text-is-underline country-label').text.strip(),
            'price': price_details.text.strip()[:-1] if price_details else '',
            'currency': price_details.text.strip()[-1] if price_details else '',
            'material': material,
            'color': color
        }

    @staticmethod
    def get_category_name(url):
        match = re.search(f'{site}/fra-fr/(.*?)/_/N-[\w\d]+', url)
        return match.group(1).replace('/', ' ')

    def get_products_list(self, url):
        products_list = []
        numbers_list = self._get_pagination_numbers_list(url)
        for number in numbers_list:
            page = requests.get(f'{url}?page={number}', headers=self.headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            products = soup.find_all('div', class_='lv-product-card__wrap')
            for product in products:
                products_list.append(product)
        return products_list

    def get_product_data(self, obj, category):
        product_details_url = obj.find('div', class_='lv-product-card__name-wrapper').find('a')['href']
        product_details = self._get_product_details(product_details_url)
        return {
            'name': obj.find('div', class_='lv-product-card__name-wrapper').text.strip(),
            'sku': product_details['sku'],
            'brand': product_details['brand'],
            'market': product_details['market'],
            'category': category,
            'price': product_details['price'],
            'currency': product_details['currency'],
            'material': product_details['material'],
            'color': product_details['color'],
            'url': product_details_url
        }


class CSVClient(Data):

    def write_data_to_file(self, products):
        if os.path.exists(csv_file_name):
            os.remove(csv_file_name)
        with open(csv_file_name, 'a+', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.csv_file_fields)
            writer.writeheader()
            for product in products:
                writer.writerow(product)


if __name__ == '__main__':
    if os.path.exists(log_file_name):
        os.remove(log_file_name)
    logging.basicConfig(filename=log_file_name, level=logging.INFO)
    product_data_list = []
    scraper_client = ScraperClient()
    csv_client = CSVClient()
    logging.info(f'Found {len(product_groups_list)} categories, starting to process them')
    for product_url in tqdm(product_groups_list, desc='Processing URLs', unit='URL'):
        category_name = scraper_client.get_category_name(product_url)
        for product_object in scraper_client.get_products_list(product_url):
            product_data_list.append(scraper_client.get_product_data(product_object, category_name))
        csv_client.write_data_to_file(product_data_list)
        logging.info(f'Processed category: "{category_name}"')
