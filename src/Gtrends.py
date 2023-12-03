# from pyusuggest import Ubersuggest not working
from pytrends.request import TrendReq
from pytrends import dailydata # https://pypi.org/project/pytrends/

pytrends = TrendReq(hl='en-US')

@staticmethod
def get_interest_trends_kw(keyword):
    kw=keyword
    # pytrends = TrendReq()
    pytrends.build_payload([kw], cat=0, timeframe='today 5-y', geo='US')
    df = pytrends.interest_over_time()
    df.reset_index(inplace=True)
    return df

def get_interest_keywords_product(self):
    kw=f"{self._brand} {self._mpn}"
    print(kw)
    
    pytrends.build_payload([kw])
    related_queries_dict = pytrends.related_queries()

    top_related = related_queries_dict[kw]['top']  # DataFrame of top related queries
    rising_related = related_queries_dict[kw]['rising']  # DataFrame of rising related queries

    print("Top Related Queries:")
    print(top_related)

    print("\nRising Related Queries:")
    print(rising_related)


def get_kwd_search_volume():
    """
    # TODO: many keyword tools are paid, it would be helpful to lookup search volume for a given product
    paid api options include semrush, ahrefs, moz, pyusuggest
    """
    return

def get_kwd_search_difficulty():
    return