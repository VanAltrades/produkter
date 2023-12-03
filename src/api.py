from flask import Flask, request, jsonify
from SearchEngine import SearchEngine

app = Flask(__name__)

se = SearchEngine()

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Missing keyword parameter'}), 400

    # Perform the search and convert the result to a DataFrame
    search_results_df = se.search(keyword)

    # Convert the DataFrame to JSON and return the response
    return search_results_df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)