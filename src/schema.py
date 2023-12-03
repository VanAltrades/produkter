import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

ua = UserAgent()

def get_schema(url):
    headers = {'User-Agent': ua.random}
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract schema
        schema = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
        # product_name = schema['name']
        # product_price = schema['offers']['price']
        # product_url = "https:" + schema['image']
        return schema
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
        return None


def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Example usage
url = 'https://www.homedepot.com/p/Husky-3-8-in-Drive-Master-Bit-Socket-Set-37-Piece-H3DBS37PC/204759235'
output_file = 'attributes.json'

schema = get_schema(url)
if schema:
    print(json.dumps(schema, indent=2))
    # save_to_json(schema, output_file)
    # print(f"schema extracted and saved to {output_file}")