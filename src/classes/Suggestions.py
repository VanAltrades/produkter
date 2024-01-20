# https://github.com/sundios/Keyword-generator-SEO/blob/master/suggestqueries.py
import requests
import json

class Suggestions:
    
    # def __init__(self, language_processor_instance):
    def __init__(self, q):
        
        self.base_url = "http://suggestqueries.google.com/complete/search?output=firefox&q="
        self.base_url_shopping = "http://suggestqueries.google.com/complete/search?output=firefox&ds=sh&q=" # shopping results

        # self.keyword_list = language_processor_instance.items
        self.keyword_list = [q] #TODO: then add language_processor_instance.items if not null

        # self.questions = self.get_questions()
        # self.comparisons = self.get_comparisons()
        # self.suggestions = self.get_suggestions()

        # get dictionaries from existing instance json, otherwise run request
        # try: # from __json__()
        #     print("got questions dict from the existing instance's json")
        #     self.questions = self['questions']
        # except: 
        #     print("got questions dict from running get_questions()")
        #     self.questions = self.get_questions()
        # try: # from __json__()
        #     print("got comparisons dict from the existing instance's json")
        #     self.comparisons = self['comparisons']
        # except: 
        #     print("got comparisons dict from running get_comparisons()")
        #     self.comparisons = self.get_comparisons()
        # try: # from __json__()
        #     self.suggestions = self['suggestions']
        # except: 
        #     self.suggestions = self.get_suggestions()


    def __json__(self):
        return {
            'questions': self.get_questions(),
            'comparisons': self.get_comparisons(),
            'suggestions': self.get_suggestions()
        }
    

    def get_questions(self):
        for keyword in self.keyword_list:
            unique_kws = set()  # Use a set to ensure uniqueness

            for prefix in ['how', 'which', 'why', 'where', 'who', 'when', 'are', 'what']:
                url = self.base_url + prefix + " " + keyword 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                
                if kws:
                    unique_kws.update(kws)

            result_list = list(unique_kws)

        return result_list


    def get_comparisons(self):
        for keyword in self.keyword_list:
            unique_kws = set()  # Use a set to ensure uniqueness

            for prefix in ['vs', 'versus']:
                url = self.base_url + prefix + " " + keyword 
                response = requests.get(url, verify=False)
                suggestions = json.loads(response.text)

                kws = suggestions[1]
                
                if kws:
                    unique_kws.update(kws)

            result_list = list(unique_kws)

        return result_list


    def get_suggestions(self):
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

            result_list = sorted(list(keyword_set))

        return result_list