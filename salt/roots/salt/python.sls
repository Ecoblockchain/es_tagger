python:
  pkg.installed:
    - names:
      - python
      - python-dev
      - python-virtualenv

python-lxml:
  pkg.installed:
    - names:
      - python-lxml

python-pip:
  pkg.installed:
    - names:
      - python-pip

python-elasticsearch:
  pip.installed:
    - name: elasticsearch
    - require:
      - pkg: python-pip

python-redis:
  pip.installed:
    - name: redis 
    - require:
      - pkg: python-pip

python-dewiki:
  pip.installed:
    - name: dewiki 
    - require:
      - pkg: python-pip
      - pkg: python-lxml

python_path:
  file.append:
    - name: /etc/environment
    - text: PYTHONPATH=/vagrant/python_modules/

