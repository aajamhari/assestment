import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

#product name
def get_product(soup):
    try:
        product_name = soup.find("h1", attrs={'class': 'Typography_body1___zS6E Typography_text-black__NvbF0 ProductInfo_productName___TZSK'}).text
    except AttributeError:
        product_name = ""

    return product_name

#price
def get_price(soup):
    try:
        price = soup.find("p", attrs={'class': 'Typography_body1___zS6E Typography_text-black__NvbF0 Typography_font-bold__vh2cV Price_root__Mo4Q_'}).text
        pattern = r"RM\D*"
        price = re.sub(pattern, "RM ", price)
    except:
            price = ""

    return price

#size
def get_size(soup):
    try:
        size_tags = soup.find_all("button",  attrs={'class': 'Swatch_root__urRF_ Swatch_fullWidth__0wgz1', 'data-testid': 'swatch-button-enabled'})
        sizes = [button.text.strip() for button in size_tags]
        sizes_string = ', '.join(sizes)
    except:
        sizes_string = ""

    return sizes_string

#shoe type
def get_shoe_type(soup):
    try:
        table_features = soup.find('dl', attrs={'class': 'ProductFeatures_list__P5nrt'}).text
        pattern = r'Activity([A-Z][a-z]*)'
        type = re.search(pattern, table_features)

        if type:
            type = type.group(1)  
            
        else:
            type = None
    except:
            type = ""

    return type
    

#gender
def get_gender(soup):
    try:
        table_features = soup.find('dl', attrs={'class': 'ProductFeatures_list__P5nrt'}).text
        pattern = r'Gender([A-Z][a-z]*)'
        gender = re.search(pattern, table_features)
        if gender:
            gender = gender.group(1)  
           
        else:
            gender = None
    except:
            gender = ""

    return gender

if __name__ == '__main__':
    # URL of the website you want to scrape
    url = 'https://www.sportsdirect.com.my/search?q=asics'

    # Headers for request
    HEADERS = ({'User-Agent': 'Mozi|lla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    # HTTP Request
    webpage = requests.get(url, headers=HEADERS)

    # Parse the HTML content
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': 'Link_root__TBCX5 ProductCard_link__cCkNX'})

    links_list = []

    d = {"product":[], "price":[], "size_available":[], "type_of_sport":[],"gender":[]}

    for link in links:
        # Extract the href attribute from the tag object
        href = link.get('href')
        if href:
            # Construct the full URL
            full_url = "https://www.sportsdirect.com.my/" + href
            
            try:
                # Make the request using the constructed URL
                new_webpage = requests.get(full_url, headers=HEADERS)
                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Function calls to extract product information
                d['product'].append(get_product(new_soup))
                d['price'].append(get_price(new_soup))
                d['size_available'].append(get_size(new_soup))
                d['type_of_sport'].append(get_shoe_type(new_soup))
                d['gender'].append(get_gender(new_soup))

                # Log the URL if successfully processed
                print(f"Processed: {full_url}")
                
            except Exception as e:
                print(f"Error processing {full_url}: {str(e)}")
       
    asics_df = pd.DataFrame.from_dict(d)
    asics_df['product'].replace('', np.nan, inplace=True)
    asics_df = asics_df.dropna(subset=['product'])
    asics_df.to_csv("asics_data.csv", header=True, index=False)


    

    

