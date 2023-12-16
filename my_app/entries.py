# Instance Classes
# Parent Class
class Entry():
    def __init__(self, dict_id, user_id, word_lang, folder_id, meaning, mean_lang):
        self.dict_id = dict_id
        self.user_id = user_id
        self.word_lang = word_lang
        self.folder_id = folder_id
        self.meaning = meaning
        self.mean_lang = mean_lang

# Child Classes
class DictEntry(Entry):
    def __init__(self, dict_id, user_id, word_id, word_lang, folder_id, classification_id, meaning, mean_lang, similar_word_id, sentence_id):
        super().__init__(dict_id, user_id, word_lang, folder_id, classification_id, meaning, mean_lang, similar_word_id, sentence_id)

        self.word_id = word_id
        self.classification_id = classification_id 
        self.similar_word_id = similar_word_id
        self.sentence_id = sentence_id

class SentenceEntry(Entry):
    def __init__(self, dict_id, user_id, sentence, word_lang, folder_id, meaning, mean_lang):
        super().__init__(dict_id, user_id, word_lang, folder_id, meaning, mean_lang)

        self.sentence = sentence

# Other Classes
class PrimaryDict():
    def __init__(self, word_id, word, normalized_word, word_lang, classification_id, similar_word_id, sentence_id):
        self.word_id = word_id
        self.word = word
        self.normalized_word = normalized_word
        self.word_lang = word_lang
        self.classification_id = classification_id
        self.similar_word_id = similar_word_id
        self.sentence_id = sentence_id

class SimilarWords():
    def __init__(self, similar_word_id, similar_words, synonyms, similar_spell):
        self.similar_word_id = similar_word_id
        self.similar_words = similar_words
        self.synonyms = synonyms
        self.similar_spell = similar_spell

class Sentence():
    def __init__(self, sentence_id, sentences):
        self.sentence_id = sentence_id
        self.sentences = sentences

class Folder():
    def __init__(self, folder_id, user_id, folder_name):
        self.folder_id = folder_id
        self.user_id = user_id
        self.folder_name = folder_name