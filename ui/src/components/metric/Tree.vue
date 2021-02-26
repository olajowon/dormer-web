<template>
  <ul id="metricTree" class="ztree"></ul>
</template>

<script>
  export default {
    name: 'Tree',
    data() {
      return {
        setting: {
          data: {
            simpleData: {
              enable: true
            }
          },
          async: {
            enable: true,
            url: "/api/v1/metric/metric_children/",
            type: "get",
            autoParam: ["id=name"],
            dataFilter: this.treeNodeDataFilter,
            headers: {
              Authorization: localStorage.getItem("jwt")
            }
          },
          callback: {
            beforeClick: this.treeNodeBeforeClick,
            onAsyncSuccess: this.treeNodeOnAsyncSuccess,
          }
        },
        tree: null,
      }
    },

    watch: {
      "$route.query": function (n, o) {
        if (n.name != o.name) {
          let node = this.tree.getNodeByParam('id', n.name)
          if (node) {
            this.tree.selectNode(node);
          }
        }
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
        this.tree = $.fn.zTree.init($("#metricTree"), this.setting, []);
      },

      treeNodeBeforeClick(treeId, treeNode) {
        if (treeNode.id != this.$route.query.name) {
          let toQuery = this.merge(this.$route.query, {name: treeNode.id, leaf: treeNode.leaf, keyword: undefined});
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
            if (!parentNode && resp.data.results[i].name != this.category) {
              continue
            }

            let icon = resp.data.results[i].leaf == 0 ? "folder" : "leaf"
            data.push({
              id: resp.data.results[i].name,
              name: resp.data.results[i].text,
              isParent: resp.data.results[i].leaf == 0,
              iconSkin: icon,
              leaf: resp.data.results[i].leaf
            })
          }
        }
        return data;
      },

      treeNodeOnAsyncSuccess(event, treeId, treeNode) {
        let queryMetric = this.$route.query.name || ""
        if (!treeNode) {
          let node = this.tree.getNodeByParam('pId', null)
          this.tree.expandNode(node, true, false, true, true);
        } else {
          if (queryMetric.indexOf(treeNode.id + ".") == 0) {
            let node = this.tree.getNodeByParam('id', queryMetric.split('.').slice(0, treeNode.level + 2).join("."))
            if (node) {
              if (node.isParent && queryMetric.split(".").length > treeNode.level + 2) {
                this.tree.expandNode(node, true, false, true, true);
              } else {
                this.tree.selectNode(node);
              }
            } else {
              this.tree.selectNode(treeNode);
            }
          } else if (treeNode.id == queryMetric) {
            this.tree.selectNode(treeNode);
          }
        }
      }
    },
    props: ["category"]
  }
</script>
<style>
  .folder_ico_close, .folder_ico_open, .leaf_ico_docu {
    background-image: unset !important;
    line-height: 14px !important;
    font-size: 12px !important;
  }

  #metricTree.ztree * {
    font-size: 13px;
  }

  #metricTree.ztree li span.button.folder_ico_close:before {
    content: "\f07b" !important;
    font-family: FontAwesome !important;
  }

  #metricTree.ztree li span.button.folder_ico_open:before {
    content: "\f07c" !important;
    font-family: FontAwesome !important;
  }

  #metricTree.ztree li span.button.leaf_ico_docu:before {
    content: "\f06c" !important;
    font-family: FontAwesome !important;
  }

  #metricTree.ztree li a.curSelectedNode {
    background-color: unset !important;
    border: unset !important;
    color: #19a2b8 !important;
    padding-top: 1px !important;
  }
</style>
