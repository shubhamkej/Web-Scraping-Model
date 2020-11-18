#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import selenium
from selenium import webdriver
import time
import io
import requests
import re
import mysql.connector
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException


# In[9]:


driver = webdriver.Chrome()


# In[10]:


def store_function(content):
    splittedcontent = content.splitlines(0)
    
    regex = re.compile(r'[^0-9]+.$')
    filtered = [i for i in splittedcontent if not regex.match(i)]
    
    while("" in filtered) : 
        filtered.remove("")
        
    regex = re.compile(r'^.*Growth+.*$')
    final = [i for i in filtered if regex.match(i)]
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="finance"
    )
    for i in final:
        stri = i.split(";")
        d = stri[0]
        a = stri[1]
        b = stri[2]
        n = stri[5]
        da = stri[7]

        mycursor = mydb.cursor()

        sql = "INSERT INTO schemevalue (SchemeCode, SchemeName, ISIN_Growth, NetAssetValue, date) VALUES ( %s, %s, %s, %s, %s)"
        val = (d, a, b, n, da)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        print(mydb)


# In[22]:


list1 = ["10", "11", "12", "13", "14","15"]
list2 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
list3 = ["2016", "2017", "2018", "2019", "2020"]

sk = "http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt="
for k in list3:
    for j in list2:
        if(k=='2016' and (j=='Jan' or j=='Feb' or j=='Mar')):
            continue;
        if(k=='2020' and j=='Nov'):
            break;
        for i in list1:
            driver.get('http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt='+i+'-'+j+'-'+k)
            #time.sleep(5)
            content = driver.find_element_by_xpath(".//pre").text
            print(content)
            store_function(content)


# In[ ]:




