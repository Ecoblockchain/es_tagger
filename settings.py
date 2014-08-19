#!/usr/bin/python
# -*- coding: utf-8 -*-

redis_host = '127.0.0.1'
redis_port = 6379
redis_list = 'wiki_stream'

es_port = 9200
es_host = 'localhost'

xml_data = '/data/nowiki-latest-pages-articles-multistream.xml'
#xml_data = '/data/test.xml'

index = 'wiki'
doc_type = 'wiki'

xml_namespace = 'http://www.mediawiki.org/xml/export-0.8/'

