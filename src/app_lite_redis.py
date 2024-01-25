from flask import Flask, Blueprint, request, jsonify, session, render_template, redirect, url_for
import os
import base64
from flask_cors import CORS
import redis
import json

from classes.EngineSearchDictionary import Engine, SearchDictionary
from classes.Suggestions import Suggestions
from classes.Sites import Sites
from utils.formatting import format_search_dictionary

app = Flask(__name__)
CORS(app)

redis_host = os.environ.get("REDISHOST", "localhost")
redis_port = int(os.environ.get("REDISPORT", 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
# r = redis.Redis(host='localhost', port=6379, db=0)

app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8') # Set a secret key for the session
# api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v0.1') # Define the base URL for the API version

current_script_directory = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path to the directory of the current script

os.chdir(current_script_directory) # Change the working directory to the directory of the current script

# redis keys defined. need these to identify what to return @ endpoints.
rkey_i_search_results = "i_search_results"
rkey_i_search_links = "i_search_links"
rkey_i_search_pdfs = "i_search_pdfs"
rkey_i_suggestions = "i_suggestions"
rkey_i_sites = "i_sites"
valid_rkeys = [rkey_i_search_results, rkey_i_search_links, rkey_i_search_pdfs, rkey_i_suggestions, rkey_i_sites]

def set_redis_cache_expiry(expiration_time_seconds=30):
    rkeys = redis_client.keys("*")
    # Set expiration for each key
    for key in rkeys:
        redis_client.expire(key, expiration_time_seconds)


def set_q_value_in_cache(q):
    '''
    check if request's `q` value is the same as the `q` value in cache. 
    if so, proceed.
    if not, reset `q` value and delete all previous cached keys/values.
    '''
    cached_q_value = redis_client.get('q')
    print(cached_q_value)
    
    if cached_q_value is None:
        redis_client.set('q',q)
        return    
    
    if q and q == cached_q_value.decode('utf-8'): # reusing `q` in cache
        return
    
    else: # requested `q` is different from `q` in cache
        redis_client.set('q', q)
        for key in valid_rkeys:
            redis_client.delete(key)


def get_rkey_value_from_redis_cache_else_compute(q, rkey):
    '''
    as long as `rkey`'s argument exists within the pre-defined `valid_rkeys`...
    return the cached `rkey` value.
    otherwise compute `rkey` and store it in cache. 
    '''
    if rkey not in valid_rkeys:
        raise ValueError(f"Invalid value for 'rkey'. It must be one of {valid_rkeys}")

    cached_result = redis_client.get(rkey)

    if cached_result:
        return json.loads(cached_result.decode('utf-8'))  # Parse the JSON string to a dictionary

    # Compute the result based on the provided rkey
    if rkey == rkey_i_search_results:
        i_engine = Engine(q)
        i_search = SearchDictionary(i_engine)
        rkey_value = i_search.__json__()['dictionary']  # dict

    elif rkey == rkey_i_search_links:
        i_engine = Engine(q)
        i_search = SearchDictionary(i_engine)
        rkey_value = i_search.__json__()['links']       # list
    
    elif rkey == rkey_i_search_pdfs:
        i_engine_pdf = Engine(q, fileType="pdf")
        i_search_pdf = SearchDictionary(i_engine_pdf)
        rkey_value = i_search_pdf.__json__()['links']   # list
    
    elif rkey == rkey_i_suggestions:
        i_suggestions = Suggestions(q)
        rkey_value = i_suggestions.__json__()           # dict

    elif rkey == rkey_i_sites:
        i_engine = Engine(q)
        i_search = SearchDictionary(i_engine)           # TODO: use i_search_links if exist, else rerun i_search
        i_sites = Sites(i_search)
        rkey_value = i_sites.__json__()                 # dict

    else:
        return None

    # Store the rkey_value as a JSON string in the cache
    redis_client.set(rkey, json.dumps(rkey_value))

    return rkey_value


@app.route('/')
def home():
    return

#   ____  _____    _    ____   ____ _   _ 
#  / ___|| ____|  / \  |  _ \ / ___| | | |
#  \___ \|  _|   / _ \ | |_) | |   | |_| |
#   ___) | |___ / ___ \|  _ <| |___|  _  |
#  |____/|_____/_/   \_\_| \_\\____|_| |_|
@app.route('/search', methods=['GET'], endpoint='search_endpoint')
# @api_v1_bp.route('/search', methods=['GET'], endpoint='search_endpoint')
def get_search_results():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_search_results)

    set_redis_cache_expiry(expiration_time_seconds=30)

    if rkey_value is not None:
        
        results = format_search_dictionary(rkey_value, keep_none_values=False)
        
        return jsonify({f"{q}": results})
    else:
        return jsonify({"error": f"no results for ?q={q}"})

#   ____  _____ ____   ___  _   _ ____   ____ _____ ____  
#  |  _ \| ____/ ___| / _ \| | | |  _ \ / ___| ____/ ___| 
#  | |_) |  _| \___ \| | | | | | | |_) | |   |  _| \___ \ 
#  |  _ <| |___ ___) | |_| | |_| |  _ <| |___| |___ ___) |
#  |_| \_\_____|____/ \___/ \___/|_| \_\\____|_____|____/ 
@app.route('/resources', methods=['GET'], endpoint='resources_endpoint')
# @api_v1_bp.route('/resources', methods=['GET'], endpoint='resources_endpoint')
def get_resources_results():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_search_pdfs)

    set_redis_cache_expiry(expiration_time_seconds=30)

    if rkey_value is not None:
        return jsonify({f"{q}": rkey_value})
    else:
        return jsonify({"error": f"no results for ?q={q}"})

#   ____  _   _  ____  ____ _____ ____ _____ ___ ___  _   _ ____  
#  / ___|| | | |/ ___|/ ___| ____/ ___|_   _|_ _/ _ \| \ | / ___| 
#  \___ \| | | | |  _| |  _|  _| \___ \ | |  | | | | |  \| \___ \ 
#   ___) | |_| | |_| | |_| | |___ ___) || |  | | |_| | |\  |___) |
#  |____/ \___/ \____|\____|_____|____/ |_| |___\___/|_| \_|____/
@app.route('/questions', methods=['GET'], endpoint='questions_endpoint')
def get_questions():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_suggestions)

    set_redis_cache_expiry(expiration_time_seconds=30)

    if rkey_value is not None:
        results = rkey_value.get('questions',{})
        return jsonify({f"{q}": results})
    else:
        return jsonify({"error": f"no results for ?q={q}"})


@app.route('/comparisons', methods=['GET'], endpoint='comparisons_endpoint')
def get_comparisons():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_suggestions)

    set_redis_cache_expiry(expiration_time_seconds=30)

    if rkey_value is not None:
        results = rkey_value.get('comparisons',{})
        return jsonify({f"{q}": results})
    else:
        return jsonify({"error": f"no results for ?q={q}"})


@app.route('/suggestions', methods=['GET'], endpoint='suggestions_endpoint')
def get_suggestions():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_suggestions)

    set_redis_cache_expiry(expiration_time_seconds=30)
    
    if rkey_value is not None:
        results = rkey_value.get('suggestions',{})
        return jsonify({f"{q}": results})
    else:
        return jsonify({"error": f"no results for ?q={q}"})


#   ____ ___ _____ _____ ____  
#  / ___|_ _|_   _| ____/ ___| 
#  \___ \| |  | | |  _| \___ \ 
#   ___) | |  | | | |___ ___) |
#  |____/___| |_| |_____|____/
@app.route('/schemas', methods=['GET'], endpoint='schemas_endpoint')
def get_schemas_results():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_sites)

    set_redis_cache_expiry(expiration_time_seconds=30)
    
    if rkey_value is not None:
        results = format_search_dictionary(rkey_value['schemas'], keep_none_values=False)
        return jsonify({f"{q}": results})
    else:
        return jsonify({"error": f"no results for ?q={q}"})


@app.route('/texts', methods=['GET'], endpoint='texts_endpoint')
def get_texts_results():
    q = request.args.get('q')
    set_q_value_in_cache(q)

    rkey_value = get_rkey_value_from_redis_cache_else_compute(q, rkey_i_sites)

    set_redis_cache_expiry(expiration_time_seconds=30)
    
    if rkey_value is not None:
        results = rkey_value['texts']
        return jsonify({f"{q}": results})
    else:
        return jsonify({"error": f"no results for ?q={q}"})


# Register the blueprint with the Flask app
# app.register_blueprint(api_v1_bp)

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=port)