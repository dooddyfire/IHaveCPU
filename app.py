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
    attr_lis = []
    price_main_lis = []
    code_lis = []
    image_lis = []
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


        brand = soupx.find('p',{'class':'f-085'}).text 
        print(brand)
        code = brand.split("|")[1].strip()
        print(code)
        code_lis.append(code)

        print(brand.split("|")[0].strip())
        brand_lis.append(brand.split("|")[0].strip())
        
        image = [ k['data-thumb'] for k in soupx.find('ul',{'id':'slider_image_detail'}).find_all('li')]
        
        image_item = "\n".join(image)
        print(image_item)
        image_lis.append(image_item)


        name = soupx.find('div',{'class':'detail-title'}).find('h1').text 
        name_lis.append(name)
        print(name)





        detail = soupx.find('div',{'id':'content-detail'}).text.replace("รายละเอียดสินค้า","").strip()
        print(detail)
        detail_lis.append(detail)

        price = soupx.find('span',{'id':'product_price'}).text.strip() 
        print(price)
        price_lis.append(price)

        try:
            price_main = driver.find_element(By.XPATH,'//*[@id="change-content"]/div[1]/div/div[2]/div[2]/div/p').text 
            print(price_main)
            price_main_lis.append(price_main)
        except: 
            price_main = " "
            print(price_main)
            price_main_lis.append(price_main)            

        try:
            cat = [ g.text for g in driver.find_element(By.XPATH,'//*[@id="change-content"]/div[1]/div/div[2]/div[3]/div[3]').find_elements(By.CSS_SELECTOR,'span')]
            cat_x = "\n".join(cat)
            cat_lis.append(cat_x)
        except:
            cat_lis.append(" ")

        attr = soupx.find('div',{'id':'content-detail'}).text
        print(attr)
        attr_lis.append(attr)

df = pd.DataFrame()
df['ชื่อสินค้า'] = name_lis 
df['หมวดหมู่'] = cat_lis 
df['ราคา'] = price_lis 
df['ราคาก่อนลด'] = price_main_lis
df['แบรนด์'] = brand_lis 
df['รหัสสินค้า'] = code_lis 
df['รายละเอียด'] = detail_lis 
df['คุณสมบัติ'] = attr 
df['ลิงค์รูป'] = image_lis

df.to_excel("{}.xlsx".format(filename))