
def get_tag_query(txt):

  ## the must_not entries are included because the dataset from wikipedia
  ## contains quite a lot of metadata entries that we don't want included
  ## in the result set

  q = {
    'size': 100,
    'from':0,
    'fields': [
      'title'
    ],
    'query': {
      'filtered': {
        'query': {
          'more_like_this': {
            'fields': ['text.myStandard_nor'],
            'like_text': txt,
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
          'min_doc_count': 3,
          #'gnd': {}
        }
      }
    }
  }

  return q

