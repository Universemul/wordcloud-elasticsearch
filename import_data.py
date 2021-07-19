import json
import uuid
import csv

from engine import ElasticSearchEngine
from models import Message, MeetingPoint
from es_helpers import delete_wordcloud_index, delete_meetingpoint_index, create_wordcloud_index, create_meetingpoint_index, MEETING_POINTS_INDEX, WORDCLOUD_INDEX, bulk_index

def wordcloud():
    _file = "samples/reviews_Amazon_Instant_Video_5.json"
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
    _file = "samples/mps_fr.csv"
    es = ElasticSearchEngine()
    delete_meetingpoint_index()
    create_meetingpoint_index()
    documents = []
    with open(_file, "r") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            item = MeetingPoint()
            item.name = row['NAME']
            item.name_suggest = row['NAME']
            item.name_prefix = row['NAME']
            item.name_ngram = row['NAME']
            item.id = row['ID']
            documents.append({
                '_id': str(uuid.uuid4()),
                '_index': MEETING_POINTS_INDEX,
                '_source': item.to_dict()
            })
    if not documents:
       print("FAIL INDEXATION")
       exit(-1)
    bulk_index(documents)
    print("INDEXATION OK")

def run():
    #wordcloud()
    meetingpoints()

run()