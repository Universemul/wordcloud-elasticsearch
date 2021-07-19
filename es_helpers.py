from elasticsearch_dsl import connections
from elasticsearch_dsl import Index
from elasticsearch import helpers

from models import Message, MeetingPoint

from typing import List

WORDCLOUD_INDEX = "wordcloud_index"
MEETING_POINTS_INDEX = "meeting_point_index"

def get_connection():
    return connections.create_connection(hosts=['127.0.0.1:9200'], timeout=60)
    
def create_index(index_name: str):
    get_connection()
    i = Index(index_name)
    i.document(Message if index_name == WORDCLOUD_INDEX else MeetingPoint)
    i.create()

def delete_index(index: str):
    try:
        get_connection()
        i = Index(index)
        i.delete()
    except Exception as e:
        print(e)

def get_mapping(index_name: str):
    client = get_connection()
    return client.indices.get_mapping(index=index_name)

def bulk_index(documents: List[object]):
    client = get_connection()
    helpers.bulk(client, documents)

def delete_wordcloud_index():
    delete_index(WORDCLOUD_INDEX)

def delete_meetingpoint_index():
    delete_index(MEETING_POINTS_INDEX)

def create_wordcloud_index():
    create_index(WORDCLOUD_INDEX)

def create_meetingpoint_index():
    create_index(MEETING_POINTS_INDEX)