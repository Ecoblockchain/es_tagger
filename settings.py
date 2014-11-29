#!/usr/bin/python
# -*- coding: utf-8 -*-

redis_host = '127.0.0.1'
redis_port = 6379
redis_list = 'wiki_stream'

es_port = 9200
es_host = 'localhost'

xml_data = './wiki_data/wiki.xml'

index = 'wiki'
doc_type = 'wiki'

## NOTICE: this variable seems to change quite often. check wiki.xml for the
## correct version:

xml_namespace = 'http://www.mediawiki.org/xml/export-0.9/'

