# https://github.com/sundios/Keyword-generator-SEO/blob/master/suggestqueries.py
import requests
import json
import pandas as pd

class Suggestions:
    
    def __init__(self, keyword_list):
        
        self.base_url = "http://suggestqueries.google.com/complete/search?output=firefox&q="
        self.base_url_shopping = "http://suggestqueries.google.com/complete/search?output=firefox&ds=sh&q=" # shopping results

        self.keyword_list = keyword_list

        self.questions = None
        # TODO: combine prefix and suffix dictionaries into one self.suggestions



    def get_questions(self):
        prefixes = ['how', 'which', 'why', 'where', 'who', 'when', 'are', 'what']
        result_dict = {}

        for i, keyword in enumerate(self.keyword_list):
            keyword_dict = {}

            for prefix in prefixes:
                url = self.base_url + prefix + " " + keyword 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                
                if kws:
                    keyword_dict[prefix] = kws
                else:
                    keyword_dict[prefix] = None

            result_dict[keyword] = keyword_dict

        return result_dict


    def get_prefix_suggestions(self):
        prefixes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'y', 'x', 'y', 'z']
        result_dict = {}

        for keyword in self.keyword_list:
            keyword_list = []

            for prefix in prefixes:
                url = self.base_url + prefix + " " + keyword 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                keyword_list.extend(kws)

            result_dict[keyword] = keyword_list

        return result_dict


    def get_suffix_suggestions(self):
        suffixes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'y', 'x', 'y', 'z']
        result_dict = {}

        for keyword in self.keyword_list:
            keyword_list = []

            for suffix in suffixes:
                url = self.base_url + keyword + " " + suffix 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                keyword_list.extend(kws)

            result_dict[keyword] = keyword_list

        return result_dict