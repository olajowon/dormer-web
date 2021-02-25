# Created by zhouwang on 2021/2/8.
from django.db import transaction
from .. import models
from ..utils import tree as tree_utils
from ..utils.exception import ForbiddenError, NotFoundError


class Screen:
    def __init__(self, requser=None):
        self.requser = requser

    def get_screen_dashboard(self, path):
        mdl = models.TreeNode.objects.filter(path=path, type='screen').first()
        if not mdl:
            raise NotFoundError('Screen不存在')
        role = tree_utils.get_node_user_role(mdl, self.requser)
        if not role:
            raise ForbiddenError('没有查看[%s]权限' % path)
        return {'results': {
            'role': role,
            'settings': mdl.settings
        }}

    def update_screen_settings(self, path, settings):
        nodel_mdl = models.TreeNode.objects.filter(path=path, type='screen').first()
        with transaction.atomic():
            nodel_mdl.settings = settings
            nodel_mdl.save()
            models.History.objects.create(
                action='update_screen_settings',
                data={
                    'id': nodel_mdl.id,
                    'screen_settings': nodel_mdl.settings
                },
                action_user=self.requser.username
            )
        return {'results': nodel_mdl.settings}
