#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

def print_matching_docs(hits):

  for h in hits:
    source = h['_source']
    score = '{:.2f}\t'.format(h['_score'])
    print(score,source['title'].encode('utf8'))

  return

def print_scores_and_groups(groups,lower_threshold):

  from operator import itemgetter

  groups = reversed(sorted(groups,key=itemgetter(1)))

  for ww,s in groups:

    if s>lower_threshold:
      score = '{:.2f}\t'.format(s)
      print(score,' '.join(ww).encode('utf8')),

  return

