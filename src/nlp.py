# pip install -U pip setuptools wheel
# pip install -U spacy
# python -m spacy download en_core_web_sm

# Example: use spaCy for named entity recognition (NER)
import spacy
from collections import Counter


nlp = spacy.load("en_core_web_sm")

# TODO: refer to schema for get_url function... this should be separated to reuse.

def get_attributes(corpus):
    corpus_load = nlp(corpus)
    attributes = {ent.label_: ent.text for ent in corpus_load.ents}
    print(attributes)

# get_attributes(corpus = "The product has a red color, large size, and costs $20.")

def calculate_confidence_for_phrases(text_corpus, keyword_phrases):
    # Process the text corpus with spaCy
    doc = nlp(text_corpus)

    # Tokenize and count words
    word_counts = Counter([token.text.lower() for token in doc if token.is_alpha])

    confidence_scores = {}

    for phrase in keyword_phrases:
        # Tokenize the keyword phrase
        tokens = nlp(phrase.lower())
        
        # Calculate the frequency of the keyword phrase
        phrase_frequency = sum(word_counts[token.text] for token in tokens if token.text in word_counts)

        # Calculate the overall word frequency
        total_words = sum(word_counts.values())

        # Calculate the confidence score for the keyword phrase
        confidence_score = phrase_frequency / total_words if total_words > 0 else 0
        confidence_scores[phrase] = confidence_score

    return confidence_scores

# Example usage with a list of keyword phrases
text_corpus = """Browse our exclusive collection of auto accessories that includes top quality products to enhance the style, comfort and functionality of your vehicle. We provide one stop shop for the perfect auto accessories for the vehicle.
Features
RV Siding Mesa
High quality construction and durability
Variety of styles for every type of accessory
4 Piece
Specifications
Design: Mesa
Length: 16 in.
Width: 96 in.
Color: Polar White
Material: Aluminum"""
# keyword_phrases = ["example keyword", "another phrase"]
# confidence_scores = calculate_confidence_for_phrases(text_corpus, keyword_phrases)

# # Print confidence scores for each keyword phrase
# for phrase, score in confidence_scores.items():
#     print(f"Confidence score for '{phrase}': {score}")