from elasticsearch_dsl import Document, Text, Completion, Integer, Keyword
from analyzers import english_analyzer, ngram_analyzer, french_analyzer, ascii_fold

class Message(Document):
    
    message = Text(analyzer=english_analyzer, fielddata=True)
    sender_suggest = Completion()
    sender = Text(analyzer=ngram_analyzer, fielddata=True)

class City(Document):
    
    id = Integer()
    name = Text(analyzer=french_analyzer, fielddata=True)
    name_suggest = Completion(analyzer=ascii_fold)
    name_prefix = Keyword()
    name_ngram = Text(analyzer=ngram_analyzer, fielddata=True)