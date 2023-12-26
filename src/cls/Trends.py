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

    
    def __json__(self):
        return {
            'keyword': self.keyword,
            'pytrends_params': {
                'hl': self.pytrends.hl,
                'tz': self.pytrends.tz,
                'timeout': self.pytrends.timeout,
                'retries': self.pytrends.retries,
                'backoff_factor': self.pytrends.backoff_factor,
                'requests_args': {'verify': self.pytrends.requests_args.get('verify', True)}
            }
        }


    def build_keyword_payload_dictionary(self):
        try:
            self.pytrends.build_payload([self.keyword], cat=0, timeframe='today 5-y', geo='US')
            payload = self.pytrends.related_queries()
            self.keyword_dictionary = payload.get(self.keyword)
            return self.keyword_dictionary
        except Exception as e:
            print(e)
            return None
        

    def get_keyword_related_keywords(self, keyword_dictionary):
        top_related_dict = {}
        keyword_dictionary = self.build_keyword_payload_dictionary()
        top_related = keyword_dictionary['top']  # DataFrame of top related queries
        top_related_dict[self.keyword] = top_related.to_dict(orient='records')
        return top_related_dict


    def get_keyword_rising_keywords(self):
        top_rising_dict = {}
        keyword_dictionary = self.build_keyword_payload_dictionary()
        top_rising = keyword_dictionary['rising']  # DataFrame of top related queries
        top_rising_dict[self.keyword] = top_rising.to_dict(orient='records')
        return top_rising_dict


    def build_related_keywords_payload(self):
        try:
            self.pytrends.build_payload(self.keyword_related_list)
            return self.pytrends.related_queries()
        except:
            return None
    

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