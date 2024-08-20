from bs4 import BeautifulSoup
import requests

url = 'https://cbr.ru/currency_base/daily/'

source = requests.get(url)
txt = source.text
soup = BeautifulSoup(txt)

table = soup.find('table', {'class': 'data'})
Usa_not = table.find_all('td')
Usa_not = list(Usa_not)

for i in range(len(Usa_not)):
    if Usa_not[i].text == '840':
        global rate_us_dollar
        rate_us_dollar = Usa_not[i+4].text[:5] + ' рублей'


