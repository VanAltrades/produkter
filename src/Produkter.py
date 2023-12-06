from cls.EngineRanks import Engine, Ranks
from cls.Links import Links

# Example usage:
engine_instance = Engine("milwaukee m18 fuel")
engine_instance = Engine("AMD Ryzen 9 5900X")
# engine_instance.results

# Create an instance of Rank and automatically pass the serp_dicts
rank_instance = Ranks(engine_instance)
# rank_instance.ranks

links_instance = Links(rank_instance)