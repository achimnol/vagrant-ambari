#! /usr/bin/env python
import sys
import ConfigParser

ambari_conf = '/etc/ambari-agent/conf/ambari-agent.ini'
config = ConfigParser.RawConfigParser()
config.read(ambari_conf)
if not config.has_option('agent', 'hostname_script'):
    config.set('agent', 'hostname_script', 'hostname')
if len(sys.argv) > 1 and sys.argv[1]:
    config.set('server', 'hostname', sys.argv[1])
with open(ambari_conf, 'wb') as f:
    config.write(f)
