#! /usr/bin/env python
import ConfigParser

ambari_conf = '/etc/ambari-agent/conf/ambari-agent.ini'
config = ConfigParser.RawConfigParser()
config.read(ambari_conf)
if not config.has_option('agent', 'hostname_script'):
    config.set('agent', 'hostname_script', 'hostname')
config.set('server', 'hostname', 'master')
with open(ambari_conf, 'wb') as f:
    config.write(f)
