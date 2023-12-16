from cls.EngineSearchDictionary import Engine, SearchDictionary
from cls.Sites import Sites
from cls.EnginePdfs import PdfEngine, PdfDictionary
from cls.LanguageProcessor import LanguageProcessor
from cls.Suggestions import Suggestions
from cls.Trends import Trends

from cls.Formatter import Formatter

keyword = "milwaukee m18 fuel"
# Engine Ranks
engine_instance = Engine("milwaukee m18 fuel")
engine_instance = Engine("AMD Ryzen 9 5900X")
engine_instance = Engine("Huy Fong HFSR3G")
engine_instance = Engine("Portal PAT-2416096054")
engine_instance = Engine("UPC 680327998169")
engine_instance = Engine("Okuma PCH-C-741XXXH")
engine_instance = Engine("Zero Degree 38152")
len(engine_instance.results)
engine_instance.results

# Create an instance of Rank and automatically pass the serp_dicts
search_dictionary_instance = SearchDictionary(engine_instance)
search_dictionary_instance.dictionary
    # Format ranks
s_dict = Formatter(search_dictionary_instance.dictionary)
s_dict_wo_nones = s_dict.format(keep_none_values=False)
### ^ route response

sites_instance = Sites(search_dictionary_instance)
sites_instance.links
sites_instance.titles
sites_instance.dictionary_schemas
sites_schema_dict_formatted = Formatter(sites_instance.dictionary_schemas)
sites_schema_dict_formatted_wo_nones = sites_schema_dict_formatted.format(keep_none_values=False)
### ^ route response

sites_instance.dictionary_texts

# LanguageProcess
# items
lp = LanguageProcessor(sites_instance, keyword)
lp.items

# Suggests
suga = Suggestions(lp)
suga.questions
suga.suggested_queries

# Trends


# PDF Ranks
pdf_instance = PdfEngine("milwaukee m18 fuel")

pdf_search_dictionary_instance = PdfDictionary(pdf_instance)
pdf_dict = pdf_search_dictionary_instance.dictionary
links = Formater(pdf_dict)
pdf_dict_w_none = pdf_dict.format(keep_none_values=True)
