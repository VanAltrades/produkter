# cse (ascii - small keyboard)
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from pandas import json_normalize

# url (ascii - digital)
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

class SearchEngine:
    
    def __init__(self, sa_credentials_path="dukt_sa.json", cx_path="cs_key.json"):
        
        self.credentials = self.load_credentials(sa_credentials_path)
        self.service = build("customsearch", "v1", credentials=self.credentials)
        self.cx = self.load_cx(cx_path)
        self.serp_dicts = None
        self.serp_url_dicts = None

        self.ua = UserAgent()


    @staticmethod
    def load_credentials(sa_credentials_path):
        # if os.path.exists(sa_credentials_path):
        return service_account.Credentials.from_service_account_file(
            sa_credentials_path, 
            scopes=["https://www.googleapis.com/auth/cse"]
        )
    

    @staticmethod
    def load_cx(cx_path):
        with open(cx_path, 'r') as file:
            data = json.load(file)
        return data["key"]
    

    @staticmethod
    def save_to_json(data, output_file):
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=2)


    @staticmethod
    def print_json(js):
        print(json.dumps(js, indent=2))


    #  ____ ____ ____ 
    # ||c |||s |||e ||
    # ||__|||__|||__||
    # |/__\|/__\|/__\|
    def search(self, query, **kwargs):        
        d = self.service.cse().list(q=query, cx=self.cx, **kwargs).execute()
        self.serp_dicts = self.load_serp_dicts(d)
        return d # json data


    def load_serp_dicts(self, d):
        serp_dicts = d.get('items', [])
        return serp_dicts


    #  +-+-+-+-+
    #  |s|e|r|p|
    #  +-+-+-+-+
    def get_primary_dicts(self, serp_dicts):
        keys_to_extract = ['title','link','displayLink','snippet']

        # Create a list of dictionaries from nested keys
        return [{key: result.get(key,None) for key in keys_to_extract} for result in serp_dicts]


    def get_metatags_dicts(self, serp_dicts):
        keys_to_extract = ['og:type','og:site_name','title','og:title','og:description','image']

        # Create a list of dictionaries from nested keys
        return [{key: result['pagemap']['metatags'][0].get(key,None) for key in keys_to_extract} for result in serp_dicts]
    

    def get_image_dicts(self, serp_dicts):
        keys_to_extract = ['src']

        # Create a list of dictionaries from nested keys
        return [{key: result['pagemap']['cse_image'][0].get(key,None) for key in keys_to_extract} for result in serp_dicts]


    def get_serp_dicts(self, serp_dicts):
        # returns a list of search engine result dicts with only desired keys
        primary = self.get_primary_dicts(serp_dicts)
        meta = self.get_metatags_dicts(serp_dicts)
        img = self.get_image_dicts(serp_dicts)

        serp_dict = []

        for dict1, dict2, dict3 in zip(primary, meta, img):
            combined_dict = {**dict1, **dict2, **dict3}
            serp_dict.append(combined_dict)
        
        self.serp_dicts = serp_dict
        return serp_dict


    #  +-+-+-+
    #  |u|r|l|
    #  +-+-+-+
    def get_serp_links(self):
        try:
            links = [item['link'] if 'link' in item else None for item in self.serp_dicts]
            return links
        except:
            raise NameError("No `serp_dicts` JSON. Run se.get_serp_dicts() first")
        

    def get_url_soup(self, url):
        headers = {'User-Agent': self.ua.random}
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            print(f"Failed to retrieve the page: \n{url}. \n\nStatus Code: {response.status_code}")
            return None
        
    
    def get_schema(soup):
        if soup is not None:
            soup_script = soup.find("script", {"type":"application/ld+json"})
            if soup_script is not None:
                schema = json.loads("".join(soup_script.contents))
                return schema
            else:
                return None
        else:
            return None
        
    
    def get_product_name(schema):
        if schema['name'] is not None:
            product_name = schema['name']
            return product_name
        else:
            return None
        

    def get_product_price(schema):
        if schema['offers']['price'] is not None:
            product_price = schema['offers']['price']
            return product_price
        else:
            return None
        

se = SearchEngine()
d = se.search('milwaukee m18 fuel')

# serp level
serp_dicts = se.load_serp_dicts(d)
se.save_to_json(serp_dicts,"./data/serp_dicts.json")

serp_dicts = se.get_serp_focus(serp_dicts) # TODO: remove serp_dicts arg and use self.serp_dicts
se.save_to_json(serp_dicts,"./data/serp_dicts_focus.json")

# url level
links = se.get_serp_links()
# se.get_url_soup()