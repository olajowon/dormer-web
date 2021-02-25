# Created by zhouwang on 2020/11/12.

import os
import configparser

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'env')

try:
    env = open(path, 'r+').read().strip()
except Exception as e:
    print(e)
    env = 'development'

cf = configparser.ConfigParser()
cf.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '%s.ini' % env))

db = {
    'name': cf.get('db', 'name'),
    'user': cf.get('db', 'user'),
    'password': cf.get('db', 'password'),
    'host': cf.get('db', 'host'),
    'port': cf.get('db', 'port'),
}

elasticsearch = {
    'hosts': [{'host': hp.split(':')[0], 'port': hp.split(':')[1]}
              for hp in cf.get('elasticsearch', 'hosts').split(',')],
    'index': cf.get('elasticsearch', 'index')
}

graphite_api = {
    'host': cf.get('graphite_api', 'host'),
}

tdengine = {
    'host': cf.get('tdengine', 'host'),
    'user': cf.get('tdengine', 'user'),
    'password': cf.get('tdengine', 'password'),
    'database': cf.get('tdengine', 'database')
}

ldap = {
    'server_uri': cf.get('ldap', 'server_uri'),
    'bind_dn': cf.get('ldap', 'bind_dn'),
    'bind_password': cf.get('ldap', 'bind_password'),
    'base_dn': cf.get('ldap', 'base_dn'),
    'search_field': cf.get('ldap', 'search_field'),
}

extend = {sec['name']: dict(sec.items()) for k, sec in cf.items() if k.startswith('extend')}
