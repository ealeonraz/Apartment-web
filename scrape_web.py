import requests
from bs4 import BeautifulSoup
import json
import re

# Function to scrape home listings from Zillow
def build_json_object(address_, links_, prices_, description_):
    all_listings = []
    with open('listings.json', 'w') as json_file:
        for i in range(len(address_)):
            new_listing = {
                "Link to post": links_[i],
                "Address": address_[i],
                "Description": description_[i],
                "Price": prices_[i]
            }
            all_listings.append(new_listing)
        return all_listings
def scrape_zillow():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}
    url = 'https://www.zillow.com/sacramento-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22price%22%3A%7B%22max%22%3A1000%7D%2C%22isMultiFamily%22%3A%7B%22value%22%3Afalse%7D%2C%22isManufactured%22%3A%7B%22value%22%3Afalse%7D%2C%22isLotLand%22%3A%7B%22value%22%3Afalse%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-121.82977211914063%2C%22east%22%3A-121.10192788085938%2C%22south%22%3A38.34009975758793%2C%22north%22%3A38.87666015783239%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20288%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A1000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22usersSearchTerm%22%3A%22Sacramento%20CA%22%7D'
    response = requests.get(url, headers = headers, timeout=30)
    address_list = []
    links_list = []
    prices_list = []
    description_list = []
    name_pattern = r'^(.*?),'
    rent_pattern = r'(\$[\d,]+/mo)'
    address_pattern = r'^(.*\d)(?=\$)'
    description = r'\$[\d,]+/mo(.+)Save this home'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_description_ul = soup.find('ul', class_="photo-cards")
        address_find = soup.find_all('address', attrs={'data-test': 'property-card-addr'})
        link_to_posts = soup.find_all('a', class_="property-card-link")

        for i in link_to_posts:
            href = i.get('href')
            if href in links_list:
                continue
            elif(href[0].isalpha()):
                links_list.append(href)
            else:
                continue
        
        for i in text_description_ul:
            if (re.search(rent_pattern, i.text) == None):
                continue
            elif (re.search(rent_pattern, i.text)):
                rent_price_match = re.search(rent_pattern, i.text)
                prices_list.append(rent_price_match.group(0))
                address_match = re.search(address_pattern, i.text)
                address_list.append(address_match.group(0))
                description_match = re.search(description, i.text)
                description_list.append(description_match.group(1))
            else:
                continue
        final_object = build_json_object(address_list, links_list, prices_list, description_list)
        with open('listings.json', 'w') as json_file:
            json.dump(final_object, json_file, indent=4)
        
    else:
        print('Failed to retrieve data from Zillow. Status code:', response.status_code)
        return []
# Main function to scrape listings from multiple websites
def main():
    scrape_zillow()

if __name__ == '__main__':
    main()
