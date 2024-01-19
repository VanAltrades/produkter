# PRODUKTER

## Overview

Produkter API allows developers to access product information in a structured JSON format.

Examples include:

1. `/search`

* Return the most relevant titles, descriptions, images, and more from search results.

2. `/resources`

* Return the most relevant PDF resources associated with a product.

3. `/schemas`

* Return product schema (if it exists) ranging from price to gtins to reviews associated with a product. 

4. `/texts`

* Return text from relevant websites featuring a given product.

5. `/suggestions`

* Return relevant user search queries associated with a product.

6. `/questions`

* Return relevant question queries users ask about a product.

7. `/comparisons`

* Return comparison queries that users are looking for when comparing a product to another.

8. `/interest`

* TODO: Return weekly interest (search demand) for a given product.

9. `/related`

* TODO: Return related queries to a given product.

10. `/rising`

* TODO: Return queries associated with a given product that are rising in popularity.

## Build Steps (Docker)

[BUILD.md](docs\BUILD.md)

## Deployment Steps (Cloud Run)

[DEPLOY.md](docs\DEPLOY.md)

## Apigee Configuration

[APIGEE_CONFIG.md](docs\APIGEE_CONFIG.MD)

## Apigee Drupal Developer Portal Setup

[PORTAL.md](docs\PORTAL.md)

## Prioritized Improvement List

#### 1. Implement redis caching

* [Implementation](https://levelup.gitconnected.com/implement-api-caching-with-redis-flask-and-docker-step-by-step-9139636cef24)

* [Deployment](https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-cloud-run#python)

This step will require a redis instance and should allow for running, *for example:* i_sites, i_suggestions, i_trends once and then calling back the instance for each subroute. Each cached instance json should have a unique `q` identifier as a key [ex](https://www.youtube.com/watch?v=_8lJ5lp8P0U). This should work until a new `q` is requested. 

#### 2. Explore JSON Extraction via CSE structured 

[Structured Search](https://developers.google.com/custom-search/docs/structured_search)

[JSON API Using REST](https://developers.google.com/custom-search/v1/using_rest) mentions:

Search engine metadata

The context property has metadata describing the search engine that performed the search query. It includes the name of the search engine, and any [facet objects](https://developers.google.com/custom-search/docs/refinements#create) it provides for refining a search.

from this doc page




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


