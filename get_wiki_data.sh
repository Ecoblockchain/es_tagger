#!/bin/bash

wiki_data_url="https://dumps.wikimedia.org/nowiki/latest/nowiki-latest-pages-articles-multistream.xml.bz2";
wiki_data="./wiki_data";

if [ ! -d "$wiki_data" ]; then
  mkdir $wiki_data;
fi

cd $wiki_data;

curl $wiki_data_url | bzip2 -d > wiki.xml

