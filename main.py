from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import re

cur_date = datetime.now().strftime('%Y_%m_%d')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
resp = requests.get('https://tables.finance.ua/ua/currency/cash/-/ua/usd/1#3:0', headers=headers).text
soup = BeautifulSoup(resp, 'html.parser')
with open('index.html', 'w') as html:
    html.write(resp)

with open('index.html') as file:
    src = file.read()

soup1 = BeautifulSoup(src, 'lxml')
table = soup1.find('table', class_='data-table')
date_th = table.find('thead').find_all('tr')[0].find_all('th')

table_th = []
for dth in date_th:
    dth= dth.text.strip()
    table_th.append(dth)

with open(f'date{cur_date}.csv','w')as file:
    writen = csv.writer(file)

    writen.writerow(
        (
            table_th
        )
    )

tbody_tr = table.find('tbody').find_all('tr',class_='selected')

date = []
i = 0

for tr in tbody_tr:
    i+=1
    course_= i
    course = type("Course", (), dict())
    course.time = tr.find("td", class_ = "c0").text.replace("\n","").strip()
    course.buy = tr.find("td", class_ = "c1").text.replace("\n","").strip()
    course.buy1 = tr.find('td', class_ = 'c2').text.replace('\n',"").strip()
    course.buy2 = tr.find('td', class_='c3').text.replace('\n','').strip()
    course.buy3 = tr.find('td', class_='c4').text.replace('\n','').strip()
    course.buys1 = re.sub(r"^\d+\.\d{2}", "", course.buy).strip()
    course.buys2 = re.sub(r"(\d+|\d+\.\d{2})$", "", course.buy).strip()
    course.buys3 = re.sub(r"^\d+\.\d{2}", "", course.buy1).strip()
    course.buys4 = re.sub(r"(\d+|\d+\.\d{2})$", "", course.buy1).strip()
    date_course = tr.find_all('td')

    date =[]
    for dtc in date_course:
        if dtc.find('a'):
            date_ar = dtc.find('a').get('href')
            date.append(date_ar)

    with open(f'date{cur_date}.csv','a')as file:
        writen = csv.writer(file)

        writen.writerow(
            (
                course_,
                course.time,
                course.buys2,
                course.buys4,
                course.buy2,
                course.buy3
            )
        )