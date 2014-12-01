#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

def get_similar_words(all_words,jaccard_threshold,shingle_size):

  from collections import defaultdict

  def get_shingles(word, size=shingle_size):

    #shingles = set()
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
                        shingle_size,
                        normalize_score=True):

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

    top_score = max([all_words_score[s] for s in ww])
    global_top_score = max((global_top_score,top_score))
    res.append((ww,top_score))

  global_top_score = float(global_top_score)
  if normalize_score:
    def norm(x): return x/global_top_score
  else:
    def norm(x): return x

  scaled_res = []
  for ww,s in res:
    scaled_res.append((ww,norm(s)))

  return scaled_res

