import json
import uuid

from engine import ElasticSearchEngine
from models import Message, MeetingPoint
from es_helpers import delete_wordcloud_index, delete_meetingpoint_index, create_wordcloud_index, create_meetingpoint_index, MEETING_POINTS_INDEX, WORDCLOUD_INDEX, bulk_index

def wordcloud():
    _file = "reviews_Amazon_Instant_Video_5.json"
    delete_wordcloud_index()
    create_wordcloud_index()
    documents = []
    with open(_file, "r") as f:
        lines = f.readlines()
        for l in lines:
            tmp = json.loads(l)
            msg = Message()
            msg.message = tmp["reviewText"]
            msg.sender = tmp.get("reviewerName", "")
            msg.sender_suggest = tmp.get("reviewerName", "")
            documents.append({
                '_id': str(uuid.uuid4()),
                '_index': WORDCLOUD_INDEX,
                '_source': msg.to_dict()
            })
    if not documents:
       print("FAIL INDEXATION")
       exit(-1)
    bulk_index(documents)
    print("INDEXATION OK")

def meetingpoints():
    _file = "meetingpoint.csv"
    es = ElasticSearchEngine(index_name=MEETING_POINTS_INDEX)
    delete_meetingpoint_index()
    create_meetingpoint_index()
    documents = []
    with open(_file, "r") as f:
        lines = f.readlines()
        for l in lines:
            tmp = json.loads(l)
            msg = MeetingPoint()()
            msg.message = tmp["reviewText"]
            msg.sender = tmp.get("reviewerName", "")
            msg.sender_suggest = tmp.get("reviewerName", "")
            documents.append({
                '_id': str(uuid.uuid4()),
                '_index': "wordcloud_test",
                '_source': msg.to_dict()
            })
    if not documents:
       print("FAIL INDEXATION")
       exit(-1)
    es.bulk_index(documents)
    print("INDEXATION OK")

def run():
    wordcloud()
    #meetingpoints()

run()