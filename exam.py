import requests
from bs4 import BeautifulSoup
import pandas as pd
import scrapy
def scrape_product_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    product_data = []

    
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    # print(products)
    for product in products:
        try:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
            product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
            product_rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split(' ')[0]
            product_reviews = product.find('span', {'class': 'a-size-base'}).text.strip().replace(',', '')

            product_data.append([product_url, product_name, product_price, product_rating, product_reviews])
        except:
            continue

    return product_data


def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print('inside_details',soup)

    description = soup.find('div', {'id': 'productDescription'}).text.strip() if soup.find('div', {'id': 'productDescription'}) else ''
    asin = soup.find('th', text='ASIN').find_next('td').text.strip() if soup.find('th', text='ASIN') else ''
    product_description = soup.find('h2', text='Product Description').find_next('div').text.strip() if soup.find('h2', text='Product Description') else ''
    manufacturer = soup.find('th', text='Manufacturer').find_next('td').text.strip() if soup.find('th', text='Manufacturer') else ''

    return description, asin, product_description, manufacturer
def scrape_multiple_pages():
    all_product_data = []

    for page in range(1, 21):
        # if page==2:
        #     break
        if page==1:
            url='https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
            
            product_data = scrape_product_list(url)

            for data in product_data:
                product_url = data[0]
                additional_info = scrape_product_details(product_url)
                data.extend(additional_info)
                all_product_data.append(data)
        else:
            
            url='https://www.amazon.in/s?k=bags&page='+str(page)+'&crid=2M096C61O4MLT&qid=1688712489&sprefix=ba%2Caps%2C283&ref=sr_pg_'+str(page)
            product_data = scrape_product_list(url)

            for data in product_data:
                product_url = data[0]
                additional_info = scrape_product_details(product_url)
                data.extend(additional_info)
                all_product_data.append(data)

    df = pd.DataFrame(all_product_data, columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                                                 'Description', 'ASIN', 'Product Description', 'Manufacturer'])

    df.to_csv('product_data.csv', index=False)


scrape_multiple_pages()





