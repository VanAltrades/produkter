from cls.EngineRanks import Engine, Ranks
from cls.Links import Links
from cls.Formater import Formater
from cls.EnginePdfs import PdfEngine, PdfRanks

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
rank_instance = Ranks(engine_instance)
rank_instance.ranks

links_instance = Links(rank_instance)
links_instance.schemas
links_instance.texts
# links_instance.links

# Formated Ranks
ranks = Formater(rank_instance)
ranks_reponse_w_none = ranks.format(keep_none_values=True)
ranks_reponse_wo_none = ranks.format(keep_none_values=False)

# Formated Links
links = Formater(links_instance)
links_reponse_w_none = links.format(keep_none_values=True)
links_reponse_wo_none = links.format(keep_none_values=False)


# LanguageProcess
# items
# attributes
# confidence score


# Suggests
# terms
# questions


# Trends


# PDF Ranks
pdf_instance = PdfEngine("milwaukee m18 fuel")

pdf_rank_instance = PdfRanks(pdf_instance)
pdf_rank_instance.ranks
