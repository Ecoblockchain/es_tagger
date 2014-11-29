#!/bin/bash

curl -XDELETE 'http://localhost:9200/_template/wiki*'
echo $?
