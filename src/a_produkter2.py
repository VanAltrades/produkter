from flask import Flask, request, Blueprint, jsonify, session
import json
import os
import base64
from cls.EngineSearchDictionary import Engine, SearchDictionary
from cls.Sites import Sites
# from cls.EnginePdfs import PdfEngine, PdfDictionary
# from cls.LanguageProcessor import LanguageProcessor
from cls.Suggestions import Suggestions
from cls.Trends import Trends
from cls.Formatter import Formatter


def response_to_json(response):
    json_object = json.dumps(response, indent=2)
    return json_object

app = Flask(__name__)
# Set a secret key for the session
app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')
# Define the base URL for the API version
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v0.1')


# Get the absolute path to the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the directory of the current script
os.chdir(current_script_directory)


@api_v1_bp.route('/set_produkt/<q>', endpoint='set_endpoint')
def set_produkt(q):
    i_engine = Engine(
        q,
        sa_credentials_path="dukt_sa.json",
        cx_path="cs_key.json"
        )
    i_search = SearchDictionary(i_engine)
    # i_trends = Trends(q)

    session['q'] = q
    session['i_search'] = i_search.__json__()

    return f'Data set successfully.<br><br>Produkt: {q}'

@api_v1_bp.route('/search', methods=['GET'], endpoint='search_endpoint')
def get_search_results():
    i_search = session.get('i_search')

    if i_search is not None:
        s_dict = Formatter(i_search["dictionary"])
        s_dict_wo_nones = s_dict.format(keep_none_values=False)
        return s_dict_wo_nones
    else:
        return "Produkt not initiated. First run /set_produkt/<product name>"


# TODO: refactor /schemas and /texts with this function (like get_suggestion_instance)
def get_sites_instance(q):
    '''
    get Sites instance from its existing session __json__() 
    or make a new session instance of Sites
    '''
    try:
        i_sites = session.get('i_sites')
    except:
        i_sites = None
    
    if i_sites == None:
        i_search = session.get('i_search')
        i_sites = Sites(i_search)
        session['i_sites'] = i_sites.__json__() # cache sites json
    else:
        return "Product not initiated. First run /set_product/<product name>"


@api_v1_bp.route('/schemas', methods=['GET'], endpoint='schema_endpoint')
def get_schema_results():
    
    try:
        i_sites = session.get('i_sites')
    except:
        i_sites = None
    
    if i_sites == None:
        i_search = session.get('i_search')
        i_sites = Sites(i_search)
        session['i_sites'] = i_sites.__json__()

        sites_schema_dict_formatted = Formatter(i_sites.dictionary_schemas)
        sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)
        return sites_schema_dict_formatted_wo_nones
    else:   # i_sites already exists from /texts
        sites_schema_dict_formatted = Formatter(i_sites.dictionary_schemas)
        sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)
        return sites_schema_dict_formatted_wo_nones


@api_v1_bp.route('/texts', methods=['GET'], endpoint='text_endpoint')
def get_text_results():
    
    try:
        i_sites = session.get('i_sites')
    except:
        i_sites = None
    
    if i_sites == None:
        i_search = session.get('i_search')
        i_sites = Sites(i_search)
        session['i_sites'] = i_sites.__json__()

        sites_texts_dict_formatted = Formatter(i_sites.dictionary_texts)
        sites_texts_dict_formatted_wo_nones = sites_texts_dict_formatted.format(keep_none_values=False)
        return sites_texts_dict_formatted_wo_nones
    else:   # i_sites already exists from /schemas
        sites_texts_dict_formatted = Formatter(i_sites.dictionary_texts)
        sites_texts_dict_formatted_wo_nones = sites_texts_dict_formatted.format(keep_none_values=False)
        return sites_texts_dict_formatted_wo_nones


def get_suggestions_instance(q):
    '''
    get Suggestions instance from its existing session __json__() 
    or make a new session instance of Suggestions
    '''
    i_suggestions = session.get('i_suggestions')

    if i_suggestions is not None:
        return i_suggestions

    if q is not None:
        i_suggestions = Suggestions(q)
        
        # UserWarning: The 'session' cookie is too large: the value was 7123 bytes but the header required 26 extra bytes. The final size was 7149 bytes but the limit is 4093 bytes. 
        # TODO: implement db to store all __json__()
        # session['i_suggestions'] = i_suggestions.__json__()
        
        return i_suggestions
    else:
        return "Product not initiated. First run /set_product/<product name>"


@api_v1_bp.route('/questions', methods=['GET'], endpoint='questions_endpoint')
def get_questions():
    q = session.get('q')
    i_suggestions = get_suggestions_instance(q)
    # return i_suggestions.__json__().get('questions',{})    

    if isinstance(i_suggestions.__json__(), dict):
        return i_suggestions.__json__().get('questions',{}) 
    elif isinstance(i_suggestions, str):
        # print info about instantiating produkt. from get_suggestions_instance(q) else
        return jsonify({"error":i_suggestions})  
    
    else:
        return jsonify({"error": "Invalid response from get_suggestions_instance."})


@api_v1_bp.route('/comparisons', methods=['GET'], endpoint='comparisons_endpoint')
def get_comparisons():
    q = session.get('q')
    i_suggestions = get_suggestions_instance(q)
    # return i_suggestions.__json__().get('comparisons',{})    

    if isinstance(i_suggestions.__json__(), dict):
        return i_suggestions.__json__().get('comparisons',{}) 
    elif isinstance(i_suggestions, str):
        # print info about instantiating produkt. from get_suggestions_instance(q) else
        return jsonify({"error":i_suggestions})  
    
    else:
        return jsonify({"error": "Invalid response from get_suggestions_instance."})
    

@api_v1_bp.route('/suggestions', methods=['GET'], endpoint='suggestions_endpoint')
def get_suggestions():
    q = session.get('q')
    i_suggestions = get_suggestions_instance(q)
    # return i_suggestions.__json__().get('suggestions',{})    

    if isinstance(i_suggestions.__json__(), dict):
        return i_suggestions.__json__().get('suggestions',{}) 
    elif isinstance(i_suggestions, str):
        # print info about instantiating produkt. from get_suggestions_instance(q) else
        return jsonify({"error":i_suggestions})  
    
    else:
        return jsonify({"error": "Invalid response from get_suggestions_instance."})
    

@api_v1_bp.route('/interest', methods=['GET'], endpoint='interest_endpoint')
def get_interest_results():
    q = session.get('q')

    i_trends = Trends(keyword=q)
    i_trends.build_interest_payload()
    interest_dictionary = i_trends.get_interest_trends()
    interest_result = response_to_json(interest_dictionary)
    return interest_result


@api_v1_bp.route('/related', methods=['GET'], endpoint='related_endpoint')
def get_related_results():
    # TODO: call keyword_related_rising_dictionary or call if exists
    q = session.get('q')

    i_trends = Trends(keyword=q)
    interest_dictionary = i_trends.get_keyword_related_keywords()
    interest_result = response_to_json(interest_dictionary)
    return interest_result


# Register the blueprint with the Flask app
app.register_blueprint(api_v1_bp)

if __name__ == '__main__':
    app.run(debug=True)