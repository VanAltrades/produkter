from flask import Flask, request, jsonify
from cls.EngineSearchDictionary import Engine, SearchDictionary

app = Flask(__name__)

@app.route('/ranks', methods=['GET'])
def ranks():
    # http://127.0.0.1:5000/ranks?product=milwaukee%20m18%20fuel
    product = request.args.get('product')  # Get the 'product_' parameter from the query string
    if not product:
        return jsonify({'error': 'Product parameter is missing'}), 400

    engine_instance = Engine(product)
    rank_instance = SearchDictionary(engine_instance)
    return rank_instance.ranks

if __name__ == '__main__':
    app.run(debug=True)