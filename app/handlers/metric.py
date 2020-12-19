# Created by zhouwang on 2020/11/12.
from ..lib import db
import configure


class Metric:

    def get_metric_categories(self):
        body = {
            'query': {
                'term': {
                    'parent': ''
                }
            }
        }
        res = db.Elasticsearch().search(index=configure.elasticsearch['index'], doc_type='_doc', body=body)
        categories = []
        for metric in res.get('hits', {}).get('hits', []):
            categories.append(metric['_source'])
        return {'results': categories}

    def get_metric_children(self, params):
        name = params.get('name') or ''

        body = {
            'query': {
                'term': {
                    'parent': name
                }
            }
        }
        res = db.Elasticsearch().search(index=configure.elasticsearch['index'], doc_type='_doc', body=body)
        children = []
        for metric in res.get('hits', {}).get('hits', []):
            children.append(metric['_source'])
        return {'results': children}

    def get_metric_offsprings(self, params):
        name = params.get('name')
        keyword = params.get('keyword') or '*'
        leaf = int(params.get('leaf'))

        body = {
            'query': {
                'bool': {
                    'filter': [
                        {
                            'regexp': {
                                'name': '%s\\.%s' % (name, keyword.replace('.', '\\.').replace('*', '.*'))
                            }
                        }
                    ]
                }
            }
        }
        if leaf in (0, 1):
            term_leaf = {'term': {'leaf': {'value': leaf}}}
            body['query']['bool']['filter'].append(term_leaf)

        res = db.Elasticsearch().search(index=configure.elasticsearch['index'], doc_type='_doc', body=body)
        offsprings = []
        for metric in res.get('hits', {}).get('hits', []):
            offsprings.append(metric['_source'])
        return {'results': offsprings}

