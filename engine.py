from elasticsearch_dsl import Search, A
from elasticsearch_dsl.search import AggsProxy
from elasticsearch_dsl.query import Match, Range, Q, Regexp, Fuzzy, Term, Exists, MatchPhrasePrefix
from elasticsearch_dsl.aggs import TopHits, Nested, ReverseNested, WeightedAvg
from models import Message
from typing import List

from es_wrapper import ElasticSearchWrapper
from es_helpers import get_connection, WORDCLOUD_INDEX, MEETING_POINTS_INDEX

INDEX_NAME = "wordcloud_test"

class ElasticSearchEngine:

    def __init__(self):
        self.client = get_connection()
        self._search = Search(using=self.client, doc_type="doc").extra(
            track_total_hits=True
        )
        self.proxy = AggsProxy(self._search)

    def aggregate(self):
        if self.proxy.aggs:
            self._search.aggs = self.proxy
        return self

    def execute(self):
        return self._search.execute()

    def _create_bucket(self, name, query):
        return self.proxy.bucket(name, query)

    def _match(self, field, val, term=False):
        query = ElasticSearchWrapper.match_phrase_prefix(field, val)
        self._search = self._search.query(Q("bool", must=query))

    def wordcloud(self):
        self._search.index(WORDCLOUD_INDEX)
        s = Search(using=self.client)
        bucket = self._create_bucket(
            "tags", ElasticSearchWrapper.aggregate("message", page_size=30)
        )
        res = self.aggregate().execute()
        result = res['aggregations']['tags']['buckets']
        total_count = sum(x['doc_count'] for x in result)
        return [
            {'word': x['key'], 'weight': int(x['doc_count'] * 100 / total_count)} for x in result
        ]
    
    def autocomplete(self, message: str, autocomplete_type: str):
        s = Search(using=self.client)
        s.params(size=100)
        self._match("sender", message)
        res = self.aggregate().execute()
        result = set([x['_source']['sender'] for x in res['hits']['hits']])
        return result