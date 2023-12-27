# gtrends scrape alternative: https://stackoverflow.com/questions/56340866/access-google-trends-data-without-a-wrapper-or-with-the-api-python
from pytrends.request import TrendReq
import random


def get_random_proxies(num_proxies=5):
    """
    Randomly selects a specified number of proxies from the given list.
    """
    with open('utils/proxies.txt', 'r') as file:
        # proxies_from_file = [line.strip() for line in file]
        proxies_from_file = [f'https://{line.strip()}' for line in file]

    if len(proxies_from_file) < num_proxies:
        raise ValueError("Not enough proxies in the list.")

    return random.sample(proxies_from_file, num_proxies)

random_proxies = get_random_proxies()


class Trends:
    
    # def __init__(self, language_processor_instance, keyword):
    def __init__(self, keyword):    
        self.pytrends = TrendReq(hl='en-US', 
                                 tz=360, 
                                 timeout=(15,25), 
                                 proxies=random_proxies, 
                                 retries=3, 
                                 backoff_factor=0.3, 
                                 requests_args={'verify':False})

        self.keyword = keyword
        self.keyword_dictionary = self.build_keyword_payload_dictionary()
        # self.keyword_related_dictionary = self.get_keyword_related_keywords()
        # self.keyword_rising_dictionary = self.get_keyword_rising_keywords()

        self.payload_interest = self.build_interest_payload()
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
        

    def get_keyword_related_keywords(self):
        top_related_dict = {}
        top_related = self.keyword_dictionary['top']  # DataFrame of top related queries
        top_related_dict = top_related.to_dict(orient='records')
        return top_related_dict


    def get_keyword_rising_keywords(self):
        top_rising_dict = {}
        top_rising = self.keyword_dictionary['rising']  # DataFrame of top related queries
        top_rising_dict = top_rising.to_dict(orient='records')
        return top_rising_dict
    

    def build_interest_payload(self):
        try:
            self.pytrends.build_payload([self.keyword], cat=0, timeframe='today 5-y', geo='US')
            return self.pytrends.interest_over_time()
        except Exception as e:
            print(e)
            return None


    def get_interest_trends(self):
        df = self.payload_interest.drop(
            self.payload_interest[self.payload_interest['isPartial'] == True].index)
        # df = df[self.keyword]
        return df.to_json(orient='index', date_format='iso')