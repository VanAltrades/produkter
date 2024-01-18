from flask import Flask, Blueprint, request, jsonify, session, render_template, redirect, url_for
import os
import base64
from flask_cors import CORS

from classes.EngineSearchDictionary import Engine, SearchDictionary
from classes.Suggestions import Suggestions
from utils.formatting import format_search_dictionary

app = Flask(__name__)
CORS(app)

app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8') # Set a secret key for the session
# api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v0.1') # Define the base URL for the API version

current_script_directory = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path to the directory of the current script

os.chdir(current_script_directory) # Change the working directory to the directory of the current script


@app.route('/')
def home():
    # Get the URL path of the deployed app
    deployed_url = request.url_root

    return render_template('home.html', deployed_url=deployed_url)


@app.route('/set_produkt', methods=['GET'], endpoint='set_endpoint')
# @api_v1_bp.route('/set_produkt', methods=['GET'], endpoint='set_endpoint')
def set_produkt():
    deployed_url = request.url_root
    # Get the 'q' parameter from the query string
    q = request.args.get('q')

    i_engine = Engine(q)
    i_search = SearchDictionary(i_engine)
    # i_trends = Trends(q)

    session['q'] = q
    session['i_search'] = i_search.__json__()

    return render_template('set_produkt.html', q=q, deployed_url=deployed_url)


@app.route('/search', methods=['GET'], endpoint='search_endpoint')
# @api_v1_bp.route('/search', methods=['GET'], endpoint='search_endpoint')
def get_search_results():
    i_search = session['i_search']

    if i_search is not None:
        results = format_search_dictionary(i_search['dictionary'], keep_none_values=False)
        return jsonify({f"{session['q']}": results})
    else:
        return jsonify({"error": "Produkt not initiated. First run /set_produkt/<product id>."})


@app.route('/search_results', methods=['GET'], endpoint='search_results_endpoint')
def show_search_results():
    # Get the JSON response from the API endpoint
    json_response = get_search_results().get_json()

    # Render the search_results.html template with the JSON response
    return render_template('search_results.html', json_response=json_response)


@app.route('/resources', methods=['GET'], endpoint='resources_endpoint')
# @api_v1_bp.route('/resources', methods=['GET'], endpoint='resources_endpoint')
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


# @api_v1_bp.route('/resources_results', methods=['GET'], endpoint='resources_results_endpoint')
@app.route('/resources_results', methods=['GET'], endpoint='resources_results_endpoint')
def show_resources_results():
    # Get the JSON response from the API endpoint
    json_response = get_resources_results().get_json()

    # Render the search_results.html template with the JSON response
    return render_template('pdfs_results.html', json_response=json_response)


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


@app.route('/questions', methods=['GET'], endpoint='questions_endpoint')
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


@app.route('/comparisons', methods=['GET'], endpoint='comparisons_endpoint')
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


@app.route('/suggestions', methods=['GET'], endpoint='suggestions_endpoint')
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


# Register the blueprint with the Flask app
# app.register_blueprint(api_v1_bp)

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=port)