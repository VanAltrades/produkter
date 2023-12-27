# PRODUKTER

## Prioritized Improvement List

#### 1. Change routes to maintain set_produkt/q/... structure:

```
@api_v1_bp.route('/set_produkt/<q>', endpoint='set_endpoint')

@api_v1_bp.route('/set_produkt/<q>/search', methods=['GET'], endpoint='search_endpoint') 

...
```

* Make sure this works for all sub routes and allows for a reset when new q is added.

#### 2. Add in template routes to visualize responses in demos:

```
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='src/templates')

@app.route('/search')
def search():
    # Replace this with your actual API logic
    json_response = {"key": "value", "another_key": "another_value"}
    return jsonify(json_response)

@app.route('/search_results')
def search_results():
    # Get the JSON response from the API endpoint
    json_response = search().get_json()

    # Render the search_results.html template with the JSON response
    return render_template('search_results.html', json_response=json_response)

if __name__ == '__main__':
    app.run(debug=True)
```

#### 3. Explore ?q options instead of session route

In the future I will want to cache results and this session route will lose it's importance. The responses are already larger than the cookies cache so each result is processing an api even if it was already run.

#### 4. Implement redis caching

* [Implementation](https://levelup.gitconnected.com/implement-api-caching-with-redis-flask-and-docker-step-by-step-9139636cef24)

* [Deployment](https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-cloud-run#python)

This step will require a redis instance and should allow for running, *for example:* i_sites, i_suggestions, i_trends once and then calling back the instance for each subroute. Each cached instance json should have a unique `q` identifier as a key [ex](https://www.youtube.com/watch?v=_8lJ5lp8P0U). This should work until a new `q` is requested. 

#### 5. Containerize the Application

Before attempting to deploy the app to Cloud Run, I will have to containerize the app using docker.

* Dockerfile review and update

* .env file review and update 

* config.app_secrets.py to os environment variables via .env file

* config.config BaseConfig class inclusion in app.py

## SearchEngine


**Authenticate Google's Custom Search API links**

[Programable Search Engine Setup](https://programmablesearchengine.google.com/controlpanel/all)

[Custom Search Engine API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com)


**Google Search Spam Policies**

[Google's Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies)


**Base URL:**

`base_url = https://www.googleapis.com/customsearch/v1`

`q_confidence_modifier = f"allintext: {brand} {mpn}"`

<details>
<summary>
Parameters:
</summary>

* q={searchTerms}: The main search query. It represents the terms that you want to search for.

* cx={cx?}: The custom search engine (CSE) ID to use for the search.

* fileType={fileType?}: Restricts results to files of a specific type.

* num={count?}: Number of search results to return per page.

* start={startIndex?}: The index of the first result to return.

* lr={language?}: The language restriction for the search results.

* safe={safe?}: SafeSearch level for filtering explicit content.

* sort={sort?}: The sorting order of the results.

* filter={filter?}: Controls turning on or off the duplicate content filter.

* gl={gl?}: The country to use for geolocation of the search results.

* cr={cr?}: The country to restrict the search to.

* googlehost={googleHost?}: The Google domain to use for the search.

* c2coff={disableCnTwTranslation?}: Disables the automatic translation between Chinese and Traditional Chinese.

* hq={hq?}: Additional query terms to be appended to the user's query.

* hl={hl?}: The interface language.

* siteSearch={siteSearch?}: Restricts results to URLs from a specific site.

* siteSearchFilter={siteSearchFilter?}: Controls whether to include or exclude results from the site specified by siteSearch.

* exactTerms={exactTerms?}: Identifies a phrase that all documents in the search results must contain.

* excludeTerms={excludeTerms?}: Identifies a word or phrase that should not appear in any documents in the search results.

* linkSite={linkSite?}: Specifies that all search results should contain a link to a particular URL.

* orTerms={orTerms?}: A list of terms separated by the OR operator.

* relatedSite={relatedSite?}: Specifies that all search results should be pages that are related to a particular URL.

* dateRestrict={dateRestrict?}: Restricts results to a specific date range.

* lowRange={lowRange?} and highRange={highRange?}: Specifies the lower and upper bounds of a date range.

* searchType={searchType}: Specifies the type of search to be performed.

* rights={rights?}: Filters search results based on licensing.

* imgSize={imgSize?}: Restricts results to images of a specified size.

* imgType={imgType?}: Restricts results to images of a specified type.

* imgColorType={imgColorType?}: Restricts results to images of a specified color type.

* imgDominantColor={imgDominantColor?}: Restricts results to images of a specified dominant color.

* alt=json: Specifies the response format as JSON.

* These parameters provide a way to customize and refine your search to get more relevant results based on your specific requirements.
</details>


