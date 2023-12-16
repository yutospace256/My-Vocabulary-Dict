import deepl
import confidential
import requests
import nltk
import unicodedata

class API():
    def __init__(self):
        self.usage = 0
        self.datamuse_url = "https://api.datamuse.com/words"

    def transrate(self, word, native_lang, target_lang):
        auth_key = confidential.deepl_key

        # Create a translator object using your authentication key
        translator = deepl.Translator(auth_key)

        # Translate the word using the translator object
        translated_text = translator.translate_text(word, target_lang=target_lang, source_lang=native_lang)

        return translated_text

    def _use_datamuse(self, mode, word):
        params = {mode: word}
        response = requests.get(self.datamuse_url, params=params)
        words = [result["word"] for result in response.json()[:10]]
        return words

    def generate_words(self, word):
        # Similar Words use Related word
        similar_words_1 = self._use_datamuse(mode="rel_syn", word=word)
        similar_words_2 = self._use_datamuse(mode="rel_gen", word=word)
        similar_words_3 = self._use_datamuse(mode="rel_spc", word=word)
        similar_words = similar_words_1 + similar_words_2 + similar_words_3
        # Synonyms use Means like
        synonyms = self._use_datamuse(mode="ml", word=word)
        # Similar Spell use Spelled like
        similar_spell = self._use_datamuse(mode="sl", word=word)
        # Change to json
        similar_words = {"similar_words": similar_words}
        synonyms = {"synonyms": synonyms}
        similar_spell = {"similar_spell": similar_spell}
        
        return similar_words, synonyms, similar_spell

    def get_classification(self, phrase):
        # Tokenize the phrase
        tokens = nltk.word_tokenize(phrase)

        # Chunk the tokens
        tree = nltk.chunk.ne_chunk(nltk.pos_tag(tokens))

        # Extract relevant information from the chunked tree
        classification = ""
        for chunk in tree:
            if type(chunk) == nltk.tree.Tree:
                chunk_type = chunk.label()
                chunk_text = " ".join([token for (token, tag) in chunk])
                # Define rules to map chunk types and text to your desired classification
                if chunk_type == "NP":
                    classification += f"NOUN_PHRASE({chunk_text}) "
                elif chunk_type == "VP":
                    classification += f"VERB_PHRASE({chunk_text}) "
            else:
                classification += f"{chunk[1]} "

        # Return the final classification
        return classification.strip()
    
    def get_example_sentences(self, word):
        synsets = nltk.corpus.wordnet.synsets(word)
        example_sentences = []
        for synset in synsets:
            for example in synset.examples():
                example_sentences.append(example.strip())
        return example_sentences
    
    def normalize_word(self, word):
        # Convert to lowercase
        word = word.lower()

        # Remove extra spaces
        word = word.strip()

        # Remove accents and diacritics
        word = unicodedata.normalize('NFD', word)
        word = word.encode('ascii', 'ignore').decode('utf-8')

        # Convert plural forms to singular using NLTK
        word = nltk.wordnet.WordNetLemmatizer().lemmatize(word)

        return word

