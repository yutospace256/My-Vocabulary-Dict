import mysql.connector
import confidential
from mysql_connect import MySQLConnector
import uuid
from api import API
import nltk
from common import CommonObjectProcessor
from entries import Folder, DictEntry, SentenceEntry



mysql = MySQLConnector(host=confidential.mysql_host, user=confidential.mysql_user, password=confidential.mysql_pass, database=confidential.mysql_db)

api = API()
cop = CommonObjectProcessor()

# Prosessing Classes

class Dict():
    def __init__(self, user_id, native_lang, target_lang):
        self.user_id = user_id
        self.native_lang = native_lang
        self.target_lang = target_lang
        self.entries = []
        self.buckets = []

    # Add entry to MySQL
    # Add persinal dictionary entry
    def add_dict_entry(self, entry):
        mysql.insert_data(query='INSERT INTO personal_dict (dict_id, user_id, word_id, word_lang, folder_id, classification_id, meaning, mean_lang, similar_word_id, sentence_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values=(entry.dict_id, entry.user_id, entry.word_id, entry.word_lang, entry.folder_id, entry.classification_id, entry.meaning, entry.mean_lang, entry.similar_word_id, entry.sentence_id))
        mysql.close

    def add_sentence_entry(self, entry):
        mysql.insert_data(query='INSERT INTO personal_sentence (dict_id, user_id, sentence, word_lang, folder_id, classification_id, meanng, mean_lang, similar_words) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', values=(entry.dict_id, entry.user_id, entry.sentence, entry.word_lang, entry.folder_id, entry.classification_id, entry.meaning, entry.mean_lang, entry.similar_words))
        mysql.close

    def add_folder_entry(self, entry):
        mysql.insert_data(query='INSERT INTO folders (folder_id, user_id, folder_name) VALUES (%s, %s, %s)', values=(entry.folder_id, entry.user_id, entry.folder_name))
        mysql.close

    # Insert data into mysql       
    def create_new_dict_entry(self, word, folder_id="Unrecorded", meaning="A"):
        # Generate a UUID for the word
        uuid_word = "personal_dict_" + word
        dict_id = cop.generate_uuid(namespace_identifier=uuid.NAMESPACE_OID, name=uuid_word)
        if  cop._word_exists_like("word", word):
            cop.create_primary_dict(word)
        word_id = mysql.fetch_data("SELECT word_id FROM primary_dict WHERE word = %s INDEX (word_index)", (word,))[0][0]
        classification_id = api.get_classification(word)
        # Get similar_word_id,sentence_id from data where word_id column of mysql primary_dict is word_id
        mysql.execute_query("SELECT similar_words_id, sentence_id FROM primary_dict WHERE word = %s INDEX (word_index)", (word,))
        similar_word_id, sentence_id = mysql.fetchone()
        mysql.close()
        dict_entry = DictEntry(dict_id, self.user_id, word_id, self.native_lang, folder_id, classification_id, meaning, self.target_lang, similar_word_id, sentence_id)
        # Add dict entry to mysql
        self.add_dict_entry(dict_entry)

    def create_new_sentence_entry(self, sentence, folder_id="Unrecorded", meaning="A"):
        # Generate a UUID for the sentence
        uuid_sentence = "personal_sentence_" + sentence
        dict_id = cop.generate_uuid(namespace_identifier=uuid.NAMESPACE_OID, name=uuid_sentence)
        sentence_entry = SentenceEntry(dict_id, self.user_id, sentence, self.native_lang, folder_id, meaning, self.target_lang)
        # Add dict entry to mysql
        self.add_sentence_entry(sentence_entry)

    def create_new_folder(self, folder_name):
        folder_id = cop.generate_uuid(namespace_identifier=uuid.NAMESPACE_X500, name=folder_name)
        folder_entry = Folder(folder_id, self.user_id, folder_name)
        # Add folder entry to mysql
        self.add_folder_entry(folder_entry)

    
