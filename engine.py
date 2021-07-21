from elasticsearch_dsl import Search, A, UpdateByQuery
from elasticsearch_dsl.search import AggsProxy
from elasticsearch_dsl import Q

from es_wrapper import ElasticSearchWrapper
from es_helpers import get_connection, CITIES_INDEX, WORDCLOUD_INDEX

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
        if term:
            query = ElasticSearchWrapper.match(field, val)
        else:
            query = ElasticSearchWrapper.match_phrase_prefix(field, val)
        self._search = self._search.query(Q("bool", must=query))

    def _generate_es_search(self, index: str, page_size=100, sorted=False):
        self._search.index(index)
        self._search.params(size=page_size)
        if sorted:
            self._search.sort({"-_score": {"order": "desc"}})

    def wordcloud(self):
        self._generate_es_search(WORDCLOUD_INDEX, page_size=30)
        self._create_bucket(
            "words", ElasticSearchWrapper.aggregate("message", page_size=30)
        )
        res = self.aggregate().execute()
        result = res['aggregations']['words']['buckets']
        total_count = sum(x['doc_count'] for x in result)
        return [
            {'word': x['key'], 'weight': int(x['doc_count'] * 100 / total_count)} for x in result
        ]
    
    def autocomplete(self, message: str, autocomplete_type: str):
        self._generate_es_search(CITIES_INDEX, sorted=False)
        if autocomplete_type == "ngram":
            self._match("name_ngram", message, True)
        elif autocomplete_type == "match":
            self._match("name", message, True)
        elif autocomplete_type == "prefix":
            self._match("name_prefix", message)
        res = self.aggregate().execute()
        result = set([x['_source']['name'] for x in res['hits']['hits']])
        return result

    def suggest(self, message: str):
        self._generate_es_search(CITIES_INDEX, page_size=30, sorted=True)
        self._search = self._search.suggest("terms", message, completion={'field': 'name_suggest', "skip_duplicates": True})
        res = self.aggregate().execute()
        result = []
        if len(res.suggest.terms) == 0:
            return result
        for option in res.suggest.terms[0].options:
            result.append({
                'id': option._source.id,
                'name': option._source.name
            })
        return result

    def updateWeight(self, id: str):
        ubq = UpdateByQuery(using=self.client, index=CITIES_INDEX, doc_type="doc").query("match", id=id).script(source="ctx._source.name_suggest.weight++")
        ubq.execute()

