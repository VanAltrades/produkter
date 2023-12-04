# PRODUKTOR

## SearchEngine

**Authenticate Google's Custom Search API:**

`https://programmablesearchengine.google.com/controlpanel/all`

`https://console.cloud.google.com/apis/library/customsearch.googleapis.com`

## TODO: new data structure

class CustomSearchAPI:
    def search(self, keyword):
        # Implementation of custom search API communication
        return product_info_json

class WebScraping:
    def scrape_websites(self, links):
        # Implementation of web scraping to extract additional product information
        return extended_product_info_json

class PDFProcessing:
    def process_pdfs(self, pdf_links, file_type_filter):
        # Implementation of PDF processing to extract information
        return pdf_product_info_json

class NLPProcessing:
    def apply_nlp(self, product_info):
        # Implementation of NLP to enhance product information
        return nlp_enhanced_product_info

class VertexAIIntegration:
    def apply_vertex_ai(self, product_info):
        # Implementation of Vertex AI integration
        return ai_enhanced_product_info

class DataStructure:
    def __init__(self):
        self.product_info = {}

class ProductInformationAPI:
    def __init__(self):
        self.custom_search_api = CustomSearchAPI()
        self.web_scraping = WebScraping()
        self.pdf_processing = PDFProcessing()
        self.nlp_processing = NLPProcessing()
        self.vertex_ai_integration = VertexAIIntegration()
        self.data_structure = DataStructure()

    def process_product_information(self, keyword):
        self.data_structure.product_info = self.custom_search_api.search(keyword)
        website_info = self.web_scraping.scrape_websites(self.data_structure.product_info['links'])
        pdf_info = self.pdf_processing.process_pdfs(self.data_structure.product_info['pdf_links'], 'type_filter')
        self.data_structure.product_info.update(website_info)
        self.data_structure.product_info.update(pdf_info)
        self.data_structure.product_info = self.nlp_processing.apply_nlp(self.data_structure.product_info)
        self.data_structure.product_info = self.vertex_ai_integration.apply_vertex_ai(self.data_structure.product_info)

    def get_product_information(self):
        return self.data_structure.product_info


**Base URL:**

`https://www.googleapis.com/customsearch/v1`

**Parameters:**

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