Get Tag Suggestions Using Elasticsearch
=============

This is a very basic example of how you can use Elasticsearch to get tag
suggestions for a text using an XML dump of Wikipedia as your corpus. The code
is specialized for the Norwegian Wikipeda, but you can probably change it with
a fairly minimal effort. 

The code is only a proof of concept/experiment, so there are a lot of things
that needs to be improved.


Utilities
-----------
This repo uses a number of utilities and resources:

 - Vagrant
 - Elasticsearch (installed via Vagrant)
 - Logstash (via Vagrant)
 - Python (via Vagrant)
 - Redis (via Vagrant)
 - Dewiki (via Vagrant)
 - Python-elasticsearch (via Vagrant)
 - An XML dump of the Norwegian Wikipedia collection (via ``get_wiki_data.sh``)


Starting
-----------
1. Start the vagrant image:
    ```
    vagrant up
    ```

2. Ssh into the vagrant box:
    ```
    vagrant ssh
    ```

3. Navigate to
    ```
    cd /vagrant
    ```

4. Get wikipedia data:
    ```
    ./get_wiki_data.sh
    ```
5. Check that the value assigned to ``xml_namespace`` in ``settings.py``
   matches the namespace in ``./wiki_data/wiki.xml``

6. Index the wikipedia data (This is slow. Go get a coffee):
    ```
    ./redis_es_stream.py
    ```

Getting Tags
-----------
To get tag suggestions for an arbitrary text you can then start ``tags.py`` and
paste the text into the terminal. Use *Ctrl^D* to execute the tag query.
Sometimes you have to press Ctrl^d twice.

