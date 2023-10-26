#Imports
from bs4 import BeautifulSoup
from selenium import webdriver
import json

from selenium.webdriver.chrome.service import Service

#driver-setup
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)



def get_house(driver):
    '''
    This function calls the search endpoint of the Magicbricks website with the help of the driver.
    '''
    cities=['Gurgaon']
    for city in cities:
        for i in range(1,6):
            driver.get("https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&page="+str(i)+"&cityName="+str(city))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # print("Page "+str(i)+" of "+str(city))
            get_data(soup)


def get_data(soup):
    '''
    This function Scrapes the data from the website and stores the output in JSON format.
    '''
    h=[]
    prop=soup.find_all('div',class_='mb-srp__card')
    for i in prop:
        name=i.find('h2',class_='mb-srp__card--title')
        title = name.text.split(', ')
        Sector = title[1]
        price=i.find('div',class_='mb-srp__card__price--amount')
        area=i.find('div',class_='mb-srp__card__summary--value')
        furnishing = i.find('div', {'data-summary': 'furnishing'})
        if furnishing:
            furnishing = furnishing.find('div', class_='mb-srp__card__summary--value').text
        else:
            furnishing = "N/A"
        society = i.find('div', {'data-summary': 'society'})
        if society:
            society_name = society.find('div', class_='mb-srp__card__summary--value').text
        else:
            society_name = "N/A"
        parking = i.find('div', {'data-summary': 'parking'})
        if parking:
            parking = parking.find('div', class_='mb-srp__card__summary--value').text
            parking = parking.split(' ')[0]
        else:
            parking = "N/A"
        bathroom = i.find('div', {'data-summary': 'bathroom'})
        if bathroom:
            bathroom = bathroom.find('div', class_='mb-srp__card__summary--value').text
        else:
            bathroom = "N/A"
        var={
            "name":name.text,
            "price":price.text,
            "Total-area":area.text,
            "Sector":Sector,
            "furnishing":furnishing,
            "parking":parking,
            "bathroom":bathroom,
            "society":society_name
        }
        h.append(var)
    with open("data.json",'r+') as f:
        feeds = json.load(f)
        for i in h:
            feeds['property'].append(i)
        f.seek(0)
        json.dump(feeds, f)




v={
    "property":[]
}
with open("data.json", mode='w', encoding='utf-8') as f:
    json.dump(v,f)


get_house(driver)