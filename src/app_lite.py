from flask import Flask, Blueprint, request, jsonify, session
import os
import base64
from flask_cors import CORS

from classes.EngineSearchDictionary import Engine, SearchDictionary
from utils.formatting import format_search_dictionary

app = Flask(__name__)
CORS(app)

app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8') # Set a secret key for the session
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v0.1') # Define the base URL for the API version

current_script_directory = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path to the directory of the current script

os.chdir(current_script_directory) # Change the working directory to the directory of the current script


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


@api_v1_bp.route('/search', methods=['GET'], endpoint='search_endpoint')
def get_search_results():
    i_search = session['i_search']

    if i_search is not None:
        results = format_search_dictionary(i_search['dictionary'], keep_none_values=False)
        return jsonify({f"{session['q']}": results})
    else:
        return jsonify({"error": "Produkt not initiated. First run /set_produkt/<product id>."})


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


# Register the blueprint with the Flask app
app.register_blueprint(api_v1_bp)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)