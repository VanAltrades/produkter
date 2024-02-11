# move to /src directory to run
import json
from classes.EngineSearchDictionary import Engine, SearchDictionary
from classes.Suggestions import Suggestions
from classes.Sites import Sites
from classes.LanguageProcessor import LanguageProcessor
from classes.Trends import Trends

from utils.formatting import format_search_dictionary
from flask import jsonify

def response_to_json(response):
    json_object = json.dumps(response, indent=2)
    return json_object


q = "AMEREX B570 fire extinguisher"     # [fixed] SSL Error from logs
q = "MILLER ELECTRIC 301568 mig cable"  # [fixed] SSL Error from logs
q = "ALLIED TUBE & CONDUIT 6103-24-00 conduit"  # TypeError: 'NoneType' object is not iterable (get_dictionary_dict)
q = "cbdmd GUM-20 rr200 d9 91544"       # NoneType from SearchEngine
q = "DOGIPOT 1402-30 bags"              # hangs infinitely
q = "milwaukee m18 fuel"
q = "AMD Ryzen 9 5900X"
q = "Huy Fong HFSR3G"
q = "Portal PAT-2416096054"
q = "UPC 680327998169"
q = "Okuma PCH-C-741XXXH"
q = "Zero Degree 38152"


# /search?q=garmin forerunner

# search
i_engine = Engine(q)
i_search = SearchDictionary(i_engine).__json__()

if i_search is not None:
    results = format_search_dictionary(i_search['dictionary'], keep_none_values=False)
    print(response_to_json({f"{q}": results}))
else:
    print({"error": "Produkt not initiated. First run /set_produkt/<product id>."})


# resource
i_engine_pdf = Engine(q, fileType="pdf")
i_search_pdf = SearchDictionary(i_engine_pdf).__json__()

if i_search_pdf is not None:
    results = format_search_dictionary(i_search_pdf.dictionary, keep_none_values=False)
    results_pdfs = results['link']
    jsonify({f"{q}": results_pdfs})
else:
    jsonify({"error": "Produkt not initiated. First run /set_produkt/<product id>."})


# suggestions
i_suggestions = Suggestions(q).__json__()


if isinstance(i_suggestions, str):
    jsonify({
        "error":
        i_suggestions
        }) 
elif isinstance(i_suggestions, dict):        
    jsonify({
        f"{q}":
        i_suggestions.get('questions',{})
        }) 
else:
    jsonify({"error": "Invalid response from /questions."})


if isinstance(i_suggestions, str):
    jsonify({
        "error":
        i_suggestions
        }) 
elif isinstance(i_suggestions, dict):        
    jsonify({
        f"{q}":
        i_suggestions.get('comparisons',{})
        }) 
else:
    jsonify({"error": "Invalid response from /comparisons."})


if isinstance(i_suggestions, str):
    jsonify({
        "error":
        i_suggestions
        }) 
elif isinstance(i_suggestions, dict):        
    jsonify({
        f"{q}":
        i_suggestions.get('suggestions',{})
        }) 
else:
    jsonify({"error": "Invalid response from /suggestions."})


# sites
i_engine = Engine(q)
i_search = SearchDictionary(i_engine).__json__()
i_sites = Sites(i_search).__json__()


if isinstance(i_sites, str):
    print(response_to_json({
        "error":
        i_sites
        }))
elif isinstance(i_sites, dict):
    sites_schema_dict_formatted_wo_nones = format_search_dictionary(i_sites['schemas'], keep_none_values=False)
    print(response_to_json({
        f"{q}":
        sites_schema_dict_formatted_wo_nones
        }))
else:
    print(response_to_json({"error":"Invalid response from /schemas."}))


if isinstance(i_sites, str):
    print(response_to_json({"error":i_sites}))
elif isinstance(i_sites, dict):
    # sites_text_dict_formatted_wo_nones = format_search_dictionary(i_sites['texts'], keep_none_values=False)
    print(response_to_json({f"{q}":i_sites['texts']}))
else:
    print(response_to_json({"error":"Invalid response from /texts."})) 


# redis cache
import redis

i_engine = Engine(q)
i_search = SearchDictionary(i_engine)

r = redis.Redis(host='localhost', port=6379, db=0)

r.set("q",q)
r.set("i_search_results",json.dumps(i_search.__json__()['dictionary']))
r.set("i_search_links",json.dumps(i_search.__json__()['links']))

r.get("q")
r.get("i_search_results")
r.get("i_search_links")

# Set an expiration time of 1 hour (3600 seconds) for the key
# r.expire(q_key, 3600)


# session['q'] = q
# session['i_search'] = i_search.__json__()


# LanguageProcess
# items
# lp = LanguageProcessor(i_sites, q)
# lp.items

### ^ route response

# Trends
# trends_instance = Trends(keyword="langer gaming mouse")
# trends_instance.keyword_dictionary


# trends_instance.keyword_related_dictionary
# trends_instance.keyword_rising_dictionary

# trends_instance.payload_interest
# trends_instance.interest_dictionary
# related_result = response_to_json(trends_instance.keyword_related_dictionary)
# trends_instance.keyword_rising_dictionary
# rising_result = response_to_json(trends_instance.keyword_rising_dictionary)
# trends_instance.interest_dictionary
# interest_result = response_to_json(trends_instance.interest_dictionary)