import mysql.connector
import deepl
import confidential




# MySQL Connector
class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.connection.cursor()

    def fetch_data(self, query, values):
        self.cursor.execute(query, values)
        results = self.cursor.fetchall()

        return results

    def update_data(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_data(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_data(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def execute_query(self, query, values):
        self.cursor.execute(query, values)

    def close(self):
        self.cursor.close()
        self.connection.close()


mysql = MySQLConnector(host=confidential.mysql_host, user=confidential.mysql_user, password=confidential.mysql_pass, database=confidential.mysql_db)

# Instance Classes
# Parent Class
class Entry():
    def __init__(self, dict_id, user_id, word_lang, folder_id, classification_id, meaning, mean_lang):
        self.dict_id = dict_id
        self.user_id = user_id
        self.word_lang = word_lang
        self.folder_id = folder_id
        self.classification_id = classification_id
        self.meaning = meaning
        self.mean_lang = mean_lang

# Child Classes
class DictEntry(Entry):
    def __init__(self, dict_id, user_id, word_id, word_lang, folder_id, classification_id, meaning, mean_lang):
        super().__init__(dict_id, user_id, word_lang, folder_id, classification_id, meaning, mean_lang)

        self.word_id = word_id

class SentenceEntry(Entry):
    def __init__(self, dict_id, user_id, sentence, word_lang, folder_id, classification_id, meaning, mean_lang):
        super().__init__(dict_id, user_id, word_lang, folder_id, classification_id, meaning, mean_lang)

        self.sentence = sentence

# Other Classes
class SimilarWords():
    def __init__(self, word_id, similar_words, synonyms, similar_spell):
        self.word_id = word_id
        self.similar_words = similar_words
        self.synonyms = synonyms
        self.similar_spell = similar_spell

class Sentence():
    def __init__(self, word_id, sentences):
        self.word_id = word_id
        self.sentences = sentences

class Folder():
    def __init__(self, folder_id, user_id, folder_name):
        self.folder_id = folder_id
        self.user_id = user_id
        self.folder_name = folder_name

# Prosessing Classes

class Dict():
    def __init__(self, user_id, native_lang, target_lang):
        self.user_id = user_id
        self.native_lang = native_lang
        self.target_lang = target_lang
        self.entries = []
        self.buckets = []

    # Add entry to MySQL
    # Add primary dictionary entry
    def add_primary_dict(self, entry):
        mysql.insert_data(query='INSERT INTO primary_dict (word_id, word, word_lang, classification_id) VALUES (%s, %s, %s, %s)', values=(entry.word_id, entry.word, entry.word_lang, entry.classification_id))
        mysql.close

    def add_similar_words(self, entry):
        mysql.insert_data(query='INSERT INTO similar_words (word_id, similar_word, synonyms, similar_spell) VALUES (%s, %s, %s, %s)', values=(entry.word_id, entry.similar_word, entry.synonyms, entry.similar_spell))
        mysql.close

    def add_sentence(self, entry):
        mysql.insert_data(query='INSERT INTO sentence (word_id, sentence) VALUES (%s, %s)', values=(entry.word_id, entry.sentence))
        mysql.close

    # Add persinal dictionary entry
    def add_dict_entry(self, entry):
        mysql.insert_data(query='INSERT INTO personal_dict (dict_id, user_id, word_id, word_lang, folder_id, classification_id, meanng, mean_lang, similar_words) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', values=(entry.dict_id, entry.user_id, entry.word_id, entry.word_lang, entry.folder_id, entry.classification_id, entry.meaning, entry.mean_lang, entry.similar_words))
        mysql.close

    def add_sentence_entry(self, entry):
        mysql.insert_data(query='INSERT INTO personal_sentence (dict_id, user_id, sentence, word_lang, folder_id, classification_id, meanng, mean_lang, similar_words) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', values=(entry.dict_id, entry.user_id, entry.sentence, entry.word_lang, entry.folder_id, entry.classification_id, entry.meaning, entry.mean_lang, entry.similar_words))
        mysql.close

    def add_folder_entry(self, entry):
        mysql.insert_data(query='INSERT INTO folders (folder_id, user_id, folder_name) VALUES (%s, %s, %s)', values=(entry.folder_id, entry.user_id, entry.folder_name))
        mysql.close



class API():
    def __init__(self):
        self.usage = 0

    def transrate(self, word, native_lang, target_lang):
        auth_key = confidential.deepl_key

        # Create a translator object using your authentication key
        translator = deepl.Translator(auth_key)

        # Translate the word using the translator object
        translated_text = translator.translate_text(word, target_lang=target_lang, source_lang=native_lang)

        return translated_text


