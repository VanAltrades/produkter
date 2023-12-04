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

        # self.serp_dicts = None
        self.serp_dicts = self.load_json_from_file("./data/se_results.json") # TESTING

        self.serp_schema_dicts = None
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
    def load_json_from_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


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
        
    #  +-+-+-+
    #  |u|r|l| schema
    #  +-+-+-+
    def get_schema(self, soup):
        if soup is not None:
            soup_script = soup.find("script", {"type":"application/ld+json"})
            if soup_script is not None:
                schema = json.loads("".join(soup_script.contents))
                return schema
            else:
                return None
        else:
            return None
        

    def get_schema_dicts(self):
        # links from serp
        links = self.get_serp_links()

        # collect schema json from each link and append to list
        schema_dicts = []
        for link in links:
            soup = self.get_url_soup(link)
            schema = self.get_schema(soup)
            schema_dicts.append(schema)
        self.serp_schema_dicts = schema_dicts
        return schema_dicts
    

    def get_product_schema_nested_key_value(self, schema, *keys):
        # abstract schema extract function
        current_level = schema

        for key in keys:
            if current_level is not None and key in current_level:
                current_level = current_level[key]
            else:
                return None

        return "_".join(keys), current_level  # Concatenate keys into a single string


    def get_product_schema_item_dicts(self, schema_dicts, *keys):
        item_dicts = []
        for schema in schema_dicts:
            result = self.get_product_schema_nested_key_value(schema, *keys)
            key, value = result if result is not None else ("_".join(keys), None) # remove else if only want non-None
            item_dict = {key: value}
            item_dicts.append(item_dict)
        return item_dicts
    

    ## logic check ##
    def all_values_none(list_of_dicts):
        # Check if all values in all dictionaries are None - True if all None
        return all(all(value is None for value in d.values()) for d in list_of_dicts)

    ## filter ##
    def filter_dicts_with_values(list_of_dicts):
        # Filter dictionaries to include only those with values not equal to None
        return [d for d in list_of_dicts if any(value is not None for value in d.values())]



    def get_url_schema_dicts(self, schema_dicts):
        # returns a list of url schema dicts with only desired keys
        # https://schema.org/Product
        schema_keys = [
            # id
            'productID','sku','gtin','gtin8','gtin12','gtin13','model','mpn','asin',
            # product
            'name', 'description',['brand', 'name'],'manufacturer','image','category',['offers','price'],['offers','availability'], # TODO: strip("https://schema.org/","")
            # niche
            'audience','keywords','slogan',['hasMerchantReturnPolicy','merchantReturnDays'], # TODO: confirm
            # taxonomy
            ['BreadcrumbList','itemListElement','name'], #TODO: confirm 
            # reviews
            ['aggregateRating','ratingValue'],'review',
            # attributes
            'depth','height','width','color','weight','material','pattern','size','countryOfOrigin','countryOfAssembly','countryOfLastProcessing',
            # relation
            'isAccessoryOrSparePartFor','isConsumableFor','isRelatedTo','isSimilarTo','isVariantOf',['mainEntity','offers','itemOffered']
        ]
        
        url_schema_dicts = []
        
        for key in schema_keys:
            if type(key) == str:
                url_schema_dict = self.get_product_schema_item_dicts(schema_dicts,key)
            else:
                url_schema_dict = self.get_product_schema_item_dicts(schema_dicts,*key)
            url_schema_dicts.append(url_schema_dict)
        
        self.serp_url_dicts = url_schema_dicts
        return url_schema_dicts


    def list_schema_keys(self):
        # Flatten the list of lists
        flat_list = [item for sublist in self.serp_url_dicts for item in sublist]

        # Get all distinct keys
        distinct_keys = set(key for item in flat_list for key in item.keys())

        print(distinct_keys)


    def get_schema_key(self, key):
        # Flatten the list of lists
        flat_list = [item for sublist in self.serp_url_dicts for item in sublist]

        # Filter dictionaries with a non-None 'name' value
        filtered_dicts = [item for item in flat_list if item.get('name') is not None]

        result_dict = {key: [item[key] for item in filtered_dicts]}
        return result_dict
    

    #  +-+-+-+
    #  |u|r|l| corpus
    #  +-+-+-+
    


se = SearchEngine()
d = se.search('milwaukee m18 fuel')

# serp level
# serp_dicts = se.load_serp_dicts(d)
# se.save_to_json(serp_dicts,"./data/serp_dicts.json")

# se rp_dicts = se.get_serp_dicts(serp_dicts) # TODO: remove serp_dicts arg and use self.serp_dicts
# se.save_to_json(serp_dicts,"./data/serp_dicts_focus.json")

# TEST EXAMPLE of above code ^
serp_dicts = se.serp_dicts
schema_dicts = se.get_schema_dicts()


# serp url level
links = se.get_serp_links()

schema_dicts = se.get_schema_dicts(links)

i = se.get_product_schema_item_dicts(schema_dicts,"name")

# below should encompass all of above code
serp_url_dicts = se.get_url_schema_dicts(schema_dicts)

# THE CODE HERE SHOULD PROBABLY RUN AUTOMATICALLY AND 
# POPULATE INSTANCE VARIABLES.
# THIS WILL ALLOW THE CLASS TO WORK MORE WITH 
# get_schema(key) AND RETURN items() FOR OTHER
# API RESPONSES.

se.list_keys()

product_names = se.get_schema_key("name")
product_price = se.get_schema_key('offers_availability')
product_price = se.get_schema_key('mainEntity_offers_itemOffered')