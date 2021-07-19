from elasticsearch_dsl import A
from elasticsearch_dsl.query import Match, Q, Fuzzy, Term, MatchPhrasePrefix


class ElasticSearchWrapper(object):

    @classmethod
    def match(cls, key, data, operator=None):
        if not data:
            return Q()
        q = {key: {"query": data}}
        if operator:
            q = {key: {"query": data, "operator": operator}}
        return Match(**q)

    @classmethod
    def match_term(cls, key, data):
        if not data:
            return Q()
        return Term(**{key: data})

    @classmethod
    def match_phrase_prefix(cls, key, data):
        if not data:
            return Q()
        return MatchPhrasePrefix(**{key: data})

    @classmethod
    def aggregate(
        cls, _field, page_size=10000000, collect_mode="depth_first", min_doc_count=1
    ):
        return A(
            "terms",
            field=_field,
            size=page_size,
            collect_mode=collect_mode,
            min_doc_count=min_doc_count,
        )

    @classmethod
    def fuzzy(cls, field, data, fuzzy="AUTO", boost_value=1.0):
        params = dict(fuzziness=fuzzy, boost=boost_value, value=data)
        return Fuzzy(field=field, **params)
