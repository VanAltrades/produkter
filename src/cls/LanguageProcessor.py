# pip install -U pip setuptools wheel
# pip install -U spacy
# python -m spacy download en_core_web_sm

# Example: use spaCy for named entity recognition (NER)
import spacy
import re
from collections import Counter

class LanguageProcessor:
    
    def __init__(self, sites_instance, keyword):
        self.keyword = keyword

        self.nlp = spacy.load("en_core_web_sm")
        self.titles = sites_instance.titles
        self.texts = list(sites_instance.dictionary_texts.values())

        self.items = self.extract_item_types()
        # self.attributes = self.extract_attributes() # entities not product attributes


    def remove_special_characters(self, text):
        # Use a regular expression to remove non-alphanumeric characters
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    

    def calculate_confidence_score(self, text_corpus):
        # Process the text corpus with spaCy
        doc = self.nlp(text_corpus)

        # Tokenize and count words
        word_counts = Counter([token.text.lower() for token in doc if token.is_alpha])

        # Tokenize the keyword phrase
        tokens = self.nlp(self.keyword.lower())
        
        # Calculate the frequency of the keyword phrase
        phrase_frequency = sum(word_counts[token.text] for token in tokens if token.text in word_counts)

        # Calculate the overall word frequency
        total_words = sum(word_counts.values())

        # Calculate the confidence score for the keyword phrase
        confidence_score = phrase_frequency / total_words if total_words > 0 else 0

        return confidence_score
    

    def extract_item_types(self):
        item_types = []

        # Add self.keyword to the item_types list
        item_types.append(self.keyword)

        for title in self.titles:
            doc = self.nlp(title)

            # Extracting noun chunks (phrases that contain nouns)
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]

            # You can customize this based on your specific data
            # Here, we are considering the first noun chunk as the item type
            if noun_chunks:
                cleaned_chunk = self.remove_special_characters(noun_chunks[0])
                
                # apply confidence score based on keyword to return only >=.25 CIs title items
                confidence_score = self.calculate_confidence_score(cleaned_chunk, self.keyword)
                if confidence_score >= 0.25:
                    item_types.append(cleaned_chunk)
            else:
                item_types.append(None)

        return item_types
    

    def extract_attributes(self):
        all_attributes = {}

        for corpus in self.texts:
             if corpus is not None:
                corpus_load = self.nlp(corpus)
                attributes = {ent.label_: ent.text for ent in corpus_load.ents}
                
                for label, text in attributes.items():
                    if label not in all_attributes:
                        all_attributes[label] = set()  # Using a set to store distinct values for each label
                    all_attributes[label].add(text)

        distinct_attributes = {label: list(values) for label, values in all_attributes.items()}
        return distinct_attributes

    # extract_attributes(corpus = "The product has a red color, large size, and costs $20.")



# # Example usage with a list of keyword phrases
# text_corpus = """Browse our exclusive collection of auto accessories that includes top quality products to enhance the style, comfort and functionality of your vehicle. We provide one stop shop for the perfect auto accessories for the vehicle.
# Features
# RV Siding Mesa
# High quality construction and durability
# Variety of styles for every type of accessory
# 4 Piece
# Specifications
# Design: Mesa
# Length: 16 in.
# Width: 96 in.
# Color: Polar White
# Material: Aluminum"""
# keyword_phrases = ["example keyword", "another phrase"]
# confidence_scores = calculate_confidence_for_phrases(text_corpus, keyword_phrases)

# # Print confidence scores for each keyword phrase
# for phrase, score in confidence_scores.items():
#     print(f"Confidence score for '{phrase}': {score}")