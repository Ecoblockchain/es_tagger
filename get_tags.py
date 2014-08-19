#!/usr/bin/python
# -*- coding: utf-8 -*-


SHINGLE_SIZE = 2
JACCARD_THRESHOLD = 0.6


def get_similar_words(all_words,jaccard_threshold,shingle_size):

  from collections import defaultdict

  def get_shingles(word, size=shingle_size):

    shingles = set()
    word = ' ' + word.strip()
    for i in range(0, len(word)-size+1):
      yield word[i:i+size]

  def jaccard(set1, set2):

    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)

  all_shingle_sets = []
  for w in all_words:
    all_shingle_sets.append(set(get_shingles(w)))

  res = defaultdict(set)
  used = set()
  n_shingle_sets = len(all_shingle_sets)

  for i in xrange(n_shingle_sets):
    a = all_shingle_sets[i]
    wa = all_words[i]

    if wa in used:
      continue

    res[wa].update([wa])
    used.update([wa])

    for j in xrange(n_shingle_sets):
      b = all_shingle_sets[j]
      wb = all_words[j]

      if wb in used:
        continue

      if jaccard(a,b)>jaccard_threshold:
        res[wa].update([wb])
        used.update([wb])

  return res

def group_similar_words(buckets,
                        min_word_length,
                        jaccard_threshold,
                        shingle_size):

  all_words = []
  all_words_score = {}

  for i,v in enumerate(buckets):

    w = v['key']
    if len(w)>min_word_length-1:
      all_words.append(w)
      all_words_score[w] = v['score']

  words_words= get_similar_words(all_words,jaccard_threshold,shingle_size)

  res = []
  global_top_score = -1.

  for ww in words_words.values():

    top_score = max([all_words_score[w] for w in ww])
    global_top_score = max((global_top_score,top_score))
    res.append((ww,top_score))

  global_top_score = float(global_top_score)
  scaled_res = []
  for ww,s in res:
    scaled_res.append((ww,s/global_top_score))

  return scaled_res

def get_query(like_text):

  #qry = {
    #'query': {
      #'more_like_this': {
        #'fields': ['text'],
        #'like_text': like_text,
        #'min_term_freq': 2,
        #'max_query_terms': 15,
        #'min_word_length': 3,
      #}
    #},
    #'aggs': {
      #'my_tags': {
        #'significant_terms': {
          #'field': 'text.text_tags',
          #'size': 20,
          #'min_doc_count': 3
        #}
      #}
    #}
  #}

  qry = {
    'query': {
      'filtered': {
        'query' : {
          'more_like_this' : {
            'fields' : ['text'],
            'like_text' : like_text,
            'min_term_freq': 2,
            'max_query_terms': 15,
            'min_word_length': 3,
          }
        },
        'filter': {
          'bool':{
            'must_not':{
              'terms' :{
                'title.title_simple':[
                  'fil','mal','wikipedia','kategori'
                ]
              }
            }
          }
        }
      }
    },
    'aggs' : {
      'my_tags' : {
        'significant_terms' : {
          'field' : 'text.text_tags',
          'size': 100,
          'min_doc_count': 3
        }
      }
    }
  }

  return qry


def main():

  import settings
  import sys

  from elasticsearch import Elasticsearch


  def print_matching_docs(hits):

    for h in hits:
      source = h['_source']
      print '{:.2f}\t'.format(h['_score']),source['title']

    return

  def print_scores_and_groups(groups,lower_threshold):

    from operator import itemgetter

    groups = reversed(sorted(groups,key=itemgetter(1)))

    for ww,s in groups:

      if s>lower_threshold:
        print '{:.2f}\t'.format(s),
        for w in ww:
          print w,

        print

    return


  index = settings.index
  doc_type = settings.doc_type

  es = Elasticsearch(host=settings.es_host,port=settings.es_port)


  while True:

    print
    print 'input document:'
    print

    try:
      data = str(sys.stdin.read())
      print
    except Exception as e:
      data = ''

    if data.strip():

      qry = get_query(data)
      res = es.search(index=index,doc_type=doc_type,body=qry)
      buckets = res['aggregations']['my_tags']['buckets']
      groups = group_similar_words(buckets,
                                   min_word_length=4,
                                   jaccard_threshold=JACCARD_THRESHOLD,
                                   shingle_size=SHINGLE_SIZE)

      print
      print
      hits = res['hits']['hits']
      print_matching_docs(hits)
      print
      print
      print_scores_and_groups(groups,lower_threshold=0.25)

  return


if __name__ == '__main__':

  main()

