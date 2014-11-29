#!/bin/bash

wiki=$(<'./templates/wiki_1.json')
echo $wiki
curl -XPUT 'http://localhost:9200/_template/wiki_1' -d "$wiki"
echo $?

