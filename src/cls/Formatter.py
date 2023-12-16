class Formatter:
    
    def __init__(self, dictionary):
        
        self.dictionary = dictionary
        self.dictionary_formatted = None

    
    def format(self, keep_none_values=True):
        flat_dict = {}
        if keep_none_values is True:
            for inner_dict in self.dictionary.values():
                for key, value in inner_dict.items():
                    if key not in flat_dict:
                        flat_dict[key] = []
                    flat_dict[key].append(value)
        elif keep_none_values is False:
            for inner_dict in self.dictionary.values():
                for key, value in inner_dict.items():
                    if key not in flat_dict and value is not None:
                        flat_dict[key] = [value]
                    elif value is not None:
                        flat_dict[key].append(value)
        else:
            print("keep_none_values must be True of False")
            flat_dict = None
        self.dictionary_formatted = flat_dict
        return flat_dict

