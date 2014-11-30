#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function


def get_query(like_text):

  qry = {
    'query': {
      'filtered': {
        'query': {
          'more_like_this': {
            'fields': ['text'],
            'like_text': like_text,
            'min_term_freq': 2,
            'max_query_terms': 15,
            'min_word_length': 4,
          }
        },
        'filter': {
          'bool': {
            'must_not': [
              {
                'term': {
                  'title': 'fil'
                }
              },
              {
                'term': {
                  'title': 'kategorier'
                }
              },
              {
                'term': {
                  'title': 'kategori'
                }
              },
              {
                'term': {
                  'title': 'mal'
                }
              },
              {
                'term': {
                  'title': 'wikipedia'
                }
              }
            ]
          }
        }
      }
    },
    'aggs': {
      'my_tags': {
        'significant_terms': {
          'field': 'text',
          'size': 100,
          'min_doc_count': 3
        }
      }
    }
  }

  return qry



def main():

  import sys
  from elasticsearch import Elasticsearch
  from jaccard.jaccard import group_similar_words
  from helpers.helpers import print_matching_docs
  from helpers.helpers import print_scores_and_groups

  import settings

  shingle_size = 2
  jaccard_threshold = 0.6


  index = settings.index
  doc_type = settings.doc_type

  es = Elasticsearch(host=settings.es_host,port=settings.es_port)

  while True:

    print()
    print('input text (Control-D to submit):')
    print()

    try:
      data = str(sys.stdin.read())
      print()
    except Exception:
      data = ''

    if data.strip():

      qry = get_query(data)
      res = es.search(index=index,doc_type=doc_type,body=qry,timeout=60)
      buckets = res['aggregations']['my_tags']['buckets']
      groups = group_similar_words(buckets,
                                   min_word_length=4,
                                   jaccard_threshold=jaccard_threshold,
                                   shingle_size=shingle_size)

      print()
      print()
      hits = res['hits']['hits']
      print_matching_docs(hits)
      print()
      print()
      print_scores_and_groups(groups,lower_threshold=0.25)

  return


if __name__ == '__main__':

  main()

