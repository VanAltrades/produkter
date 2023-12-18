from flask import Flask, request
import json
import os
from cls.EngineSearchDictionary import Engine, SearchDictionary
from cls.Sites import Sites
# from cls.EnginePdfs import PdfEngine, PdfDictionary
# from cls.LanguageProcessor import LanguageProcessor
# from cls.Suggestions import Suggestions
# from cls.Trends import Trends
from cls.Formatter import Formatter

# TODO: understand cacheing and how to store engine for same product keywords, 
# while allowing new product keywords entered by client to refresh

app = Flask(__name__)

# Get the absolute path to the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the directory of the current script
os.chdir(current_script_directory)

class Produkter:
    engine_instance = None

    def __init__(self):
        pass

    def get_engine_instance(self, product):
        if Produkter.engine_instance is None:
            Produkter.engine_instance = Engine(product,sa_credentials_path="dukt_sa.json", cx_path="cs_key.json")
        return Produkter.engine_instance

# Create an instance of Produkter
my_routes_instance = Produkter()
        

@app.route('/results', methods=['GET'], endpoint='results_endpoint')
def results():
    keyword = request.args.get('product')
    engine_instance = my_routes_instance.get_engine_instance(keyword)

    search_dictionary_instance = SearchDictionary(engine_instance)

    s_dict = Formatter(search_dictionary_instance.dictionary)

    s_dict_wo_nones = s_dict.format(keep_none_values=False)

    return s_dict_wo_nones

@app.route('/schemas', methods=['GET'], endpoint='schemas_endpoint')
def schemas():
    keyword = request.args.get('product')
    engine_instance = my_routes_instance.get_engine_instance(keyword)

    search_dictionary_instance = SearchDictionary(engine_instance)

    sites_instance = Sites(search_dictionary_instance)

    sites_schema_dict_formatted = Formatter(sites_instance.dictionary_schemas)

    sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)

    return sites_schema_dict_formatted_wo_nones


# # Use the instance methods as routes
# app.add_url_rule('/results', view_func=my_routes_instance.results)
# app.add_url_rule('/schemas', view_func=my_routes_instance.schemas)

if __name__ == '__main__':
    app.run(debug=True)



    # @app.route('/questions', methods=['GET'])
    # def questions(self):
    #     keyword = request.args.get('product')
    #     return 'Contact Page'


    # @app.route('/comparisions', methods=['GET'])
    # def comparisions(self):
    #     keyword = request.args.get('product')
    #     return 'Contact Page'


    # @app.route('/suggestions', methods=['GET'])
    # def suggestions(self):
    #     keyword = request.args.get('product')
    #     return 'Contact Page'
    
    # @app.route('/related', methods=['GET'])
    # def related(self):
    #     keyword = request.args.get('product')
    #     return 'Contact Page'

    # @app.route('/rising', methods=['GET'])
    # def contact(self):
    #     rising = request.args.get('product')
    #     return 'Contact Page'
    
    # @app.route('/assets', methods=['GET'])
    # def assets(self):
    #     keyword = request.args.get('product')
    #     return 'Contact Page'