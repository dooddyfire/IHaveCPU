#import cloudscraper

#scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
#print(scraper.get("https://animekimi.co/").text) 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium import webdriver
import pandas as pd 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# "https://animekimi.co/page/4/"
if __name__ == '__main__':
    df = pd.DataFrame()

    
    url_lis = []
    start = int(input("Enter your start page : "))
    end = int(input("Enter your end page : "))
    filename = input("Enter your filename : ")

    name_lis = []
    brand_lis = [ ]
    price_lis = []
    cat_lis = []
    detail_lis = []

#Get bot selenium make sure you can access google chrome
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
    
   
    for i in range(start,end+1): 

        url = "https://www.ihavecpu.com/pages/Category?mode=manu&search=all&id=&sort_by=R&page={}".format(i)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source,'html.parser')

        for x in soup.find_all('div',{'class':'card-body'}): 

            link = x.find('a')['href']
            print(link)
            url_lis.append(link)
    

    for item in url_lis: 
        try:
            driver.get(item)
            soupx = BeautifulSoup(driver.page_source,'html.parser')
        except:
            continue

        name = soupx.find('div',{'class':'detail-title'}).find('h1').text 
        name_lis.append(name)
        print(name)

        brand = soupx.find('p',{'class':'f-085'}).text 
        print(brand)
        brand_lis.append(brand)

        detail = soupx.find('div',{'id':'content-detail'}).text.replace("รายละเอียดสินค้า","").strip()
        print(detail)
        detail_lis.append(detail)

        price = soupx.find('span',{'id':'product_price'}).text.strip() 
        print(price)
        price_lis.append(price)

        try:
            cat = [d for d in soupx.find_all('span',{'class':'p-1'})] 
            cat_x = " ".join(cat)
            cat_lis.append(cat)
        except:
            cat_lis.append(" ")

df = pd.DataFrame()
df['ชื่อสินค้า'] = name_lis 
df['หมวดหมู่'] = cat_lis 
df['ราคา'] = price_lis 
df['แบรนด์'] = brand_lis 
df['รายละเอียด'] = detail_lis 

df.to_excel("{}.xlsx".format(filename))