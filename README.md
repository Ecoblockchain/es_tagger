Get Tag Suggestions Using Elasticsearch
=============

This is a very basic example of how you can use Elasticsearch to get tag
suggestions for a text using an XML dump of Wikipedia as your corpus. The code
is specialized for the Norwegian Wikipeda, but you can probably change it with
a fairly minimal effort. 

The code is only a proof of concept/experiment, so there are a lot of things
that need improvement. 

Installing
-----------
To run this you will need a few components:
 - Elasticsearch (download and extract into the repo. ``run.sh`` must be
   corrected with the correct path to the Elasticsearch executable.)
 - Logstash (download and extract into the repo. ``run.sh`` must be corrected
   with the correct path to the Logstash executable.)
 - Python (2.7)
 - Redis (``apt-get install redis-server``)
 - dewiki (``pip install dewiki``)
 - elasticsearch for python (``pip install elasticsearch``)
 - A dump of the Norwegian Wikipedia collection in XML (download from
   ``https://dumps.wikimedia.org/nowiki/latest/``. The file I use is called
   ``nowiki-latest-pages-articles-multistream.xml.bz2``. Put the path to the
   extracted file in ``settings.py``)

Populating the Elasticsearch Index
-----------
First you need to start Logstash and Elasticsearch. To do this run ``run.sh``.

Then you must execute ``redis_stream.py``. This will populate the index.
Parsing the XML requires a fair bit of memory (around 20 GB when I execute it
on my machine.). Redis us used as a message queue here so it will take some
time from ``redis_stream.py`` finishes until ES has index all documents.

Getting Tags
-----------
To get tag suggestions for an arbitrary text you can then start ``get_tags.py``
and past the text into the terminal. Use *Control-D* to execute the tag query.

Questions
-----------
Feel free to ask me any questions you might have, and I will do my best to
answer.

