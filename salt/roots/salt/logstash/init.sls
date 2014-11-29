# Include the ``java`` sls in order to use oracle_java_pkg
include:
    - jdk7

# Note: this is only valid for the Debian repo / package
# You should filter on grain['os'] conditional for yum-based distros
logstash_repo:
    pkgrepo.managed:
        - humanname: Logstash Official Debian Repository
        - name: deb http://packages.elasticsearch.org/logstash/1.4/debian stable main
        - dist: stable
        - key_url: salt://logstash/GPG-KEY-elasticsearch
        - file: /etc/apt/sources.list.d/logstash.list

logstash:
    pkg:
        - installed
        - require:
            - pkg: oracle-java7-installer
            - pkgrepo: logstash_repo
            - service: redis-server
    service:
        - running
        - enable: True
        - require:
            - pkg: logstash
            - file: /etc/logstash/conf.d/logstash.conf

/etc/logstash/conf.d/logstash.conf:
    file.managed:
        - source: salt://logstash/logstash.conf
        - user: root
        - group: root
        - mode: 644
        - makedirs: True
