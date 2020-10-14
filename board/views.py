from django.shortcuts import render

# Create your views here.
from django.db import connection
import sqlite3
from pymongo import MongoClient

def ddata(request):
    data = request.GET.copy()
    with MongoClient("mongodb://172.17.0.3:27017/") as client:
        result = list(client.ddb.ddetail.find({}))
        data['page_obj'] = result
    return render(request, 'board/ddata.html', context=data)

def listwithmongo(request):
    data = request.GET.copy()
    with MongoClient('mongodb://172.17.0.2:27017/') as client:
        mydb = client.mydb
        result = list(mydb.economic.find({}))
        data['page_obj'] = result
    return render(request, 'board/listwithmongo.html', context=data)

def listwithrawquery(request):
    data = request.GET.copy()
    # data = dict()
    # connection.row_factory = sqlite3.Row
    # cursor = connection.cursor()
    with sqlite3.connect("db.sqlite3") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor();	cur.execute("select * from economic")
        data['rows'] = cur.fetchall()

    for row in data['rows']:
        print(f"{row['title']}, {row['link']}")

    return render(request, 'board/listwithrawquery.html', context=data)

from django.core.paginator import Paginator
def listwithrawquerywithpaginator(request):
    data = request.GET.copy()
    # data = dict()
    # connection.row_factory = sqlite3.Row
    # cursor = connection.cursor()
    with sqlite3.connect("db.sqlite3") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor();	cur.execute("select * from economic")
        contact_list = cur.fetchall()

    paginator = Paginator(contact_list, 5) # Show 15 contacts per page.

    page_number = request.GET.get('page')
    page_number = page_number if page_number else 1 
    data['page_obj'] = paginator.get_page(page_number)

    page_obj=data['page_obj']
    for row in page_obj:
        print(f"{row['title']}, {row['link']}")

    return render(request, 'board/listwithrawquerywithpaginator.html', context=data)

from pymongo import MongoClient
from board.mongopaginator import MongoPaginator

# def listwithmongo(request):
#     data = request.GET.copy()
#     with MongoClient('mongodb://10.0.0.5:27017/')  as client:
#         mydb = client.mydb
#         result = list(mydb.economic.find({}))			# get Collection with find()
        
#         result_page = []
#         for info in result:						# Cursor
#             # del info(_id)
#             temp = {'title':info['title'], 'link':info['link']}
#             result_page.append(temp)
#             print(type(info), info)
#         data['page_obj'] = result
        
#     return render(request, 'board/listwithmongo.html', context=data)

def listwithmongowithpaginator(request):
    data = request.GET.copy()
    with MongoClient('mongodb://192.168.0.6:27017/')  as client:
        mydb = client.mydb
        contact_list = mydb.economic.find({})			# get Collection with find()
        for info in contact_list:						# Cursor
            print(info)

    paginator = MongoPaginator(contact_list, 5) # Show 15 contacts per page.

    page_number = request.GET.get('page', 1)
    data['page_obj'] = paginator.get_page(page_number)

    page_obj=data['page_obj']
    for row in page_obj:
        print(f"{row['title']}, {row['link']}")

    return render(request, 'board/listwithrawquerywithpaginator.html', context=data)


# 구름 새컨테이너 생성
# 이름 learn_django1
# 지역 서울
# 공개 private
# 템플릿 깃허브
# 소프트웨어 장고
# 추가모듈 몽고디비설치 선택
# 구름 새터미널에서 mongod 입력
# 위에 goormide 옆에 window에서 new terminal window 선택
# mongo 입력
# show dbs
# new terminal window 하나 더 만든다
# ls 하고 cd datas/ 들어가서 ls 확인
# python3 ./scrapingandinsertmongo.py 입력하면 에러가 날 텐데
# pip3 install -U pip pymongo
# pip3 install -U pip bs4
# python3 ./scrapingandinsertmongo.py

#두번째 터미널에서 
# show mydb 
# show collections 
# economic.find 하는거 



# 구름 장고 gui
# 실행하면 에러가 뜰텐데 migrate && 까지 삭제해준다
# 실행하고 url 카피해서 board/listwithmongo 붙여줘서 브라우저에서 연다



