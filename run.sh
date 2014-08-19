#!/bin/bash

elastic=elasticsearch-1.3.2
logstash=logstash-1.4.2
templates="./$elastic/config/templates"

if [ ! -d "$templates" ]; then
  mkdir $templates;
fi

if [ -f $templates/wiki.json ]; then
  rm $templates/wiki.json;
fi

cd $templates 
ln -s ../../../wiki.json wiki.json
cd -

./$elastic/bin/elasticsearch -d
./$logstash/bin/logstash -f logstash.conf 2>&1 > /dev/null &


