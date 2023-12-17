# gtrends scrape alternative: https://stackoverflow.com/questions/56340866/access-google-trends-data-without-a-wrapper-or-with-the-api-python
from pytrends.request import TrendReq

class Trends:
    
    # def __init__(self, language_processor_instance, keyword):
    def __init__(self, keyword):    
        self.pytrends = TrendReq(hl='en-US')

        self.keyword = keyword
        self.payload_related = self.build_keyword_payload()
        #1. get related keywords to the engine's `keyword`
        # self.related = self.get_keyword_related_keywords()      
        
        # 2. instantiate top 2 other keywords if they exists  

        # self.keyword_related_list = None
        # if not isinstance(self.keyword_related_list, list):
        #     raise TypeError("The 'keyword_related_list' from `get_related_keywords` must be a list.")

        # self.payload_interest = self.build_interest_payload()
        # # TODO: may delete since prioritizing trends' related keywords instead of nlp items
        # self.keyword_items_list_ = [item for item in language_processor_instance.items if isinstance(item, str) and len(item) < 100]
        # if not isinstance(self.keyword_list, list):
        #     raise TypeError("The 'keyword_list' must be a list.")


        # 3. 
        # self.weekly = self.get_interest_trends()
        # self.rising = self.get_rising_keywords()


    def build_keyword_payload(self):
        try:
            self.pytrends.build_payload(self.keyword)
            return self.pytrends.related_queries()
        except Exception as e:
            print(e)
            return None
        

    def get_keyword_related_keywords(self):
        top_related_dict = {}
        top_related = self.payload_related.get(self.keyword)['top']  # DataFrame of top related queries
        top_related_dict[self.keyword] = top_related.to_dict(orient='records')
        return top_related_dict


    def build_related_keywords_payload(self):
        try:
            self.pytrends.build_payload(self.keyword_related_list)
            return self.pytrends.related_queries()
        except:
            return None
        
    
    def get_related_keywords_related_keywords(self):
        top_related_dict = {}

        # case when using Engine's keyword because no related keywords yet
        if self.keyword_related_list[:3] is None: 
            # for keyword in self.keyword_list:
            top_related = self.payload_related.get(self.keyword)['top']  # DataFrame of top related queries
            top_related_dict[self.keyword] = top_related.to_dict(orient='records')
            return top_related_dict
        # case when related keywords already collected so loop through top ones
        else:
            for keyword in self.keyword_related_list:
                top_related = self.payload_related.get(keyword)['top']  # DataFrame of top related queries
                top_related_dict[keyword] = top_related.to_dict(orient='records')
                return top_related_dict
    

    def build_interest_payload(self):
        try:
            self.pytrends.build_payload(self.keyword_list, cat=0, timeframe='today 5-y', geo='US')
            return self.pytrends.interest_over_time()
        except Exception as e:
            print(e)
            return None


    def get_interest_trends(self):
        df = self.payload_interest.drop(
            self.payload_interest[self.payload_interest['isPartial'] == True].index)
        df = df[self.keyword_list]
        return df.to_json(orient='index', date_format='iso')
    

    def get_rising_keywords(self):
        rising_related_dict = {}
        for keyword in self.keyword_list:
            rising_related = self.payload_related.get(keyword)['rising']  # DataFrame of rising related queries
            rising_related_dict[keyword] = rising_related.to_dict(orient='records')
        return rising_related_dict