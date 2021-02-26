# Created by zhouwang on 2021/1/11.
from django.db import transaction
from .. import models
from django.contrib.auth import models as auth_models
from ..utils.exception import ParamError, ForbiddenError, NotFoundError
from ..utils import tree as tree_utils
from .. import serializers
import re


class Tree:
    def __init__(self, requser=None):
        self.requser = requser

    def create_node(self, data):
        cleaned = self.clean_create_node_data(data)
        with transaction.atomic():
            mdl = models.TreeNode.objects.create(
                path=cleaned['path'],
                text=cleaned['text'],
                type=cleaned['type'],
                space=cleaned['space'],
            )

            models.History.objects.create(
                action='create_tree_node',
                data={
                    'id': mdl.id,
                    'tree_node': serializers.Serializer(mdl).data
                },
                action_user=self.requser.username
            )
        return {'result': self.make_node_data(mdl)}

    def clean_create_node_data(self, data):
        path = data.get('path')
        tp = data.get('type')
        text = path.split('.')[-1]

        if not path or path.find('.') == -1 or not re.match('^[-\u4e00-\u9fa5_a-zA-Z0-9]+$', text):
            raise ParamError('path', '节点路径格式无效，节点名称由[中文、英文、数字、_、-]组成')

        parent_path = '.'.join(path.split('.')[:-1])
        parent_mdl = models.TreeNode.objects.filter(path=parent_path, type='branch').first()
        if not parent_mdl:
            raise ParamError('path', '节点[%s]不存在或类型不是分支' % parent_path)

        role = tree_utils.get_node_user_role(parent_mdl, self.requser)
        if not role['owner']:
            raise ForbiddenError('没有添加权限')

        node_mdl = models.TreeNode.objects.filter(path=path).first()
        if node_mdl:
            raise ParamError('path', '节点已存在')

        if tp not in ('branch', 'screen', 'alarm'):
            raise ParamError('type', '节点类型不支持')

        return {
            'path': path,
            'text': text,
            'type': tp,
            'space': parent_mdl.space,
        }

    def update_node(self, node, data):
        update_mdl = models.TreeNode.objects.filter(path=node).first()
        if not update_mdl:
            raise NotFoundError('节点不存在')

        cleaned = self.clean_update_node_data(update_mdl, data)
        if cleaned['path'] != update_mdl.path:
            with transaction.atomic():
                if update_mdl.type == 'branch':
                    child_qs = models.TreeNode.objects.filter(
                        path__startswith='%s.' % update_mdl.path).values('id', 'path')
                    for child_mdl in child_qs:
                        models.TreeNode.objects.filter(
                            id=child_mdl['id']
                        ).update(path=cleaned['path'] + child_mdl['path'][len(update_mdl.path):])

                update_mdl.path = cleaned['path']
                update_mdl.text = cleaned['text']
                update_mdl.save()

                models.History.objects.create(
                    action='update_tree_node',
                    data={
                        'id': update_mdl.id,
                        'tree_node': serializers.Serializer(update_mdl).data
                    },
                    action_user=self.requser.username
                )
        return {'result': self.make_node_data(update_mdl)}

    def clean_update_node_data(self, update_mdl, data):
        if update_mdl.path.find('.') == -1:
            raise ForbiddenError('不允许修改根节点')
        role = tree_utils.get_node_user_role(update_mdl, self.requser)
        if not role['owner']:
            raise ForbiddenError('没有修改权限')

        path = data.get('path')
        text = path.split('.')[-1]
        if not path or path.find('.') == -1 or not re.match('^[-\u4e00-\u9fa5_a-zA-Z0-9]+$', text):
            raise ParamError('path', '节点路径格式无效，节点名称由[中文、英文、数字、_、-]组成')

        if models.TreeNode.objects.filter(path=path).exclude(id=update_mdl.id).count():
            raise ParamError('path', '节点[%s]已存在' % path)

        if path != update_mdl.path:
            parent_path = '.'.join(path.split('.')[:-1])
            if parent_path != update_mdl.path.split('.')[:-1]:
                parent_mdl = models.TreeNode.objects.filter(path=parent_path, type='branch').first()
                if not parent_mdl:
                    raise ParamError('path', '节点[%s]不存在或类型不是分支' % parent_path)

                role = tree_utils.get_node_user_role(parent_mdl, self.requser)
                if not role['owner']:
                    raise ForbiddenError('没有[%s]权限' % parent_mdl.path)
        return {
            'path': path,
            'text': text
        }

    def delete_node(self, node):
        node_mdl = models.TreeNode.objects.filter(path=node).first()
        if not node_mdl:
            raise NotFoundError('节点不存在')
        if node_mdl.path.find('.') == -1:
            raise ForbiddenError('不允许删除根节点')
        role = tree_utils.get_node_user_role(node_mdl, self.requser)
        if not role['owner']:
            raise ForbiddenError('没有删除权限')
        child_cnt = models.TreeNode.objects.filter(path__startswith='%s.' % node_mdl.path).count()
        if child_cnt:
            raise ForbiddenError('存在子节点，不允许删除')

        with transaction.atomic():
            models.History.objects.create(
                action='delete_tree_node',
                data={
                    'id': node_mdl.id,
                    'tree_node': serializers.Serializer(node_mdl).data
                },
                action_user=self.requser.username
            )
            node_mdl.delete()
        return {'result': self.make_node_data(node_mdl)}

    def get_node_users(self, node):
        node_mdl = models.TreeNode.objects.filter(path=node).first()
        if not node_mdl:
            raise NotFoundError('节点不存在')
        role = tree_utils.get_node_user_role(node_mdl, self.requser)
        if not role['owner'] and not role['viewer']:
            raise ForbiddenError('没有[%s]权限' % node_mdl.path)
        return {
            'results': {
                'owners': [o.username for o in node_mdl.owners.all()],
                'viewers': [v.username for v in node_mdl.viewers.all()],
            }
        }

    def update_node_users(self, node, data):
        node_mdl = models.TreeNode.objects.filter(path=node).first()
        if not node_mdl:
            raise NotFoundError('节点不存在')
        cleaned = self.clean_update_node_users_data(node_mdl, data)
        new_owners = [o.username for o in cleaned['owners']]
        new_viewers = [v.username for v in cleaned['viewers']]
        old_owners = [o.username for o in node_mdl.owners.all()]
        old_viewers = [v.username for v in node_mdl.viewers.all()]

        with transaction.atomic():
            if not (set(new_owners) & set(old_owners) == set(new_owners) == set(old_owners)):
                node_mdl.owners.clear()
                node_mdl.owners.add(*cleaned['owners'])

            if not (set(new_viewers) & set(old_viewers) == set(new_viewers) == set(old_viewers)):
                node_mdl.viewers.clear()
                node_mdl.viewers.add(*cleaned['viewers'])

            models.History.objects.create(
                action='update_tree_node_users',
                data={
                    'id': node_mdl.id,
                    'tree_node_owners': new_owners,
                    'tree_node_viewers': new_viewers
                },
                action_user=self.requser.username
            )
        return {'results': {'owners': new_owners, 'viewers': new_viewers}}

    def clean_update_node_users_data(self, node_mdl, data):
        if node_mdl.space == 'user':
            raise ForbiddenError('节点不允许设置用户')

        role = tree_utils.get_node_user_role(node_mdl, self.requser)
        if not role['owner']:
            raise ForbiddenError('没有[%s]权限' % node_mdl.path)

        owners = data.get('owners', [])
        viewers = data.get('viewers', [])
        owner_qs = auth_models.User.objects.filter(username__in=owners)
        viewer_qs = auth_models.User.objects.filter(username__in=viewers)

        return {'owners': owner_qs, 'viewers': viewer_qs}

    def get_node_user_role(self, params):
        path = params.get('path')
        node_mdl = models.TreeNode.objects.filter(path=path).first()
        if not node_mdl:
            raise NotFoundError('节点不存在')
        role = tree_utils.get_node_user_role(node_mdl, self.requser)
        return {'result': role}

    @staticmethod
    def make_node_data(mdl):
        return {
            'path': mdl.path,
            'text': mdl.text,
            'type': mdl.type,
            'space': mdl.space,
        }

    def get_node_children(self, params):
        path = params.get('path', '')
        space = params.get('space', 'user')
        root = params.get('root')   # space == user

        if space == 'user' and root:
            node_qs = []
            root_mdl = models.TreeNode.objects.filter(path=root, space=space).first()
            if not root_mdl and root == self.requser.username:
                with transaction.atomic():
                    root_mdl = models.TreeNode.objects.create(path=root, text=root, space=space)
                    root_mdl.owners.add(self.requser)

            if root_mdl:
                role = tree_utils.get_node_user_role(root_mdl, self.requser, keys=['viewer'])
                if role['viewer']:
                    if not path:
                        node_qs = models.TreeNode.objects.filter(
                            path=root,
                            space=space
                        ).order_by('path')
                    elif path.split('.')[0] == root:
                        node_qs = models.TreeNode.objects.filter(
                            path__regex='^%s$' % '.'.join([path, '[-\u4e00-\u9fa5_a-zA-Z0-9]*']),
                            space=space
                        ).order_by('path')
        elif space == 'organization':
            node_qs = models.TreeNode.objects.filter(
                path__regex='^%s$' % '.'.join([path, '[-\u4e00-\u9fa5_a-zA-Z0-9]*']),
                space=space
            ).order_by('path')

        children = []
        for mdl in node_qs:
            children.append({
                'path': mdl.path,
                'text': mdl.text,
                'type': mdl.type,
                'space': mdl.space
            })
        return {'results': children}
