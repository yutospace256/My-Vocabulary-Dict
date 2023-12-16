import uuid
from api import API
from entries import PrimaryDict, SimilarWords, Sentence
from mysql_connect import MySQLConnector
import confidential

mysql = MySQLConnector(host=confidential.mysql_host, user=confidential.mysql_user, password=confidential.mysql_pass, database=confidential.mysql_db)
api = API()

class CommonObjectProcessor():
    def __init__(self):
        self.generated_ids = []

    # Generate ID 
    def generate_uuid(self, namespace_identifier, name):
        # Create a UUID object using the specified namespace identifier and name
        uuid_obj = uuid.uuid5(namespace_identifier, name)

        # Convert the UUID object to a string representation
        uuid_string = str(uuid_obj)

        # Return the generated UUID string
        return uuid_string
    
    def _word_exists_like(self, column, word):
        try:
            word_search_query = f"SELECT EXISTS (SELECT 1 FROM primary_dict WHERE {column} LIKE %s)"
            mysql.execute_query(word_search_query, (f"%{word}%",))
            result = mysql.fetchone()
            mysql.close()
            return bool(result)
        
        except Exception as e:
            print(f"Error checking word existence: {e}")
            return False
    
    # Add entry to MySQL
    # Add primary dictionary entry
    def add_primary_dict(self, entry):
        mysql.insert_data(query='INSERT INTO primary_dict (word_id, word, normalized_word, word_lang, classification_id, similar_words_id, sentence_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', values=(entry.word_id, entry.word, entry.normalized_word, entry.word_lang, entry.classification_id, entry.similar_word_id, entry.sentence_id))
        mysql.close

    def add_similar_words(self, entry):
        mysql.insert_data(query='INSERT INTO similar_words (similar_word_id, similar_words, synonyms, similar_spell) VALUES (%s, %s, %s, %s)', values=(entry.similar_word_id, entry.similar_words, entry.synonyms, entry.similar_spell))
        mysql.close

    def add_sentence(self, entry):
        mysql.insert_data(query='INSERT INTO sentences (sentence_id, sentences) VALUES (%s, %s)', values=(entry.sentence_id, entry.sentences))
        mysql.close

    # Primary dict entry creation
    # Only when there is no same word in primary_dict
    def create_primary_dict(self, word):
        # Generate a UUID for the word
        uuid_word = "primary_dict_" + word
        word_id = self.generate_uuid(namespace_identifier=uuid.NAMESPACE_OID, name=uuid_word)
        normalized_word = api.normalize_word(word)
        classification_id = api.get_classification(word)

        # Determine if normalized exists in primary_dict
        if  self._word_exists_like("normalized_word", normalized_word):
            # Get IDs from mysql primary_dict
            mysql.execute_query("SELECT similar_words_id, sentence_id FROM primary_dict WHERE normalized_word = %s INDEX (normalized_word_index)", (normalized_word,))
            similar_word_id, sentence_id = mysql.fetchone()
        else:
            # Create similar words entry
            similar_word_id = self._create_similar_words(word)
            # Create sentence entry
            sentence_id = self._create_sentence(word)
        mysql.close()
        # Create a primary dictionary entry object
        # Exploring how to set native_lang
        primary_dict_entry = PrimaryDict(word_id, word, normalized_word, "en", classification_id, similar_word_id, sentence_id)
        self.add_primary_dict(primary_dict_entry)

    # Works only within create_primary_dict_entry
    def _create_similar_words(self, word):
        uuid_similar_words = "similar_words_" + word
        similar_word_id = self.generate_uuid(namespace_identifier=uuid.NAMESPACE_OID, name=uuid_similar_words)
        
        similar_words, synonyms, similar_spell = api.generate_words(word)

        # Create a similar words entry object
        similar_words_entry = SimilarWords(similar_word_id, similar_words, synonyms, similar_spell)
        self.add_similar_words(similar_words_entry)

        return similar_word_id

    def _create_sentence(self, word):
        uuid_sentence = "sentence_" + word
        sentence_id = self.generate_uuid(namespace_identifier=uuid.NAMESPACE_OID, name=uuid_sentence)

        sentences = api.get_example_sentences(word)

        # Create a sentence entry object
        sentence_entry = Sentence(sentence_id, sentences)
        self.add_sentence(sentence_entry)

        return sentence_id