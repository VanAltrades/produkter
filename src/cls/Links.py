# url (ascii - digital)
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

class Links:
    def __init__(self, rank_instance):
        # Assuming rank_instance is an instance of the rank class
        self.links = [item['link'] if 'link' in item else None for item in rank_instance.ranks.values()]
        self.ua = UserAgent()
        self.schema = self.get_schema_dict()


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
        

    @staticmethod
    def safe_get(dictionary, *keys, default=None):
        for key in keys:
            if isinstance(dictionary, dict) and key in dictionary:
                dictionary = dictionary[key]
            elif isinstance(dictionary, list) and isinstance(key, int) and 0 <= key < len(dictionary):
                dictionary = dictionary[key]
            else:
                return default
        return dictionary
    

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
        

    def get_schema_dict(self):
        # collect schema json from each link and append to list
        schemas = {}
        for i, link in enumerate(self.links):
            schema = {}

            soup = self.get_url_soup(link)
            sche = self.get_schema(soup)
            
            name = self.safe_get(sche, 'name', default=None) 
            schema['name'] = name
            
            # TODO: get all schema in scope and append to schema dict
            # schema_keys = [
            #     # id
            #     'productID','sku','gtin','gtin8','gtin12','gtin13','model','mpn','asin',
            #     # product
            #     'name', 'description',['brand', 'name'],'manufacturer','image','category',['offers','price'],['offers','availability'], # TODO: strip("https://schema.org/","")
            #     # niche
            #     'audience','keywords','slogan',['hasMerchantReturnPolicy','merchantReturnDays'], # TODO: confirm
            #     # taxonomy
            #     ['BreadcrumbList','itemListElement','name'], #TODO: confirm 
            #     # reviews
            #     ['aggregateRating','ratingValue'],'review',
            #     # attributes
            #     'depth','height','width','color','weight','material','pattern','size','countryOfOrigin','countryOfAssembly','countryOfLastProcessing',
            #     # relation
            #     'isAccessoryOrSparePartFor','isConsumableFor','isRelatedTo','isSimilarTo','isVariantOf',['mainEntity','offers','itemOffered']
            # ]

            schemas[i] = schema
        
        self.schemas = schemas
        return schemas