# Created by zhouwang on 2021/1/11.
from rest_framework.views import APIView
from ..handlers.tree import Tree
from ..utils.request import with_request


class Node(APIView):
    @with_request(auth=True)
    def post(self, request, *args, **kwargs):
        data = Tree(request.user).create_node(request.data)
        return data

    @with_request(auth=True)
    def put(self, request, *args, **kwargs):
        node = kwargs.get('node')
        data = Tree(request.user).update_node(node, request.data)
        return data

    @with_request(auth=True)
    def delete(self, request, *args, **kwargs):
        node = kwargs.get('node')
        data = Tree(request.user).delete_node(node)
        return data


class NodeUsers(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        node = kwargs.get('node')
        data = Tree(request.user).get_node_users(node)
        return data

    @with_request(auth=True)
    def put(self, request, *args, **kwargs):
        node = kwargs.get('node')
        data = Tree(request.user).update_node_users(node, request.data)
        return data


class NodeUserRole(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        data = Tree(request.user).get_node_user_role(request.query_params)
        return data


class NodeChildren(APIView):
    @with_request(auth=True)
    def get(self, request, *args, **kwargs):
        data = Tree(request.user).get_node_children(request.query_params)
        return data
