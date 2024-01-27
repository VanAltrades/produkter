def format_search_dictionary(dictionary, keep_none_values=True):
    flat_dict = {}
    if keep_none_values is True:
        for inner_dict in dictionary.values():
            for key, value in inner_dict.items():
                if key not in flat_dict:
                    flat_dict[key] = []
                flat_dict[key].append(value)
    elif keep_none_values is False:
        for inner_dict in dictionary.values():
            for key, value in inner_dict.items():
                if key not in flat_dict and value is not None:
                    flat_dict[key] = [value]
                elif value is not None:
                    flat_dict[key].append(value)
    else:
        print("keep_none_values must be True of False")
        flat_dict = None
    return flat_dict

def format_schemas_dictionary(dictionary):        
    flat_dict = {}
    for inner_dict in dictionary.values():
        for key, value in inner_dict.items():
            if key not in flat_dict:
                flat_dict[key] = [value] if value is not None else [None]
            elif value is not None and value not in flat_dict[key]:
                flat_dict[key].append(value)

    # If all values for a key are None, add a single None to the list
    for key, values in flat_dict.items():
        if all(v is None for v in values):
            flat_dict[key] = [None]

    return flat_dict


# formatted by search index results 0,1,n 
# def format_search_dictionary(dictionary):
#     flat_dict = {}
#     for inner_dict in dictionary.values():
#         for key, value in inner_dict.items():
#             if key not in flat_dict:
#                 flat_dict[key] = [value] if value is not None else [None]
#             elif value is not None:
#                 flat_dict[key].append(value)
#     return flat_dict


# class Formatter:
    
#     def __init__(self, dictionary):
        
#         self.dictionary = dictionary
#         self.dictionary_formatted = None

    
#     def format(self, keep_none_values=True):
#         flat_dict = {}
#         if keep_none_values is True:
#             for inner_dict in self.dictionary.values():
#                 for key, value in inner_dict.items():
#                     if key not in flat_dict:
#                         flat_dict[key] = []
#                     flat_dict[key].append(value)
#         elif keep_none_values is False:
#             for inner_dict in self.dictionary.values():
#                 for key, value in inner_dict.items():
#                     if key not in flat_dict and value is not None:
#                         flat_dict[key] = [value]
#                     elif value is not None:
#                         flat_dict[key].append(value)
#         else:
#             print("keep_none_values must be True of False")
#             flat_dict = None
#         self.dictionary_formatted = flat_dict
#         return flat_dict

