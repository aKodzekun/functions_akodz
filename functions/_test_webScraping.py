import requests
from bs4 import BeautifulSoup

# Машины жагсаалтын хуудас руу HTTP хүсэлт илгээнэ үү
# url = 'https://autocj.co.jp/hpmo/used_cars?chk_new=new&sort=price'
# url = 'https://1234.mn/'

url = 'https://1234.mn/'
response = requests.get(url)
response.encoding = 'utf-8'

print(response.status_code)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)
    # HTML бүтцэд үндэслэн машины мэдээллийг олж, задлах
    # car_listings = soup.find_all('li', class_='l-vblock')

    # print(car_listings)
    # for car in car_listings:
    #     name = car.find('h2', class_='').text
    #     model = car.find('p', class_='v-model').text
    #     table = car.find('table', class_='v-table').text
    #     print(f"Make: {name}, Model: {model}, Table: {table}")


    products = soup.find_all('div', class_='span3')
    print(products)
    for item in products:
        # model = item.find('p', class_='').text
        table = item.find('div', class_='blog-post-title').text
        print(f"Table: {table}")

else:
    print('Failed to retrieve the web page.')