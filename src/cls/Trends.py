# gtrends scrape alternative: https://stackoverflow.com/questions/56340866/access-google-trends-data-without-a-wrapper-or-with-the-api-python
from pytrends.request import TrendReq

class Trends:
    
    # def __init__(self, language_processor_instance, keyword):
    def __init__(self, keyword):    
        self.pytrends = TrendReq(hl='en-US', 
                                 tz=360, 
                                 timeout=(10,25), 
                                #  proxies=['https://34.203.233.13:80',], 
                                 retries=2, 
                                 backoff_factor=0.1, 
                                 requests_args={'verify':False})

        self.keyword = keyword
        # self.keyword_dictionary = self.build_keyword_payload_dictionary()
        # self.keyword_related_dictionary = self.get_keyword_related_keywords()
        # self.keyword_rising_dictionary = self.get_keyword_rising_keywords()

        # self.payload_interest = self.build_interest_payload()
        # self.interest_dictionary = self.get_interest_trends()


    def build_keyword_payload_dictionary(self):
        try:
            self.pytrends.build_payload([self.keyword], cat=0, timeframe='today 5-y', geo='US')
            payload = self.pytrends.related_queries()
            keyword_dictionary = payload.get(self.keyword)
            return keyword_dictionary
        except Exception as e:
            print(e)
            return None
        

    def get_keyword_related_keywords(self):
        top_related_dict = {}
        top_related = self.keyword_dictionary['top']  # DataFrame of top related queries
        top_related_dict[self.keyword] = top_related.to_dict(orient='records')
        return top_related_dict


    def get_keyword_rising_keywords(self):
        top_rising_dict = {}
        top_rising = self.keyword_dictionary['rising']  # DataFrame of top related queries
        top_rising_dict[self.keyword] = top_rising.to_dict(orient='records')
        return top_rising_dict


    def build_related_keywords_payload(self):
        try:
            self.pytrends.build_payload(self.keyword_related_list)
            return self.pytrends.related_queries()
        except:
            return None
        
    
    # def get_related_keywords_related_keywords(self):
    #     top_related_dict = {}

    #     # case when using Engine's keyword because no related keywords yet
    #     if self.keyword_related_list[:3] is None: 
    #         # for keyword in self.keyword_list:
    #         top_related = self.payload_related.get(self.keyword)['top']  # DataFrame of top related queries
    #         top_related_dict[self.keyword] = top_related.to_dict(orient='records')
    #         return top_related_dict
    #     # case when related keywords already collected so loop through top ones
    #     else:
    #         for keyword in self.keyword_related_list:
    #             top_related = self.payload_related.get(keyword)['top']  # DataFrame of top related queries
    #             top_related_dict[keyword] = top_related.to_dict(orient='records')
    #             return top_related_dict
    

    def build_interest_payload(self):
        try:
            self.pytrends.build_payload([self.keyword], cat=0, timeframe='today 5-y', geo='US')
            return self.pytrends.interest_over_time()
        except Exception as e:
            print(e)
            return None


    def get_interest_trends(self):
        payload_interest = self.build_interest_payload()
        df = payload_interest.drop(
            payload_interest[payload_interest['isPartial'] == True].index)
        # df = df[self.keyword]
        return df.to_json(orient='index', date_format='iso')