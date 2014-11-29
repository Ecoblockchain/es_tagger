redis-server:
  pkg.installed:
    - name: redis-server 
  service:
    - running
    - enable: True
    - watch:
      - pkg: redis-server
