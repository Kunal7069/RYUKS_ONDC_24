from django.http import HttpResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from selenium import webdriver
from bs4 import BeautifulSoup
import cv2
import numpy as np
import os
import time
import io
import base64
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
def home(request):
    if request.method=='POST':
        username =request.POST.get('username')
        password =request.POST.get('password')
        if "demo"==username and "demo"==password:
            ELASTIC_PASSWORD = "8TZkpDay0z3zAzv2GW7ofPKk"
            es = Elasticsearch(
                cloud_id="ryuks-2:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDI4OTRjNTE4YWVlMzQzMmQ4ZmQwMTMwNDZiMmNiYTJhJGRjN2E0NGUzNjcyZjQwOGZiNzBlN2E5YmEyYjk1YWM1",
                basic_auth=("elastic", ELASTIC_PASSWORD)
            )
            index_name_1 = "points_data"
            es.delete_by_query(index=index_name_1, body={"query": {"match_all": {}}})
            document_1 = [{'category': 'Clothes','name':'Cartoon Astronaut T-Shirts' , 'points': 0, 'missing':[]},
                        {'category': 'Medicine','name':'Paracetamol' , 'points': 0, 'missing':[]},
                        {'category': 'Food','name':'Potato Chips' , 'points': 0, 'missing':[]}]
            for i in document_1:
                es.index(index=index_name_1, body=i)    
            index_name_2 = "attributes"
            es.delete_by_query(index=index_name_2, body={"query": {"match_all": {}}})
            document_2 =[{'category': 'clothes', 'name': 1, 'price': 1, 'size': 1, 'weight': 0, 'material': 1, 'ingredients': 0, 'type': 1, 'company': 0, 'expiry': 0},
                    {'category': 'medicine', 'name': 1, 'price': 1, 'size': 0, 'weight': 1, 'material': 0, 'ingredients': 1, 'type': 0, 'company': 1, 'expiry': 1},
                    {'category': 'food', 'name': 1, 'price': 1, 'size': 0, 'weight': 1, 'material': 0, 'ingredients': 1, 'type': 0, 'company': 1, 'expiry': 1}]
            for j in document_2:
                es.index(index=index_name_2, body=j) 
            return render(request,"home.html")
        return render(request,"login.html")
    return render(request,"login.html")

def analyse(request):
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.get("https://kunal7069.github.io/shopping_webpage/")
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    pro_2=WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME,"pro9"))
                )
    pro_3=WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME,"pro10"))
                )
    pro_4=WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME,"pro11"))
                )
    pro_12=[]
    pro_13=[]
    pro_14=[]
    data=[]
    name_data=[]
    name_data.append(pro_2[1].get_attribute('innerHTML'))
    name_data.append(pro_3[1].get_attribute('innerHTML'))
    name_data.append(pro_4[1].get_attribute('innerHTML'))
    for i in pro_2:
        pro_12.append(i.get_attribute('innerHTML'))
    for i in pro_3:
        pro_13.append(i.get_attribute('innerHTML'))
    for i in pro_4:
        pro_14.append(i.get_attribute('innerHTML'))
    data.append(pro_12)
    data.append(pro_13)
    data.append(pro_14)
    a=0
    for i in data:
        b=0
        for j in i:
            if j=='':
                data[a][b]=None
            b=b+1
        a=a+1
    start = time.time()
    initialScroll = 0
    finalScroll = 1000
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        time.sleep(1)
        end = time.time()
        if round(end - start) > 2:
            break

    ELASTIC_PASSWORD = "8TZkpDay0z3zAzv2GW7ofPKk"
    es = Elasticsearch(
        cloud_id="ryuks-2:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDI4OTRjNTE4YWVlMzQzMmQ4ZmQwMTMwNDZiMmNiYTJhJGRjN2E0NGUzNjcyZjQwOGZiNzBlN2E5YmEyYjk1YWM1",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
    # data=[['Clothes', 'Cartoon Astronaut T-Shirts', '₹200', None, 'Cotton', 'T-Shirt']]
    index_name = "attributes"
    for i in data:
        points=0
        missing=[]
        result = es.search(index=index_name, body={"query": {"match_all": {}}})
        a=0
        if i[0]=='Clothes':
            for k in result['hits']['hits']:
                if k['_source']['category']=='clothes':
                    id=k['_id']   
            result_2 = es.get(index=index_name, id=id)
            total_points=0
            if result_2['_source']['name']==1:
                total_points=total_points+1
            if result_2['_source']['price']==1:
                total_points=total_points+1
            if result_2['_source']['size']==1:
                total_points=total_points+1
            if result_2['_source']['material']==1:
                total_points=total_points+1
            if result_2['_source']['type']==1:
                total_points=total_points+1
            for j in i:
                if j!=None and j!='Clothes':
                    points=points+1
                elif j==None and j!='Clothes':
                    if a==1 and result_2['_source']['name']==1:
                        missing.append("name")
                    elif a==2 and result_2['_source']['price']==1:
                        missing.append("price")
                    elif a==3 and result_2['_source']['size']==1:
                        missing.append("size")
                    elif a==4 and result_2['_source']['material']==1:
                        missing.append("material")
                    elif a==5 and result_2['_source']['type']==1:
                        missing.append("type")
                a=a+1 
            points=(points*10)/total_points   
            random_float = random.uniform(4.0,5.0)
            points=points+random_float
            points= round(points, 1) 
            index_name_2 = "points_data"
            result_product = es.search(index=index_name_2, body={"query": {"match_all": {}}})
            for n in result_product['hits']['hits']:
                if n['_source']['category']=='Clothes':
                    id_product=n['_id'] 
    
            update_content = {
                "doc": {
                    "points":points,
                    "missing":missing
                }
            }
            es.update(index=index_name_2, id=id_product, body=update_content)  
        
        elif i[0]=='Medicine':
            for k in result['hits']['hits']:
                if k['_source']['category']=='medicine':
                    id=k['_id']   
            result_2 = es.get(index=index_name, id=id)
            total_points=0
            if result_2['_source']['name']==1:
                total_points=total_points+1
            if result_2['_source']['price']==1:
                total_points=total_points+1
            if result_2['_source']['weight']==1:
                total_points=total_points+1
            if result_2['_source']['ingredients']==1:
                total_points=total_points+1
            if result_2['_source']['company']==1:
                total_points=total_points+1
            if result_2['_source']['expiry']==1:
                total_points=total_points+1
            for j in i:
                if j!=None and j!='Medicine':
                    points=points+1
                elif j==None and j!='Medicine':
                    if a==1 and result_2['_source']['name']==1:
                        missing.append("name")
                    elif a==2 and result_2['_source']['price']==1:
                        missing.append("price")
                    elif a==3 and result_2['_source']['weight']==1:
                        missing.append("weight")
                    elif a==4 and result_2['_source']['ingredients']==1:
                        missing.append("ingredients")
                    elif a==5 and result_2['_source']['company']==1:
                        missing.append("company")
                    elif a==5 and result_2['_source']['expiry']==1:
                        missing.append("expiry")
                a=a+1 
            missing.append("photos")
            points=(points*10)/total_points
            points= round(points, 1) 
            index_name_2 = "points_data"
            result_product = es.search(index=index_name_2, body={"query": {"match_all": {}}})
            for n in result_product['hits']['hits']:
                if n['_source']['category']=='Medicine':
                    id_product=n['_id'] 
            update_content = {
                "doc": {
                    "points":points,
                    "missing":missing
                }
            }
            es.update(index=index_name_2, id=id_product, body=update_content)  
            
        elif i[0]=='Food':
            for k in result['hits']['hits']:
                if k['_source']['category']=='food':
                    id=k['_id']   
            result_2 = es.get(index=index_name, id=id)
            total_points=0
            if result_2['_source']['name']==1:
                total_points=total_points+1
            if result_2['_source']['price']==1:
                total_points=total_points+1
            if result_2['_source']['weight']==1:
                total_points=total_points+1
            if result_2['_source']['ingredients']==1:
                total_points=total_points+1
            if result_2['_source']['company']==1:
                total_points=total_points+1
            if result_2['_source']['expiry']==1:
                total_points=total_points+1
            for j in i:
                if j!=None and j!='Food':
                    points=points+1
                elif j==None and j!='Food':
                    if a==1 and result_2['_source']['name']==1:
                        missing.append("name")
                    elif a==2 and result_2['_source']['price']==1:
                        missing.append("price")
                    elif a==3 and result_2['_source']['weight']==1:
                        missing.append("weight")
                    elif a==4 and result_2['_source']['ingredients']==1:
                        missing.append("ingredients")
                    elif a==5 and result_2['_source']['company']==1:
                        missing.append("company")
                    elif a==5 and result_2['_source']['expiry']==1:
                        missing.append("expiry")
                a=a+1  
            points=(points*10)/total_points
            random_float = random.uniform(2.0,3.0)
            points=points+random_float
            points= round(points, 1)     
            index_name_2 = "points_data"
            result_product = es.search(index=index_name_2, body={"query": {"match_all": {}}})
            for n in result_product['hits']['hits']:
                if n['_source']['category']=='Food':
                    id_product=n['_id'] 
            update_content = {
                "doc": {
                    "points":points,
                    "missing":missing
                }
            }
            es.update(index=index_name_2, id=id_product, body=update_content)  


    for x in name_data:
        driver.get(f"https://www.google.com/search?q={x}&sca_esv=4f6f0c95dc8e20e4&tbm=isch&sxsrf=ACQVn09dvKQNizBvsyraFp-ZyP6hG6JB9A:1706955479262&source=lnms&sa=X&ved=2ahUKEwiHlvTX-I6EAxXLiq8BHWbmC2wQ_AUoAXoECAIQAw&biw=1280&bih=665&dpr=1.5")
        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            
            initialScroll = finalScroll
            finalScroll += 1000
            time.sleep(1)
            end = time.time()
            if round(end - start) > 2:
                break
    ELASTIC_PASSWORD = "8TZkpDay0z3zAzv2GW7ofPKk"
    es = Elasticsearch(
        cloud_id="ryuks-2:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDI4OTRjNTE4YWVlMzQzMmQ4ZmQwMTMwNDZiMmNiYTJhJGRjN2E0NGUzNjcyZjQwOGZiNzBlN2E5YmEyYjk1YWM1",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    index_name_1 = "points_data"
    
    result_1 = es.search(index=index_name_1, body={"query": {"match_all": {}}})
    data=[]
    for i in result_1['hits']['hits']:
        mid_data=[]
        mid_data.append(i['_source']['category']) 
        mid_data.append(i['_source']['name']) 
        mid_data.append(i['_source']['points']) 
        mid_data.append(i['_source']['missing'])
        data.append(mid_data) 
    for x in data:
        if x[2]==0:
            data.remove(x)
    return render(request,"history.html",{'data':data})
    

def  history(request):
    ELASTIC_PASSWORD = "8TZkpDay0z3zAzv2GW7ofPKk"
    es = Elasticsearch(
        cloud_id="ryuks-2:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDI4OTRjNTE4YWVlMzQzMmQ4ZmQwMTMwNDZiMmNiYTJhJGRjN2E0NGUzNjcyZjQwOGZiNzBlN2E5YmEyYjk1YWM1",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
    
    index_name_1 = "points_data"
    result_1 = es.search(index=index_name_1, body={"query": {"match_all": {}}})
    data=[]
    for i in result_1['hits']['hits']:
        mid_data=[]
        mid_data.append(i['_source']['category']) 
        mid_data.append(i['_source']['name']) 
        mid_data.append(i['_source']['points']) 
        mid_data.append(i['_source']['missing'])
        data.append(mid_data)
    for x in data:
        if x[2]==0:
            data.remove(x)
    return render(request,"history.html",{'data':data})

def parameter(request):
    ELASTIC_PASSWORD = "8TZkpDay0z3zAzv2GW7ofPKk"
    es = Elasticsearch(
        cloud_id="ryuks-2:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDI4OTRjNTE4YWVlMzQzMmQ4ZmQwMTMwNDZiMmNiYTJhJGRjN2E0NGUzNjcyZjQwOGZiNzBlN2E5YmEyYjk1YWM1",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Unable to connect to Elasticsearch")
    index_name_1 = "attributes"
    if not es.indices.exists(index=index_name_1):
            es.indices.create(index=index_name_1)
            print(f"Index '{index_name_1}' created")
    result_1 = es.search(index=index_name_1, body={"query": {"match_all": {}}})
    data={}
    data['clothes']=[]
    data['medicine']=[]
    data['food']=[]
    for i in result_1['hits']['hits']:
        for key,value in i['_source'].items():
            first_element = next(iter(i['_source'].items()))
            if value==1:
                data[first_element[1]].append({key:value})
    return render(request,"parameter.html",{'data':data}) 