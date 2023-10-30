#Imports
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd
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
    data = []
    for city in cities:
        for i in range(1,16):
            driver.get("https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&page="+str(i)+"&cityName="+str(city))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # print("Page "+str(i)+" of "+str(city))
            data.extend(get_data(soup))
    
    # After scraping data from all pages, dump the list as a single JSON object
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    print("Data has been scraped and stored in data.json file")



def get_data(soup):
    '''
    This function Scrapes the data from the website and stores the output in JSON format.
    '''
    h=[]
    prop=soup.find_all('div',class_='mb-srp__card')
    for i in prop:
        name=i.find('h2',class_='mb-srp__card--title')
        title=name.text.split(', ')
        if i.find('span', class_='mb-srp__card__developer--name--highlight'):
            Sector = i.find('span', class_='mb-srp__card__developer--name--highlight').text
        elif i.find('div', class_='mb-srp__card__society--name'):
            Sector = i.find('div', class_='mb-srp__card__society--name').text
        elif len(title) > 1:
            Sector = title[1]
        else:
            Sector = "N/A"
        price =i.find('div',class_='mb-srp__card__price--amount')
        price_in_INR=price.text.replace('\u20b9', '').strip()
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
            "Name":name.text,
            "Price(INR)":price_in_INR,
            "Total-area":area.text,
            "Sector":Sector,
            "Furnishing":furnishing,
            "Parking":parking,
            "Bathroom":bathroom,
            "Society":society_name
        }
        h.append(var)

    return h






get_house(driver)