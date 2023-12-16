# https://github.com/sundios/Keyword-generator-SEO/blob/master/suggestqueries.py
import requests
import json
import pandas as pd

class Suggestions:
    
    def __init__(self, language_processor_instance):
        
        self.base_url = "http://suggestqueries.google.com/complete/search?output=firefox&q="
        self.base_url_shopping = "http://suggestqueries.google.com/complete/search?output=firefox&ds=sh&q=" # shopping results

        self.keyword_list = language_processor_instance.items

        self.question_queries = self.get_questions()
        self.comparison_queries = self.get_comparisons()
        self.suggested_queries = self.get_suggestions()
        # TODO: combine prefix and suffix dictionaries into one self.suggestions



    def get_questions(self):
        result_dict = {}

        for keyword in self.keyword_list:
            unique_kws = set()  # Use a set to ensure uniqueness

            for prefix in ['how', 'which', 'why', 'where', 'who', 'when', 'are', 'what']:
                url = self.base_url + prefix + " " + keyword 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                
                if kws:
                    unique_kws.update(kws)

            result_dict[keyword] = list(unique_kws)

        return result_dict


    def get_comparisons(self):
        result_dict = {}

        for keyword in self.keyword_list:
            unique_kws = set()  # Use a set to ensure uniqueness

            for prefix in ['vs', 'versus']:
                url = self.base_url + prefix + " " + keyword 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                
                if kws:
                    unique_kws.update(kws)

            result_dict[keyword] = list(unique_kws)

        return result_dict


    def get_suggestions(self):
        result_dict = {}
        characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'y', 'x', 'y', 'z']

        for keyword in self.keyword_list:
            keyword_set = set()  # Use a set to ensure uniqueness

            for character in characters:
                url_prefix = self.base_url + f"{character} {keyword}"
                url_suffix = self.base_url + f"{keyword} {character}"
                
                # url_prefix
                response = requests.get(url_prefix, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                keyword_set.update(kws)

                # url_suffix
                response = requests.get(url_suffix, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                keyword_set.update(kws)

            result_dict[keyword] = sorted(list(keyword_set))

        return result_dict