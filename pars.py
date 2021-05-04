import requests
from bs4 import BeautifulSoup

link='https://auto.ru/rostovskaya_oblast/cars/daewoo/tacuma/all/'
#link='https://auto.ru/rostovskaya_oblast/cars/vaz/21099/all/'
#link='https://auto.ru/rostovskaya_oblast/cars/daewoo/espero/all/'
#link='https://auto.ru/rostovskaya_oblast/cars/mazda/3/all/'
#link='https://auto.ru/rostovskaya_oblast/cars/skoda/fabia/all/' nice
#link='https://auto.ru/rostovskaya_oblast/cars/mazda/6/all/' nice
#link='https://auto.ru/rostovskaya_oblast/cars/land_rover/all/' -
#link='https://auto.ru/rostovskaya_oblast/cars/land_rover/range_rover/all/'
#link='https://auto.ru/rostovskaya_oblast/cars/land_rover/discovery_sport/all/'  50/50
#link='https://auto.ru/rostovskaya_oblast/cars/mercedes/all/'
car_url=[]
while True:
  response=requests.get(link)
  response.encoding = 'utf-8'
  soup = BeautifulSoup(response.text, 'html.parser')
  cards=soup.find_all('div', class_='ListingItem-module__main')
  #Добавляет в словарь ссылки авто
  for card in cards:
      car_url.append(card.find('a').get('href'))
  #Ловит строку страниц
  #stranica=soup.find('a',class_='ListingPagination-module__next')
  # Проверка на наличие страницы
  if soup.find('a',class_='ListingPagination-module__next'):
      stranica = soup.find('a', class_='ListingPagination-module__next').get('href')
      link = stranica
  else:
      break

  if link==None:
    break
  print(stranica)

car_url

cars = []
for car in car_url:
    response = requests.get(car)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        title = soup.find('div', class_='CardSidebarActions__title').get_text()
        #saler = soup.find('div', class_='CardSellerNamePlace__name').get('title')
        gorod = soup.find('span', class_='MetroListPlace_space').get_text()
        car_year = soup.find('a', class_='Link Link_color_black').get_text()
        opisanie = soup.find('div', class_='CardDescription__textInner').get_text()
        car_probeg = soup.find('li', class_='CardInfoRow CardInfoRow_kmAge').get_text()
        vladelci = soup.find('li', class_='CardInfoRow CardInfoRow_ownersCount').get_text()
        price = soup.find('span', class_='OfferPriceCaption__price').get_text()
    except:
        pass
    #vladenie = soup.find('li', class_='CardInfoRow CardInfoRow_owningTime').get_text()
    #carr = {}
   #for info_car in soup.find_all('ul',class_='CardInfoRow'):
     #   carr[info_car.contents[0].get_text()]=info_car.contents[1].get_text()
    cars.append({
        'Модель': title,
        'Цена': int(price.replace('\xa0','').replace('₽','')),
        'Ссылка на авто': car,
        #'Продавец:': saler,
        'Город': gorod,
        'Пробег': int(car_probeg.replace('\xa0','').replace('Пробег','').replace('км','')),
        'Год выпуска': car_year,
        'Владельцы': vladelci.replace('Владельцы',''),
        #'Владение:': vladenie.replace('Владение',''),
        'Описание':opisanie
         #'Информация:': carr
    })

print(cars)


import csv
#newline - перевод строки, чтобы не было пустых строк в файле
with open(f'{title}.csv','w', encoding='cp1251', newline='') as f:
  #delimiter - разделитель для того, чтобы нормально открывались по умолчанию
  writer = csv.writer(f, delimiter=';')
  writer.writerow(['Марка', 'Цена', 'Ссылка на авто', 'Город', 'Пробег', 'Год выпуска', 'Владельцы', 'Описание'])
  try:
      for items in cars:
          writer.writerow([items['Модель'], items['Цена'], items['Ссылка на авто'], items['Город'], items['Пробег'],
                           items['Год выпуска'], items['Владельцы'], items['Описание']])
  except:
      pass

import pandas as pd
import matplotlib.pyplot as plot

cars_df=pd.DataFrame(cars)

cars_df['Год выпуска']=cars_df['Год выпуска'].apply(int)
cars_df['Возраст']=cars_df['Год выпуска']

cars_df.plot.scatter(x='Возраст', y='Цена')
plot.show()
