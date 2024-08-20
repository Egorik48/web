# Импортируем библиотеку BeautifulSoup для парсинга HTML
from bs4 import BeautifulSoup

# Импортируем модуль requests для получения веб-страниц
import requests

# Задаем URL страницы с курсами валют на сайте ЦБ РФ
url = 'https://cbr.ru/currency_base/daily/'

# Используем метод get класса requests для загрузки содержимого страницы
source = requests.get(url)

# Преобразуем полученное содержимое в объект BeautifulSoup
txt = source.text
soup = BeautifulSoup(txt)

# Находим таблицу с данными на странице, используя селектор класса data
table = soup.find('table', {'class': 'data'})

# Находим все ячейки (td) в таблице и сохраняем их в список Usa_not
Usa_not = table.find_all('td')
Usa_not = list(Usa_not)

# Проходим в цикле по списку ячеек и ищем ячейку с кодом валюты 840 (код доллара США)
for i in range(len(Usa_not)):
    if Usa_not[i].text == '840':
        # Присваиваем переменной rate_us_dollar значение из следующей ячейки, которая содержит курс доллара
        global rate_us_dollar
        rate_us_dollar = Usa_not[i+4].text[:5] + ' рублей'
