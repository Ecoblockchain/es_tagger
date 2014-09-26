#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, redis
import lxml.etree as ET
from collections import defaultdict
import dewiki
from random import random
import settings


host = settings.redis_host
port = settings.redis_port
redis_list = settings.redis_list

xml_data = settings.xml_data

namespace = 'http://www.mediawiki.org/xml/export-0.9/'


def remove_namespace(doc, namespace):
  ns = u'{%s}' % namespace
  nsl = len(ns)
  for elem in doc.getiterator():
    if elem.tag.startswith(ns):
      elem.tag = elem.tag[nsl:]


def etree_to_dict(t):
  d = {t.tag: {} if t.attrib else None}
  children = list(t)
  if children:
    dd = defaultdict(list)
    for dc in map(etree_to_dict, children):
      for k, v in dc.iteritems():
        dd[k].append(v)
    d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
  if t.attrib:
    d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
  if t.text:
    text = t.text.strip()
    if children or t.attrib:
      if text:
        d[t.tag]['#text'] = text
    else:
      d[t.tag] = text
  return d

def vividify(as_dict, *arg):

  res = as_dict
  for a in arg:

    try:
      res = res[a]
    except KeyError:
      return u''

  return res

def fast_iter(context, func, args=[], kwargs={}):
  # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
  # Author: Liza Daly
  for event, elem in context:
    func(elem, *args, **kwargs)
    elem.clear()
    while elem.getprevious() is not None:
      del elem.getparent()[0]
  del context

def main():

  dw = dewiki.from_string

  r = redis.StrictRedis(host=host, port=port)

  def process_element(elem):

    ns = lambda x: '{'+namespace+'}'+x

    as_dict = etree_to_dict(elem)[ns('page')]

    # im so sorry ...
    reduced_dict = { 'title': vividify(as_dict,ns('title')),\
                     'text': dw(vividify(as_dict,ns('revision'),
                                         ns('text'),'#text')),\
                     'myid': vividify(as_dict,ns('id')),\
                     '@timestamp': vividify(as_dict,ns('revision'),\
                                            ns('timestamp')),\
                     'comment': vividify(as_dict,ns('revision'),ns('comment')) }

    as_json = json.dumps(reduced_dict)
    r.rpush(redis_list, as_json)

    print reduced_dict['title']


  context=ET.iterparse(xml_data, events=('end',),
                       tag='{'+namespace+'}page')

  fast_iter(context, process_element)


if __name__ == '__main__':

  main()

