# Created by zhouwang on 2020/12/19.
from ..utils import db


class Common:
    def render(self, params):
        params = {
            'target': params.getlist('target'),
            'from': params.get('from'),
            'until': params.get('until'),
            'format': params.get('format') or 'json'
        }
        return db.GraphiteApi().render(params)