<template>
  <div>
    <div v-if="role.owner" class="tree-options">
      <b-button
        :disabled="!selectedTreeNode || selectedTreeNode.type != 'branch'"
        @click="onCreateTreeNodeBtnClick"
        size="mini"
        variant="success">
        <i class="fa fa-plus fa-fw" aria-hidden="true" ></i>
      </b-button>
      <b-button
        :disabled="!selectedTreeNode || (space == 'user' && selectedTreeNode.level == 0)"
        @click="onUpdateTreeNodeBtnClick"
        size="mini" variant="warning">
        <i class="fa fa-pencil fa-fw" aria-hidden="true" ></i>
      </b-button>
      <b-button
        :disabled="!selectedTreeNode || selectedTreeNode.level == 0 || selectedTreeNode.check_Child_State > -1"
        @click="onDeleteTreeNodeBtnClick"
        size="mini"
        variant="danger">
        <i class="fa fa-trash-o fa-fw" aria-hidden="true" ></i>
      </b-button>
      <b-button
        :disabled="!selectedTreeNode || (space == 'user' && selectedTreeNode.level != 0)"
        @click="onUpdateTreeNodeUserBtnClick"
        size="mini"
        variant="info">
        <i class="fa fa-users fa-fw" aria-hidden="true" ></i>
      </b-button>
    </div>

    <ul id="userOrgTree" class="ztree"></ul>


    <TreeNodeCreateModal
      v-if="createTreeNodeModalShow"
      v-bind:parentNode.sync="selectedTreeNode"
      v-bind:show.sync="createTreeNodeModalShow"/>

    <TreeNodeUpdateModal
      v-if="updateTreeNodeModalShow"
      v-bind:node.sync="selectedTreeNode"
      v-bind:show.sync="updateTreeNodeModalShow"/>

    <TreeNodeUserUpdateModal
      v-if="updateTreeNodeUserModalShow"
      v-bind:node.sync="selectedTreeNode"
      v-bind:show.sync="updateTreeNodeUserModalShow"/>
  </div>
</template>

<script>
  import TreeNodeCreateModal from '@/components/user-organization/modal/TreeNodeCreateModal'
  import TreeNodeUpdateModal from '@/components/user-organization/modal/TreeNodeUpdateModal'
  import TreeNodeUserUpdateModal from '@/components/user-organization/modal/TreeNodeUserUpdateModal'

  export default {
    name: 'Tree',
    components: {
      TreeNodeCreateModal: TreeNodeCreateModal,
      TreeNodeUpdateModal: TreeNodeUpdateModal,
      TreeNodeUserUpdateModal: TreeNodeUserUpdateModal
    },
    data() {
      return {
        setting: {
          data: {
            simpleData: {
              enable: true
            },
            keep: {
              parent: true
            }
          },
          async: {
            enable: true,
            url: "/api/v1/tree/node_children/",
            type: "get",
            autoParam: ["path=path"],
            dataFilter: this.treeNodeDataFilter,
            headers: {
              Authorization: localStorage.getItem("jwt")
            },
            otherParam: {
              space: this.space,
              root: this.root
            }
          },
          callback: {
            beforeClick: this.treeNodeBeforeClick,
            onAsyncSuccess: this.treeNodeOnAsyncSuccess,
          }
        },
        tree: null,
        selectedTreeNode: null,

        role: {
          owner: null,
          viewer: null
        },

        createTreeNodeModalShow: false,
        updateTreeNodeModalShow: false,
        updateTreeNodeUserModalShow: false
      }
    },

    watch: {
      "$route.query": function (n, o) {
        if (n.path != o.path) {
          let node = this.tree.getNodeByParam('path', n.path)
          if (node) {
            this.tree.selectNode(node);
            this.selectedTreeNode = node;
          } else {
            this.treeInit();
          }
        }
      },

      "selectedTreeNode.id": function(n, o) {
        this.getTreeNodeUserRole(n);
      }
    },

    mounted() {
      this.treeInit();
    },

    beforeDestroy() {
      this.tree && this.tree.destroy();
    },

    methods: {
      treeInit() {
        this.tree && this.tree.destroy();
        this.tree = $.fn.zTree.init($("#userOrgTree"), this.setting, []);
      },

      treeNodeBeforeClick(treeId, treeNode) {
        if (treeNode.path != this.$route.query.path) {
          let toQuery = this.merge(this.$route.query, {path: treeNode.path, type: treeNode.type});
          this.utils.checkQueryFromUntil(toQuery);
          this.utils.checkQueryRefresh(toQuery);
          this.$router.push({
            query: toQuery
          });
        }
        return false
      },

      treeNodeDataFilter(treeId, parentNode, resp) {
        let data = []
        if (resp.data) {
          for (let i = 0; i < resp.data.results.length; i++) {
            let icon = resp.data.results[i].type
            data.push({
              id: resp.data.results[i].path,
              path: resp.data.results[i].path,
              name: resp.data.results[i].text,
              space: resp.data.results[i].space,
              isParent: resp.data.results[i].type == "branch",
              iconSkin: icon,
              type: resp.data.results[i].type
            })
          }
        }
        return data;
      },

      treeNodeOnAsyncSuccess(event, treeId, treeNode) {
        let queryPath = this.$route.query.path || ""
        if (!treeNode) {
          let node = this.tree.getNodeByParam('pId', null)
          this.tree.expandNode(node, true, false, true, true);
        } else {
          if (queryPath.indexOf(treeNode.path + ".") == 0) {
            let node = this.tree.getNodeByParam('path', queryPath.split('.').slice(0, treeNode.level + 2).join("."))
            if (node) {
              if (node.isParent && queryPath.split(".").length > treeNode.level + 2) {
                this.tree.expandNode(node, true, false, true, true);
              } else {
                this.tree.selectNode(node);
                this.selectedTreeNode = node;
              }
            } else {
              this.tree.selectNode(treeNode);
              this.selectedTreeNode = treeNode;
            }
          } else if (treeNode.path == queryPath) {
            this.tree.selectNode(treeNode);
            this.selectedTreeNode = treeNode;
          }
        }
      },

      onCreateTreeNodeBtnClick() {
        this.createTreeNodeModalShow = true;
      },

      onUpdateTreeNodeBtnClick() {
        this.updateTreeNodeModalShow = true;
      },

      onUpdateTreeNodeUserBtnClick() {
        this.updateTreeNodeUserModalShow = true;
      },

      onDeleteTreeNodeBtnClick() {
        let node = this.selectedTreeNode
        this.$bvModal.msgBoxConfirm("确定要删除 " + node.path + " ?", {
          title: '提示',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: '是',
          cancelTitle: '否',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: true
        })
          .then(value => {
            value && this.submitDeleteTreeNode(node);
          })
          .catch(err => {
          })
      },

      submitDeleteTreeNode(node) {
        console.log(node)
        this.axios.delete("/api/v1/tree/nodes/" + node.path + "/")
          .then(response => {
            this.$root.$bvToast.toast("删除成功", {
              title: "提示",
              variant: "success",
              toaster: "b-toaster-top-center",
              solid: true
            })
            this.submitting = false;
            this.tree.removeNode(node);
            this.$router.push({
              query: this.merge(this.$route.query, {path: node.pId, type: "branch"})
            });
          })
          .catch(error => {
            this.submitting = false;
          })
      },

      getTreeNodeUserRole() {
        this.axios.get("/api/v1/tree/node_user_role/", {params: {path: this.selectedTreeNode.id}})
          .then(response => {
            this.role.owner = response.data.data.result.owner;
            this.role.viewer = response.data.data.result.viewer;
          })
          .catch(error => {
            this.role.owner = null;
            this.role.viewer = null;
          })
      }
    },

    props: ["space", "root"]
  }
</script>
<style>
  .branch_ico_close, .branch_ico_open, .alarm_ico_docu, .screen_ico_docu {
    background-image: unset !important;
    line-height: 14px !important;
    font-size: 12px !important;
  }

  #userOrgTree.ztree * {
    font-size: 13px;
  }

  #userOrgTree.ztree li span.button.branch_ico_close:before {
    content: "\f07b" !important;
    font-family: FontAwesome !important;
  }

  #userOrgTree.ztree li span.button.branch_ico_open:before {
    content: "\f07c" !important;
    font-family: FontAwesome !important;
  }

  #userOrgTree.ztree li span.button.alarm_ico_docu:before {
    content: "\f0f3" !important;
    font-family: FontAwesome !important;
  }

  #userOrgTree.ztree li span.button.screen_ico_docu:before {
    content: "\f0e4" !important;
    font-family: FontAwesome !important;
  }

  #userOrgTree.ztree li a.curSelectedNode {
    background-color: unset !important;
    border: unset !important;
    color: #19a2b8 !important;
    padding-top: 1px !important;
  }

  .tree-options {
    margin-bottom: 5px !important;
  }
</style>
