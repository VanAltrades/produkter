# cse (ascii - small keyboard)
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from pandas import json_normalize


class Engine:
    
    def __init__(self, query, sa_credentials_path, cx_path, **enginekwargs):
        
        self.credentials = self.load_credentials(sa_credentials_path)
        self.service = build("customsearch", "v1", credentials=self.credentials)
        self.cx = self.load_cx(cx_path)
        self.keyword = query

        self.engine = None
        self.results = self.search(query, **enginekwargs)

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
    def search(self, query, **enginekwargs):        
        d = self.service.cse().list(q=query, cx=self.cx, **enginekwargs).execute()
        self.engine = d
        try:
            results = d.get('items')
            self.results = results
            return results
        except Exception as e:
            return e


    

class SearchDictionary:
    def __init__(self, engine_instance):
        # Assuming engine_instance is an instance of the Engine class
        self.results = engine_instance.results
        self.dictionary = self.get_dictionary_dict()
        # You can now use self.results in the Rank class or perform additional operations.

    #  +-+-+-+-+
    #  |s|e|r|p|
    #  +-+-+-+-+
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

    def get_dictionary_dict(self):
        dictionary = {}
        
        for i, result in enumerate(self.results):
            rank = {}

            link = self.safe_get(result, 'link', default=None) # link = result.get('link', None)
            # Store the values in the dictionary, even if they are None
            rank['link'] = link
            
            # site = result.get('displayLink', None)
            site = self.safe_get(result, 'displayLink', default=None) 
            rank['site'] = site

            # site2 = result['pagemap']['metatags'][0].get('og:site_name', None)
            site2 = self.safe_get(result, 'pagemap', 'metatags', 0, 'og:site_name', default=None) # result['pagemap']['metatags'][0].get('og:site_name', None)
            rank['site2'] = site2
    
            # pagetype = result['pagemap']['metatags'][0].get('og:type', None)
            pagetype = self.safe_get(result, 'pagemap', 'metatags', 0, 'og:type', default=None)
            rank['pagetype'] = pagetype
    
            # title = result.get('title', None)
            title = self.safe_get(result, 'title', default=None)
            rank['title'] = title
            
            # title2 = result['pagemap']['metatags'][0].get('title', None)
            title2 = self.safe_get(result, 'pagemap', 'metatags', 0, 'title', default=None)
            rank['title2'] = title2

            # title3 = result['pagemap']['metatags'][0].get('og:title', None)
            title3 = self.safe_get(result, 'pagemap', 'metatags', 0, 'og:title', default=None)
            rank['title3'] = title3

            # description = result['pagemap']['metatags'][0].get('og:description', None)
            description = self.safe_get(result, 'pagemap', 'metatags', 0, 'og:description', default=None)
            rank['description'] = description

            # snippet = result.get('snippet', None)
            snippet = self.safe_get(result, 'snippet', default=None)
            rank['snippet'] = snippet
            
            # image = result['pagemap']['metatags'][0].get('image', None)
            image = self.safe_get(result, 'pagemap', 'metatags', 0, 'image', default=None)
            rank['image'] = image

            image2 = self.safe_get(result, 'pagemap', 'cse_image', 0, 'src', default=None)
            rank['image2'] = image2

            dictionary[i] = rank

        self.dictionary = dictionary
        return dictionary



# # Example usage:
# engine_instance = Engine("milwaukee m18 fuel")
# engine_instance = Engine("AMD Ryzen 9 5900X")

# # Create an instance of Rank and automatically pass the results
# rank_instance = SearchDictionary(engine_instance)

# # Now you can access rank_instance.results
# print(rank_instance.results)