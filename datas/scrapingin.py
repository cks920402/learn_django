import datetime
import requests
import schedule
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import datetime


# 사람인 사이트를 크롤링해서 하나의 리스트 안에 데이터를 담고 몽고 클라이언트로 연결해서 데이터 넣기

checkdatas = list()
def putdata():
    url = "http://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword=%EB%93%9C%EB%A1%A0"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find_all("div", attrs={"class":"item_recruit"})
    datas = list()
    for item in items:
        title = item.a["title"]
        link = item.a["href"]
        link = "http://www.saramin.co.kr" + link
        data = {"title" : title, "link" : link}
        if data not in checkdatas:
            datas.append(data)
        else:
            continue

    checkdatas.append(datas[:])

    with MongoClient("mongodb://172.17.0.3:27017/") as client:
        ddb = client.ddb
        ddb.ddetail.insert_many(datas)
    
    now = datetime.datetime.now()
    print(now)

schedule.every(10).seconds.do(putdata)
while True:
    schedule.run_pending()
    time.sleep(1)
