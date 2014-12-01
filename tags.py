#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function


def main():

  import sys
  from elasticsearch import Elasticsearch
  import settings

  ## all these modules are located in ./python_modules

  from jaccard.jaccard import group_similar_words
  from helpers.helpers import print_matching_docs
  from helpers.helpers import print_scores_and_groups
  from helpers.helpers import pretty_json
  from search.search import get_tag_query


  es = Elasticsearch(host=settings.es_host,
                     port=settings.es_port)


  print('\nInput text (Control-D to submit):\n\n')

  ## read from terminal
  data = unicode(sys.stdin.read().decode('utf8')).strip()

  print('\n\nprocessing {:d} characters...\n\n'.format(len(data)))

  q = get_tag_query(data)

  ## Sometimes Elasticsearch is a little slow when you have just started it.
  ## Try adding a timeout=60 here if you have timeout issues.
  ## WARNING: I have had some weird experiences with inconsistent query results
  ## when setting a timeount, and I have yet to find an explanation.
  res = es.search(index=settings.index,
                  body=q)

  #pretty_json(res)
  hits = res['hits']['hits']
  buckets = res['aggregations']['my_tags']['buckets']

  ## prints some of the wiki articles that are similar to the input text
  print('\n\n\nnumber of similar documents: ',res['hits']['total'],'\n')
  print_matching_docs(hits)
  print('\n\n')

  ## Use Jaccard similarity to group together words that are similar
  ## The returned score for each group of similar words is the best score of the
  ## words in the group
  ##
  ## https://en.wikipedia.org/wiki/Jaccard_index
  groups = group_similar_words(buckets,
                               min_word_length=4,
                               jaccard_threshold=0.6,
                               shingle_size=2,
                               normalize_score=False)

  print_scores_and_groups(groups,lower_threshold=0.1)

  return


if __name__ == '__main__':

  main()

