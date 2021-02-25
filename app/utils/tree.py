# Created by zhouwang on 2021/1/30.
from .. import models


def get_node_user_role(node_mdl, user_mdl, keys=[]):
    keys = keys or ['owner', 'viewer']

    role = {p: False for p in keys}

    if node_mdl.space == 'user':
        if node_mdl.path.find('.') > -1:
            node_mdl = models.TreeNode.objects.get(path=node_mdl.path.split('.')[0])

    if 'owner' in role:
        role['owner'] = bool(node_mdl.owners.filter(username=user_mdl.username))
    if 'viewer' in role:
        if role.get('owner'):
            role['viewer'] = True
        elif role.get('owner') is None:
            role['viewer'] = bool(node_mdl.owners.filter(username=user_mdl.username)) or \
                             bool(node_mdl.viewers.filter(username=user_mdl.username))
        else:
            role['viewer'] = bool(node_mdl.viewers.filter(username=user_mdl.username))

    if node_mdl.space == 'organization' and not all(role.values()):
        nodes = node_mdl.path.split('.')
        for idx in range(len(nodes) - 1):
            path = '.'.join(nodes[0: idx+1])
            if 'owner' in role and not role['owner']:
                role['owner'] = bool(models.TreeNode.objects.filter(path=path, owners=user_mdl).first())
            if 'viewer' in role and not role['viewer']:
                if role.get('owner'):
                    role['viewer'] = True
                elif role.get('owner') is None:
                    role['viewer'] = bool(models.TreeNode.objects.filter(path=path, owners=user_mdl).first()) or \
                                     bool(models.TreeNode.objects.filter(path=path, viewers=user_mdl).first())
                else:
                    role['viewer'] = bool(models.TreeNode.objects.filter(path=path, viewers=user_mdl).first())

            if all(role.values()):
                break
    return role
