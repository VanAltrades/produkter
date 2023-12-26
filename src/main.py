import json
from classes.EngineSearchDictionary import Engine, SearchDictionary
from classes.Sites import Sites
from classes.EnginePdfs import PdfEngine, PdfDictionary
from classes.LanguageProcessor import LanguageProcessor
from classes.Suggestions import Suggestions
from classes.Trends import Trends

from utils.formatting import format_search_dictionary
from flask import jsonify

def response_to_json(response):
    json_object = json.dumps(response, indent=2)
    return json_object


keyword = "milwaukee m18 fuel"
# keyword = "anker A3025"
# Engine Ranks
engine_instance = Engine(keyword,sa_credentials_path="dukt_sa.json", cx_path="cs_key.json")
engine_instance = Engine("AMD Ryzen 9 5900X")
engine_instance = Engine("Huy Fong HFSR3G")
engine_instance = Engine("Portal PAT-2416096054")
engine_instance = Engine("UPC 680327998169")
engine_instance = Engine("Okuma PCH-C-741XXXH")
engine_instance = Engine("Zero Degree 38152")
len(engine_instance.results)
engine_instance.results

# Create an instance of Rank and automatically pass the serp_dicts
search_dictionary_instance = SearchDictionary(engine_instance)
search_dictionary_instance.dictionary
    # Format ranks
r = jsonify({f"{engine_instance.q}":search_dictionary_instance.dictionary}) 

s_dict_wo_nones = format_search_dictionary(search_dictionary_instance.dictionary, keep_none_values=False)
# s_dict_wo_nones = s_dict.format(keep_none_values=False)
# s_dict_w_nones = s_dict.format(keep_none_values=True)
search_result = response_to_json(s_dict_wo_nones)
### ^ route response

sites_instance = Sites(search_dictionary_instance)
sites_instance.links
sites_instance.titles
sites_instance.dictionary_schemas
sites_schema_dict_formatted = Formatter(sites_instance.dictionary_schemas)
# sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)
sites_schema_dict_formatted_w_nones = sites_schema_dict_formatted.format(keep_none_values=True)
schema_result = response_to_json(sites_schema_dict_formatted_w_nones)
### ^ route response

sites_instance.dictionary_texts

# LanguageProcess
# items
lp = LanguageProcessor(sites_instance, keyword)
lp.items

# Suggests
suga = Suggestions(lp)
suga.question_queries
questions_result = response_to_json(suga.question_queries)
suga.comparison_queries
comparison_result = response_to_json(suga.comparison_queries)
suga.suggested_queries
suggestion_result = response_to_json(suga.suggested_queries)
### ^ route response

# Trends
trends_instance = Trends(keyword=keyword)
trends_instance.keyword_related_dictionary
related_result = response_to_json(trends_instance.keyword_related_dictionary)
trends_instance.keyword_rising_dictionary
rising_result = response_to_json(trends_instance.keyword_rising_dictionary)
trends_instance.interest_dictionary
interest_result = response_to_json(trends_instance.interest_dictionary)
# PDF Ranks
pdf_instance = PdfEngine("milwaukee m18 fuel")

pdf_search_dictionary_instance = PdfDictionary(pdf_instance)
pdf_dict = pdf_search_dictionary_instance.dictionary
links = Formatter(pdf_dict)
pdf_dict_w_none = pdf_dict.format(keep_none_values=True)
