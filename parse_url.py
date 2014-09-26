#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


SHINGLE_SIZE = 2
JACCARD_THRESHOLD = 0.6

db_iso = 'iso-8859-1'


def visible(element):

    import re

    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def parse_html(html):

  from BeautifulSoup import BeautifulSoup
  soup = BeautifulSoup(html)
  texts = soup.findAll(text=True)

  visible_texts = filter(visible, texts)

  txt = ''
  for t in visible_texts:
    txt += t

  return txt


def get_url(url):

  import urllib2

  opener = urllib2.build_opener()
  opener.addheaders = [('Accept-Charset', db_iso)]
  url_response = opener.open(url)
  deal_html = url_response.read()
  deal_html_unicode = deal_html.decode(db_iso)

  #print deal_html_unicode

  return deal_html_unicode


def main():

  import settings
  from elasticsearch import Elasticsearch

  from get_tags import get_query, group_similar_words, JACCARD_THRESHOLD,\
    SHINGLE_SIZE, print_matching_docs, print_scores_and_groups

  index = settings.index
  doc_type = settings.doc_type

  es = Elasticsearch(host=settings.es_host,port=settings.es_port)


  if not len(sys.argv) == 2:
    print
    print 'parse_url.py http://google.com'
    print
    sys.exit(1)

  url = sys.argv[1]
  try:
    html = get_url(url)
  except ValueError, e:
    print
    print e
    print

  txt = parse_html(html)

  qry = get_query(txt)
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






if __name__ == '__main__':

  main()

