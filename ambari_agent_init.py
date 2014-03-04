#! /usr/bin/env python
import ConfigParser

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('/etc/ambari-agent/conf/ambari-agent.ini')
    if not config.has_option('agent', 'hostname_script'):
        config.set('agent', 'hostname_script', 'hostname')
        with open('test.ini', 'wb') as f:
            config.write(f)
