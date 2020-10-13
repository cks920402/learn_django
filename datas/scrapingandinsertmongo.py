from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

# 경제 사이트를 크롤링해서 하나의 리스트안에 데이터를 담고 몽고클라이언트로 연결해서 데이터담기!

res = requests.get('http://media.daum.net/economic/')
if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    links = soup.find_all('a', class_='link_txt')
    print('task_crawling_daum : ', type(links), len(links))
    dates = list()
    title = str()
    link = str()        
    for link in links:
        title = str.strip(link.get_text())
        link = link.get('href')
        data = {"title": title, "link": link, "create_date": datetime.datetime.now()}
        dates.append(data)
        # print(type(dates), dates)
        # list, [{'title': '1boon', 'link': '/1boon', 'create_date': datetime.datetime(2020, 10, 13, 15, 13, 32, 308767)}, {~~}]

    with MongoClient('mongodb://172.17.0.2:27017/')  as client:
        mydb = client.mydb
        # res = mydb.economic.insert_many(dates)
        mydb.economic.insert_many(dates)
