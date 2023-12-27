# how I got a list of proxies
import re
import requests

url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt'
response = requests.get(url)

response_text = response.text
# Define a regular expression pattern for matching proxy strings in the format "IP:Port"
proxy_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b')

# Find all matches in the response text
proxies = proxy_pattern.findall(response_text)

# print(proxies)
with open('proxies.txt', 'w') as file:
    for proxy in proxies:
        file.write(proxy + '\n')