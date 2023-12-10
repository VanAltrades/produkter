# pip install -U pip setuptools wheel
# pip install -U spacy
# python -m spacy download en_core_web_sm

# Example: use spaCy for named entity recognition (NER)
import spacy
from collections import Counter

class LanguageProcessor:
    
    def __init__(self, dictionary):
        
        self.nlp = spacy.load("en_core_web_sm")
        self.dictionary = dictionary

    def extract_attributes(self, corpus):
        corpus_load = self.nlp(corpus)
        attributes = {ent.label_: ent.text for ent in corpus_load.ents}
        print(attributes)

    # extract_attributes(corpus = "The product has a red color, large size, and costs $20.")


    def extract_item_type(self, product_title):
        doc = self.nlp(product_title)

        # Extracting noun chunks (phrases that contain nouns)
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]

        # You can customize this based on your specific data
        # Here, we are considering the first noun chunk as the item type
        if noun_chunks:
            return noun_chunks[0]

        return None
    
    # # Extracting item types for each product title
    # for title in product_titles:
    #     item_type = extract_item_type(title)
    #     print(f"Product Title: {title}\nItem Type: {item_type}\n")


    def calculate_confidence_score(self, text_corpus, keyword_phrases):
        # Process the text corpus with spaCy
        doc = self.nlp(text_corpus)

        # Tokenize and count words
        word_counts = Counter([token.text.lower() for token in doc if token.is_alpha])

        confidence_scores = {}

        for phrase in keyword_phrases:
            # Tokenize the keyword phrase
            tokens = self.nlp(phrase.lower())
            
            # Calculate the frequency of the keyword phrase
            phrase_frequency = sum(word_counts[token.text] for token in tokens if token.text in word_counts)

            # Calculate the overall word frequency
            total_words = sum(word_counts.values())

            # Calculate the confidence score for the keyword phrase
            confidence_score = phrase_frequency / total_words if total_words > 0 else 0
            confidence_scores[phrase] = confidence_score

        return confidence_scores