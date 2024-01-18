# url (ascii - digital)
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class Sites:
    def __init__(self, search_dictionary_instance):
        # Assuming search_dictionary_instance is an instance of the rank class
        # self.links = [item['link'] if 'link' in item else None for item in search_dictionary_instance.dictionary.values()]
        # self.titles = [item['title'] if 'title' in item else None for item in search_dictionary_instance.dictionary.values()]
        try:
            self.links = search_dictionary_instance.links
        except: # from __json__()
            self.links = search_dictionary_instance['links']
        try:
            self.titles = search_dictionary_instance.titles
        except: # from __json__()
            self.titles = search_dictionary_instance['titles']

        self.ua = UserAgent()
        
        self.dictionary_schemas = self.get_schema_dict()
        self.dictionary_texts = self.get_text_dict()


    def __json__(self):
        return {
            'schemas': self.dictionary_schemas,
            'texts': self.dictionary_texts
        }
    

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
                json_data = "".join(soup_script.contents)
                cleaned_json_data = re.sub(r'[^\x20-\x7E]', '', json_data)
                schema = json.loads(cleaned_json_data)
                return schema
            else:
                return None
        else:
            return None
        

    def get_schema_dict(self):
        schemas = {}

        def process_link(i, link):
            schema = {}
            soup = self.get_url_soup(link)
            sch = self.get_schema(soup)

            # id
            productID = self.safe_get(sch, 'productID', default=None) 
            schema['productID'] = productID

            sku = self.safe_get(sch, 'sku', default=None) 
            schema['sku'] = sku
            
            gtin = self.safe_get(sch, 'gtin', default=None) 
            schema['gtin'] = gtin

            gtin8 = self.safe_get(sch, 'gtin8', default=None) 
            schema['gtin8'] = gtin8

            gtin12 = self.safe_get(sch, 'gtin12', default=None) 
            schema['gtin12'] = gtin12

            gtin13 = self.safe_get(sch, 'gtin13', default=None) 
            schema['gtin13'] = gtin13

            model = self.safe_get(sch, 'model', default=None) 
            schema['model'] = model

            mpn = self.safe_get(sch, 'mpn', default=None) 
            schema['mpn'] = mpn

            asin = self.safe_get(sch, 'asin', default=None) 
            schema['asin'] = asin

            # product
            name = self.safe_get(sch, 'name', default=None) 
            schema['name'] = name

            description = self.safe_get(sch, 'description', default=None) 
            schema['description'] = description

            brand_name = self.safe_get(sch, 'brand', 'name', default=None) 
            schema['brand_name'] = brand_name

            manufacturer = self.safe_get(sch, 'manufacturer', default=None) 
            schema['manufacturer'] = manufacturer

            image = self.safe_get(sch, 'image', default=None) 
            schema['image'] = image

            category = self.safe_get(sch, 'category', default=None) 
            schema['category'] = category

            offers_price = self.safe_get(sch, 'offers', 'price', default=None) 
            schema['offers_price'] = offers_price

            offers_availability = self.safe_get(sch, 'offers', 'availability', default=None) 
            if offers_availability is not None:
                offers_availability = offers_availability.replace('http://schema.org/','')
            schema['offers_availability'] = offers_availability

            # niche
            audience = self.safe_get(sch, 'audience', default=None) 
            schema['audience'] = audience

            keywords = self.safe_get(sch, 'keywords', default=None) 
            schema['keywords'] = keywords

            slogan = self.safe_get(sch, 'slogan', default=None) 
            schema['slogan'] = slogan

            return_window = self.safe_get(sch, 'hasMerchantReturnPolicy', 'merchantReturnDays', default=None) 
            schema['return_window'] = return_window # TODO: confirm

            # taxonomy
            taxonomy = self.safe_get(sch, 'BreadcrumbList', 'itemListElement', 'name', default=None) 
            schema['taxonomy'] = taxonomy # TODO: confirm

            # reviews
            review_value = self.safe_get(sch, 'aggregateRating', 'ratingValue', default=None) 
            schema['review_value'] = review_value

            review = self.safe_get(sch, 'review', default=None) 
            schema['review'] = review

            # attributes
            depth = self.safe_get(sch, 'depth', default=None) 
            schema['depth'] = depth

            height = self.safe_get(sch, 'height', default=None) 
            schema['height'] = height

            width = self.safe_get(sch, 'width', default=None) 
            schema['width'] = width

            color = self.safe_get(sch, 'color', default=None) 
            schema['color'] = color

            weight = self.safe_get(sch, 'weight', default=None) 
            schema['weight'] = weight

            material = self.safe_get(sch, 'material', default=None) 
            schema['material'] = material

            pattern = self.safe_get(sch, 'pattern', default=None) 
            schema['pattern'] = pattern

            size = self.safe_get(sch, 'size', default=None) 
            schema['size'] = size

            country_origin = self.safe_get(sch, 'countryOfOrigin', default=None) 
            schema['country_origin'] = country_origin

            country_assembly = self.safe_get(sch, 'countryOfAssembly', default=None) 
            schema['country_assembly'] = country_assembly

            country_last_process = self.safe_get(sch, 'countryOfLastProcessing', default=None) 
            schema['country_last_process'] = country_last_process

            # relation
            accessory_part_for = self.safe_get(sch, 'isAccessoryOrSparePartFor', default=None) 
            schema['accessory_part_for'] = accessory_part_for

            consumable_for = self.safe_get(sch, 'isConsumableFor', default=None) 
            schema['consumable_for'] = consumable_for

            related_to = self.safe_get(sch, 'isRelatedTo', default=None) 
            schema['related_to'] = related_to

            similar_to = self.safe_get(sch, 'isSimilarTo', default=None) 
            schema['similar_to'] = similar_to

            variant_of = self.safe_get(sch, 'isVariantOf', default=None) 
            schema['variant_of'] = variant_of

            item_offer = self.safe_get(sch, 'mainEntity', 'offers', 'itemOffered', default=None) 
            schema['item_offer'] = item_offer

            return i, schema

        with ThreadPoolExecutor() as executor:
            # Use executor.map to parallelize the processing of links
            futures = [executor.submit(process_link, i, link) for i, link in enumerate(self.links)]

            # Wait for all tasks to complete and collect results
            for future in concurrent.futures.as_completed(futures):
                i, schema = future.result()
                schemas[i] = schema

        return schemas
        

    def get_text_dict(self):
        texts = {}

        def process_link(i, link):
            text = {}
            soup = self.get_url_soup(link)
            if soup is not None:
                text = soup.get_text()
                text = text.replace("\n", " ")
                text = text.replace("\r", " ")
                text = text.replace("\t", " ")
            return i, text

        with ThreadPoolExecutor() as executor:
            # Use executor.map to parallelize the processing of links
            futures = [executor.submit(process_link, i, link) for i, link in enumerate(self.links)]

            # Wait for all tasks to complete and collect results
            for future in concurrent.futures.as_completed(futures):
                i, text = future.result()
                texts[i] = text

        return texts
    
# NON-CONCURRENT SCRAPING
    # def get_schema_dict(self):
    #     # collect schema json from each link and append to list
    #     schemas = {}
    #     for i, link in enumerate(self.links):
    #         schema = {}

    #         soup = self.get_url_soup(link)
    #         sch = self.get_schema(soup)
    
    #         # id
    #         productID = self.safe_get(sch, 'productID', default=None) 
    #         schema['productID'] = productID

    #         sku = self.safe_get(sch, 'sku', default=None) 
    #         schema['sku'] = sku
            
    #         gtin = self.safe_get(sch, 'gtin', default=None) 
    #         schema['gtin'] = gtin

    #         gtin8 = self.safe_get(sch, 'gtin8', default=None) 
    #         schema['gtin8'] = gtin8

    #         gtin12 = self.safe_get(sch, 'gtin12', default=None) 
    #         schema['gtin12'] = gtin12

    #         gtin13 = self.safe_get(sch, 'gtin13', default=None) 
    #         schema['gtin13'] = gtin13

    #         model = self.safe_get(sch, 'model', default=None) 
    #         schema['model'] = model

    #         mpn = self.safe_get(sch, 'mpn', default=None) 
    #         schema['mpn'] = mpn

    #         asin = self.safe_get(sch, 'asin', default=None) 
    #         schema['asin'] = asin

    #         # product
    #         name = self.safe_get(sch, 'name', default=None) 
    #         schema['name'] = name

    #         description = self.safe_get(sch, 'description', default=None) 
    #         schema['description'] = description

    #         brand_name = self.safe_get(sch, 'brand', 'name', default=None) 
    #         schema['brand_name'] = brand_name

    #         manufacturer = self.safe_get(sch, 'manufacturer', default=None) 
    #         schema['manufacturer'] = manufacturer

    #         image = self.safe_get(sch, 'image', default=None) 
    #         schema['image'] = image

    #         category = self.safe_get(sch, 'category', default=None) 
    #         schema['category'] = category

    #         offers_price = self.safe_get(sch, 'offers', 'price', default=None) 
    #         schema['offers_price'] = offers_price

    #         offers_availability = self.safe_get(sch, 'offers', 'availability', default=None) 
    #         if offers_availability is not None:
    #             offers_availability = offers_availability.replace('http://schema.org/','')
    #         schema['offers_availability'] = offers_availability

    #         # niche
    #         audience = self.safe_get(sch, 'audience', default=None) 
    #         schema['audience'] = audience

    #         keywords = self.safe_get(sch, 'keywords', default=None) 
    #         schema['keywords'] = keywords

    #         slogan = self.safe_get(sch, 'slogan', default=None) 
    #         schema['slogan'] = slogan

    #         return_window = self.safe_get(sch, 'hasMerchantReturnPolicy', 'merchantReturnDays', default=None) 
    #         schema['return_window'] = return_window # TODO: confirm

    #         # taxonomy
    #         taxonomy = self.safe_get(sch, 'BreadcrumbList', 'itemListElement', 'name', default=None) 
    #         schema['taxonomy'] = taxonomy # TODO: confirm

    #         # reviews
    #         review_value = self.safe_get(sch, 'aggregateRating', 'ratingValue', default=None) 
    #         schema['review_value'] = review_value

    #         review = self.safe_get(sch, 'review', default=None) 
    #         schema['review'] = review

    #         # attributes
    #         depth = self.safe_get(sch, 'depth', default=None) 
    #         schema['depth'] = depth

    #         height = self.safe_get(sch, 'height', default=None) 
    #         schema['height'] = height

    #         width = self.safe_get(sch, 'width', default=None) 
    #         schema['width'] = width

    #         color = self.safe_get(sch, 'color', default=None) 
    #         schema['color'] = color

    #         weight = self.safe_get(sch, 'weight', default=None) 
    #         schema['weight'] = weight

    #         material = self.safe_get(sch, 'material', default=None) 
    #         schema['material'] = material

    #         pattern = self.safe_get(sch, 'pattern', default=None) 
    #         schema['pattern'] = pattern

    #         size = self.safe_get(sch, 'size', default=None) 
    #         schema['size'] = size

    #         country_origin = self.safe_get(sch, 'countryOfOrigin', default=None) 
    #         schema['country_origin'] = country_origin

    #         country_assembly = self.safe_get(sch, 'countryOfAssembly', default=None) 
    #         schema['country_assembly'] = country_assembly

    #         country_last_process = self.safe_get(sch, 'countryOfLastProcessing', default=None) 
    #         schema['country_last_process'] = country_last_process

    #         # relation
    #         accessory_part_for = self.safe_get(sch, 'isAccessoryOrSparePartFor', default=None) 
    #         schema['accessory_part_for'] = accessory_part_for

    #         consumable_for = self.safe_get(sch, 'isConsumableFor', default=None) 
    #         schema['consumable_for'] = consumable_for

    #         related_to = self.safe_get(sch, 'isRelatedTo', default=None) 
    #         schema['related_to'] = related_to

    #         similar_to = self.safe_get(sch, 'isSimilarTo', default=None) 
    #         schema['similar_to'] = similar_to

    #         variant_of = self.safe_get(sch, 'isVariantOf', default=None) 
    #         schema['variant_of'] = variant_of

    #         item_offer = self.safe_get(sch, 'mainEntity', 'offers', 'itemOffered', default=None) 
    #         schema['item_offer'] = item_offer

    #         schemas[i] = schema
        
    #     return schemas


    # def get_text_dict(self):
    #     # collect soup text from each link and append to list
    #     texts = {}
    #     for i, link in enumerate(self.links):
    #         text = {}

    #         soup = self.get_url_soup(link)
    #         if soup is not None:
    #             text = soup.get_text()
    #             text = text.replace("\n"," ")
    #             text = text.replace("\r"," ")
    #             text = text.replace("\t"," ")
    #             texts[i] = text
    #         else:
    #             texts[i] = None

    #     return texts