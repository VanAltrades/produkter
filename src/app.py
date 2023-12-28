from flask import Flask, Blueprint, request, jsonify, session, render_template
import json
import os
import base64

from classes.EngineSearchDictionary import Engine, SearchDictionary
from classes.Sites import Sites
# from cls.EnginePdfs import PdfEngine, PdfDictionary
# from cls.LanguageProcessor import LanguageProcessor
from classes.Suggestions import Suggestions
from classes.Trends import Trends

from utils.formatting import format_search_dictionary


def response_to_json(response):
    json_object = json.dumps(response, indent=2)
    return json_object

app = Flask(__name__, template_folder='templates')

# Set a secret key for the session
app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')
# Define the base URL for the API version
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v0.1')


# Get the absolute path to the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the directory of the current script
os.chdir(current_script_directory)

#   ____  _____ _____ 
#  / ___|| ____|_   _|
#  \___ \|  _|   | |  
#   ___) | |___  | |  
#  |____/|_____| |_|  
@api_v1_bp.route('/set_produkt', methods=['GET'], endpoint='set_endpoint')
def set_produkt():
    # Get the 'q' parameter from the query string
    q = request.args.get('q')

    i_engine = Engine(q)
    i_search = SearchDictionary(i_engine)
    # i_trends = Trends(q)

    session['q'] = q
    session['i_search'] = i_search.__json__()

    return f'Data set successfully.<br><br>Produkt: {q}'

#   ____  _____    _    ____   ____ _   _ 
#  / ___|| ____|  / \  |  _ \ / ___| | | |
#  \___ \|  _|   / _ \ | |_) | |   | |_| |
#   ___) | |___ / ___ \|  _ <| |___|  _  |
#  |____/|_____/_/   \_\_| \_\\____|_| |_|
@api_v1_bp.route('/search', methods=['GET'], endpoint='search_endpoint')
def get_search_results():
    i_search = session['i_search']

    if i_search is not None:
        results = format_search_dictionary(i_search['dictionary'], keep_none_values=False)
        return jsonify({f"{session['q']}": results})
    else:
        return jsonify({"error": "Produkt not initiated. First run /set_produkt/<product id>."})


@api_v1_bp.route('/search_results', methods=['GET'], endpoint='search_results_endpoint')
def show_search_results():
    # Get the JSON response from the API endpoint
    json_response = get_search_results().get_json()

    # Render the search_results.html template with the JSON response
    return render_template('search_results.html', json_response=json_response)

#   ____ ___ _____ _____ ____  
#  / ___|_ _|_   _| ____/ ___| 
#  \___ \| |  | | |  _| \___ \ 
#   ___) | |  | | | |___ ___) |
#  |____/___| |_| |_____|____/ 
def get_sites_instance():
    '''
    get Sites instance from its existing session __json__() 
    or make a new session instance of Sites
    '''
    # Get i_sites from session with a default value of None
    i_sites = session.get('i_sites', None)
    
    # case where i_sites json already instantiated in session
    if i_sites is not None:
        return i_sites
    # case where i_sites json not instantiated so try adding it to session
    elif i_sites is None:
        i_search = session['i_search']
        i_sites = Sites(i_search)
        try: # try to cache sites json
            session['i_sites'] = i_sites.__json__() 
            return i_sites.__json__()
        except: # no memory so just return json from sites instance and accept long load
            return i_sites.__json__()
    else:
        return "Product not initiated. First run /set_product/<product name>"


@api_v1_bp.route('/schemas', methods=['GET'], endpoint='schema_endpoint')
def get_schema_results():
    i_sites = get_sites_instance()
    
    if isinstance(i_sites, str):
        return jsonify({
            "error":
            i_sites
            })
    elif isinstance(i_sites, dict):
        sites_schema_dict_formatted_wo_nones = format_search_dictionary(i_sites['schemas'], keep_none_values=False)
        return jsonify({
            f"{session.get('q')}":
            sites_schema_dict_formatted_wo_nones
            })
    else:
        return jsonify({"error":"Invalid response from /schemas."})


@api_v1_bp.route('/texts', methods=['GET'], endpoint='text_endpoint')
def get_text_results():
    i_sites = get_sites_instance()
    
    if isinstance(i_sites, str):
        return jsonify({"error":i_sites})
    elif isinstance(i_sites, dict):
        # sites_text_dict_formatted_wo_nones = format_search_dictionary(i_sites['texts'], keep_none_values=False)
        return jsonify({f"{session.get('q')}":i_sites['texts']})
    else:
        return jsonify({"error":"Invalid response from /texts."}) 


#   ____  _   _  ____  ____ _____ ____ _____ ___ ___  _   _ ____  
#  / ___|| | | |/ ___|/ ___| ____/ ___|_   _|_ _/ _ \| \ | / ___| 
#  \___ \| | | | |  _| |  _|  _| \___ \ | |  | | | | |  \| \___ \ 
#   ___) | |_| | |_| | |_| | |___ ___) || |  | | |_| | |\  |___) |
#  |____/ \___/ \____|\____|_____|____/ |_| |___\___/|_| \_|____/
def get_suggestions_instance(q):
    '''
    get Suggestions instance from its existing session __json__() 
    or make a new session instance of Suggestions
    '''
    q = session.get('q', None)
    i_suggestions = session.get('i_suggestions', None)

    # case where i_suggestions json already instantiated in session
    if i_suggestions is not None:
        return i_suggestions
    # case where i_suggestions json not instantiated so try adding it to session
    elif i_suggestions is None:
        i_suggestions = Suggestions(q)
        try: # try to cache sites json
            session['i_suggestions'] = i_suggestions.__json__() 
            return i_suggestions.__json__()
        except: # no memory so just return json from sites instance and accept long load
            return i_suggestions.__json__()

    else:
        return "Product not initiated. First run /set_product/<product id>"


@api_v1_bp.route('/questions', methods=['GET'], endpoint='questions_endpoint')
def get_questions():
    q = session.get('q')
    i_suggestions = get_suggestions_instance(q)

    if isinstance(i_suggestions, str):
        return jsonify({
            "error":
            i_suggestions
            }) 
    elif isinstance(i_suggestions, dict):        
        return jsonify({
            f"{session.get('q')}":
            i_suggestions.get('questions',{})
            }) 
    else:
        return jsonify({"error": "Invalid response from /questions."})


@api_v1_bp.route('/comparisons', methods=['GET'], endpoint='comparisons_endpoint')
def get_comparisons():
    q = session.get('q')
    i_suggestions = get_suggestions_instance(q)

    if isinstance(i_suggestions, str):
        return jsonify({
            "error":
            i_suggestions
            }) 
    elif isinstance(i_suggestions, dict):        
        return jsonify({
            f"{session.get('q')}":
            i_suggestions.get('comparisons',{})
            }) 
    else:
        return jsonify({"error": "Invalid response from /comparisons."})


@api_v1_bp.route('/suggestions', methods=['GET'], endpoint='suggestions_endpoint')
def get_suggestions():
    q = session.get('q')
    i_suggestions = get_suggestions_instance(q)

    if isinstance(i_suggestions, str):
        return jsonify({
            "error":
            i_suggestions
            }) 
    elif isinstance(i_suggestions, dict):        
        return jsonify({
            f"{session.get('q')}":
            i_suggestions.get('suggestions',{})
            }) 
    else:
        return jsonify({"error": "Invalid response from /suggestions."})
 

#   _____ ____  _____ _   _ ____  ____  
#  |_   _|  _ \| ____| \ | |  _ \/ ___| 
#    | | | |_) |  _| |  \| | | | \___ \ 
#    | | |  _ <| |___| |\  | |_| |___) |
#    |_| |_| \_\_____|_| \_|____/|____/ 
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

#   ____  _____ ____   ___  _   _ ____   ____ _____ ____  
#  |  _ \| ____/ ___| / _ \| | | |  _ \ / ___| ____/ ___| 
#  | |_) |  _| \___ \| | | | | | | |_) | |   |  _| \___ \ 
#  |  _ <| |___ ___) | |_| | |_| |  _ <| |___| |___ ___) |
#  |_| \_\_____|____/ \___/ \___/|_| \_\\____|_____|____/ 
@api_v1_bp.route('/resources', methods=['GET'], endpoint='resources_endpoint')
def get_resources_results():
    q = session['q']
    i_engine_pdf = Engine(q, fileType="pdf")
    i_search_pdf = SearchDictionary(i_engine_pdf)


    if i_search_pdf is not None:
        results = format_search_dictionary(i_search_pdf.dictionary, keep_none_values=False)
        results_pdfs = results['link']
        return jsonify({f"{session['q']}": results_pdfs})
    else:
        return jsonify({"error": "Produkt not initiated. First run /set_produkt/<product id>."})

@api_v1_bp.route('/resources_results', methods=['GET'], endpoint='resources_results_endpoint')
def show_resources_results():
    # Get the JSON response from the API endpoint
    json_response = get_resources_results().get_json()

    # Render the search_results.html template with the JSON response
    return render_template('pdfs_results.html', json_response=json_response)


# Register the blueprint with the Flask app
app.register_blueprint(api_v1_bp)

if __name__ == '__main__':
    app.run(debug=True)