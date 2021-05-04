import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from menu import Ui_MainWindow # Импорт основного UI

import requests
from bs4 import BeautifulSoup

import csv

from PyQt5.QtWidgets import QMessageBox # для всплывающего окна

class CarsMenu(QtWidgets.QMainWindow):    # наследуемся от класса в файле menu
    def __init__(self):
        super(CarsMenu, self).__init__() # возвращает объект родителя класса CarsMenu и вызывает его конструктор
        self.menu = Ui_MainWindow()
        self.menu.setupUi(self) # Вызываем функцию setupUi чтобы отрисовать интерфейс
        self.init_UI()

    def init_UI(self):   # Функция для доработки графического интерфейса
        self.setWindowTitle('autoРУshka')
        self.setWindowIcon(QIcon('icon.png'))

        self.menu.lineEdit.setPlaceholderText('Введите ссылку с auto.ru:') # подсказка для пользователя

        self.menu.parsingButton.clicked.connect(self.pars)

        self.setFixedSize(821, 737) # Фиксированный размер окна

    def pars(self):
        try:
            link = self.menu.lineEdit.text()
            str(link)

            car_url = []

            while True:
                response = requests.get(link)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                cards = soup.find_all('div', class_='ListingItem-module__main')
                # Добавляет в словарь ссылки авто
                for card in cards:
                    car_url.append(card.find('a').get('href'))
                # Проверка на наличие страницы
                if soup.find('a', class_='ListingPagination-module__next'):
                    # Ловит строку страниц
                    stranica = soup.find('a', class_='ListingPagination-module__next').get('href')
                    link = stranica
                else:
                    break

                if link == None:
                    break
                print(stranica)

            info = QMessageBox()
            info.setWindowTitle('Ответ')
            info.setText('Ожидайте! Если у вас более 100 машин, то нужно набраться терпения и ждать. :)')
            info.setIcon(QMessageBox.Warning)
            info.setStandardButtons(QMessageBox.Ok)

            info.exec_()

            cars = []
            for car in car_url:
                response = requests.get(car)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                try:
                    title = soup.find('div', class_='CardSidebarActions__title').get_text()
                    gorod = soup.find('span', class_='MetroListPlace_space').get_text()
                    car_year = soup.find('a', class_='Link Link_color_black').get_text()
                    opisanie = soup.find('div', class_='CardDescription__textInner').get_text()
                    car_probeg = soup.find('li', class_='CardInfoRow CardInfoRow_kmAge').get_text()
                    vladelci = soup.find('li', class_='CardInfoRow CardInfoRow_ownersCount').get_text()
                    price = soup.find('span', class_='OfferPriceCaption__price').get_text()
                except:
                    pass
                cars.append({
                    'Модель': title,
                    'Цена': int(price.replace('\xa0', '').replace('₽', '')),
                    'Ссылка на авто': car,
                    'Город': gorod,
                    'Пробег': int(car_probeg.replace('\xa0', '').replace('Пробег', '').replace('км', '')),
                    'Год выпуска': car_year,
                    'Владельцы': vladelci.replace('Владельцы', ''),
                    'Описание': opisanie
                })

            #print(cars)

            # newline - перевод строки, чтобы не было пустых строк в файле
            with open(f'{title}.csv', 'w', encoding='cp1251', newline='') as f:
                # delimiter - разделитель для того, чтобы номарльно открывались по умолчанию
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    ['Марка', 'Цена', 'Ссылка на авто', 'Горо   д', 'Пробег', 'Год выпуска', 'Владельцы', 'Описание'])
                for items in cars:
                    try:
                        writer.writerow(
                            [items['Модель'], items['Цена'], items['Ссылка на авто'], items['Город'], items['Пробег'],
                            items['Год выпуска'], items['Владельцы'], items['Описание']])
                    except:
                        pass
            info1 = QMessageBox()
            info1.setWindowTitle('Ответ')
            info1.setText('Мы собрали для вас всю информацию!')
            info1.setIcon(QMessageBox.Warning)
            info1.setStandardButtons(QMessageBox.Ok)

            info1.setInformativeText('Смотрите в папке <kursach>')

            info1.exec_()
            self.menu.lineEdit.setText('')
            pass
        except:
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setText('Вставьте ссылку либо вы указали неверную ссылку!')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)

            error.setInformativeText('Пример: \nhttps://auto.ru/rostovskaya_oblast/cars/daewoo/tacuma/all/')
            self.menu.lineEdit.setText('')

            error.exec_()
            pass


app = QtWidgets.QApplication([])
application = CarsMenu()
application.show()

sys.exit(app.exec())