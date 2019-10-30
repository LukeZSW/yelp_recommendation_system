# -*- coding: UTF-8 -*-
# retrieve information by whoosh library
# two methods: BM25F (default) and TF_IDF
# combine with CF

from whoosh import index
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh import scoring, query, sorting, qparser
from .collaborative_filtering import user_cf
import numpy as np


def query_search(indexdir, queries, n=10, function='BM25F'):
    ix = index.open_dir(indexdir)
    search_fields = ['resname', 'categories', 'address', 'city', 'state']  # search fields
    og = qparser.OrGroup.factory(0.9)
    qp = MultifieldParser(search_fields, ix.schema, termclass=query.Variations, group=og)
    qp.add_plugin(DateParserPlugin(free=True))
    q = qp.parse(queries)
    result_index = []
    if function == 'BM25F':
        with ix.searcher(weighting=scoring.BM25F(B=0.75, K1=1.2)) as s:
            rates = sorting.FieldFacet('rating', reverse=True)
            scores = sorting.ScoreFacet()
            results = s.search(q, limit=n, sortedby=[scores, rates])
            k = min(len(results), n)
            for i in range(k):
                result_index.append(int(results[i]['ID']))
    if function == 'TF_IDF':
        with ix.searcher(weighting=scoring.TF_IDF()) as s:
            rates = sorting.FieldFacet('rating', reverse=True)
            scores = sorting.ScoreFacet()
            results = s.search(q, limit=n, sortedby=[scores, rates])
            k = min(len(results), n)
            for i in range(k):
                result_index.append(int(results[i]['ID']))
    return result_index


def person_query_search(indexdir, queries, user_id, E, n=10, function='BM25F'):
    prediction = user_cf(E, user_id, 3)
    ix = index.open_dir(indexdir)
    search_fields = ['resname', 'categories', 'address', 'city', 'state']  # search fields
    og = qparser.OrGroup.factory(0.9)
    qp = MultifieldParser(search_fields, ix.schema, termclass=query.Variations, group=og)
    qp.add_plugin(DateParserPlugin(free=True))
    q = qp.parse(queries)
    result_index = []
    if function == 'BM25F':
        # with ix.searcher(weighting=scoring.BM25F(B=0.75, resname_B = 1.0, categories_B = 0.8, K1=1.2)) as s:
        # add weight for the resname and the categories_B
        with ix.searcher(weighting=scoring.BM25F(B=0.75, K1=1.2)) as s:
            scores = sorting.ScoreFacet()
            results = s.search(q, limit=None, sortedby=[scores])
            m = len(results)
            if m != 0:
                relevance = np.zeros(m)
                expected = np.zeros(m)
                for i in range(m):
                    relevance[i] = - results[i].score
                relevance = (relevance - relevance.min()) / (relevance.max() - relevance.min())
                # normalized score from 0 to 1
                for i in range(m):
                    expected[i] = relevance[i] * prediction[int(results[i]['ID'])]
                indorder = np.argsort(expected)
                k = min(m, n)
                for i in range(k):
                    result_index.append(int(results[indorder[-1-i]]['ID']))
    if function == 'TF_IDF':
        with ix.searcher(weighting=scoring.TF_IDF()) as s:
            scores = sorting.ScoreFacet()
            results = s.search(q, limit=m, sortedby=[scores])
            m = len(results)
            if m != 0:
                relevance = np.zeros(m)
                expected = np.zeros(m)
                for i in range(m):
                    relevance[i] = - results[i].score
                relevance = (relevance - relevance.min())/(relevance.max() - relevance.min())  # normalized score from 0 to 1
                for i in range(m):
                    expected[i] = relevance[i] * prediction[int(results[i]['ID'])]
                indorder = np.argsort(expected)
                k = min(m, n)
                for i in range(k):
                    result_index.append(int(results[indorder[-1-i]]['ID']))
    return result_index
