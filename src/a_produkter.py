from flask import Flask, request, Blueprint, g, session
import json
import os
import base64
from cls.EngineSearchDictionary import Engine, SearchDictionary
from cls.Sites import Sites
# from cls.EnginePdfs import PdfEngine, PdfDictionary
# from cls.LanguageProcessor import LanguageProcessor
# from cls.Suggestions import Suggestions
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




class Produkter:
    engine = None

    def __init__(self, q):
        self.sa_credentials_path="dukt_sa.json" 
        self.cx_path="cs_key.json"
        self.q = q
        self.engine = self.get_engine_instance()


    def to_dict(self):
        return {'q':self.q, 'engine': self.engine}
    

    def get_engine_instance(self):
        if Produkter.engine is None:
            Produkter.engine = Engine(self.q, self.sa_credentials_path, self.cx_path)
        return Produkter.engine


# Middleware to initialize the global object for each request
# @api_v1_bp.before_request
# def before_request():
#     engine_instance = None  # Initialize to None for the first request
#     search_instance = None  # Initialize search_instance
#     sites_instance = None # Initialize sites_instance

# Create an instance of Produkter
# my_routes_instance = Produkter()
# def serialize_produkt(obj):
#     if isinstance(obj, Produkter):
#         return {'attributes': vars(obj)}
#     raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# def deserialize_produkt(obj, attr):
#     if attr in obj:
#         return Produkter(obj[attr])
#     return obj
    
def to_dict(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} has no __dict__ attribute")


def serialize_class(obj):
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        return {'__class__': obj.__class__.__name__, 'data': obj.to_dict()}
    raise TypeError(f"Object of type {type(obj)} is not serializable")


def deserialize_class(obj):
    if 'to_dict' in obj:
        return obj['to_dict']()
    else:
        return f"to_dict not in {obj}"


@api_v1_bp.route('/search', methods=['GET'], endpoint='search_endpoint')
def get_search_results():
    q = request.args.get('q')
    engine_instance = Produkter(q)

    # Create or retrieve the search_instance
    if engine_instance:
        search_instance = SearchDictionary(engine_instance.engine)
    else:
        search_instance = None
        sites_instance = None
        
    s_dict = Formatter(search_instance.dictionary)
    s_dict_wo_nones = s_dict.format(keep_none_values=False)

    # Store Serialize engine_instance to JSON in the session for future requests
    # session['engine_instance'] = json.dumps(engine_instance, default=serialize_class)
    # Store Serialize searcg_instance to JSON in the session for future requests
    # session['search_instance'] = json.dumps(search_instance, default=serialize_class)
    session['q'] = q
    session['search_dictionary'] = search_instance.dictionary

    return s_dict_wo_nones


@api_v1_bp.route('/schemas', methods=['GET'], endpoint='schema_endpoint')
def get_schema_results():
    if sites_instance:
        # if sites_instance already exists from /texts
        # Retrieve the sites_instance
        sites_schema_dict_formatted = Formatter(sites_instance.dictionary_schemas)
        sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)
        return sites_schema_dict_formatted_wo_nones

    elif engine_instance and search_instance:
        # if sites_instance does not exist
        # Create the sites_instance
        sites_instance = Sites(search_instance)

        sites_schema_dict_formatted = Formatter(sites_instance.dictionary_schemas)
        sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)
        return sites_schema_dict_formatted_wo_nones

    else:
        return 'No valid q or search_instance found for /schemas'
    

@api_v1_bp.route('/texts', methods=['GET'], endpoint='texts_endpoint')
def get_texts_results():
    # Retrieve globals from the session
    engine_instance = session.get('engine_instance')

    if sites_instance:
        # if sites_instance already exists from /schemas
        # Retrieve the sites_instance
        sites_texts_dict_formatted = Formatter(sites_instance.dictionary_texts)
        sites_texts_dict_formatted_wo_nones = sites_texts_dict_formatted.format(keep_none_values=False)
        return sites_texts_dict_formatted_wo_nones

    elif engine_instance and search_instance:
        # if sites_instance does not exist
        # Create the sites_instance
        sites_instance = Sites(search_instance)

        sites_texts_dict_formatted = Formatter(sites_instance.dictionary_texts)
        sites_texts_dict_formatted_wo_nones = sites_texts_dict_formatted.format(keep_none_values=False)
        return sites_texts_dict_formatted_wo_nones

    else:
        return 'No valid q or search_instance found for /texts'
    

@api_v1_bp.route('/interest', methods=['GET'], endpoint='interest_endpoint')
def get_interest_results():
    q = session.get('q')

    trends_instance = Trends(keyword=q)
    trends_instance.build_interest_payload()
    interest_dictionary = trends_instance.get_interest_trends()
    interest_result = response_to_json(interest_dictionary)
    return interest_result


# Register the blueprint with the Flask app
app.register_blueprint(api_v1_bp)

if __name__ == '__main__':
    app.run(debug=True)



    # @app.route('/questions', methods=['GET'])
    # def questions(self):
    #     keyword = request.args.get('q')
    #     return 'Contact Page'


    # @app.route('/comparisions', methods=['GET'])
    # def comparisions(self):
    #     keyword = request.args.get('q')
    #     return 'Contact Page'


    # @app.route('/suggestions', methods=['GET'])
    # def suggestions(self):
    #     keyword = request.args.get('q')
    #     return 'Contact Page'
    
    # @app.route('/related', methods=['GET'])
    # def related(self):
    #     keyword = request.args.get('q')
    #     return 'Contact Page'

    # @app.route('/rising', methods=['GET'])
    # def contact(self):
    #     rising = request.args.get('q')
    #     return 'Contact Page'
    
    # @app.route('/assets', methods=['GET'])
    # def assets(self):
    #     keyword = request.args.get('q')
    #     return 'Contact Page'