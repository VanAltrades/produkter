from pytrends.request import TrendReq

class Trends:
    
    def __init__(self, keyword_list : list):    
        if not isinstance(keyword_list, list):
            raise TypeError("The 'keyword_list' argument must be a list.")
        
        self.keyword_list = keyword_list

        self.pytrends = TrendReq(hl='en-US')
        self.payload_interest = self.build_interest_payload()
        self.payload_related = self.build_related_payload()
        
        self.weekly = self.get_interest_trends()
        self.related = self.get_related_keywords()
        self.rising = self.get_rising_keywords()


    def build_interest_payload(self):
        try:
            self.pytrends.build_payload(self.keyword_list, cat=0, timeframe='today 5-y', geo='US')
            return self.pytrends.interest_over_time()
        except:
            return None


    def get_interest_trends(self):
        df = self.payload_interest.drop(
            self.payload_interest[self.payload_interest['isPartial'] == True].index)
        df = df[self.keyword_list]
        return df.to_json(orient='index', date_format='iso')
    

    def build_related_payload(self):
        try:
            self.pytrends.build_payload(self.keyword_list)
            return self.pytrends.related_queries()
        except:
            return None
        
    
    def get_related_keywords(self):
        top_related_dict = {}
        for keyword in self.keyword_list:
            top_related = self.payload_related.get(keyword)['top']  # DataFrame of top related queries
            top_related_dict[keyword] = top_related.to_dict(orient='records')
        return top_related_dict
    

    def get_rising_keywords(self):
        rising_related_dict = {}
        for keyword in self.keyword_list:
            rising_related = self.payload_related.get(keyword)['rising']  # DataFrame of rising related queries
            rising_related_dict[keyword] = rising_related.to_dict(orient='records')
        return rising_related_dict