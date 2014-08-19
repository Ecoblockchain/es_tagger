#!/bin/bash

# add the correct folder names for elasticsearch and logstash: 

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

# start elasticsearch as a daemon
./$elastic/bin/elasticsearch -d

# start logstash as a detached process and dump all
# logs. you probably don't want to do this ...
./$logstash/bin/logstash -f logstash.conf 2>&1 > /dev/null &


