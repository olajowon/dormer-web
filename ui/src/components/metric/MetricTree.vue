<template>
  <ul id="metricTree" class="ztree"></ul>
</template>

<script>
  export default {
    name: 'MetricTree',
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
            dataFilter: this.treeNodeDataFilter
          },
          callback: {
            beforeClick: this.treeNodeBeforeClick,
            onAsyncSuccess: this.treeNodeOnAsyncSuccess,
          }
        },
        tree: null
      }
    },

    watch: {
      "$route.query": function (n, o) {
        let node = this.tree.getNodeByParam('id', n.name)
        if (node) {
          this.tree.selectNode(node);
        }
      }
    },

    mounted() {
      let metricName = this.$route.query.name;
      this.metricCategory = metricName.split(".")[0];
      this.tree = $.fn.zTree.init($("#metricTree"), this.setting, []);
    },

    methods: {
      treeNodeBeforeClick(treeId, treeNode) {
        this.$router.push({
          query: this.merge(this.$route.query, {name: treeNode.id, leaf: treeNode.leaf, keyword: undefined})
        })
        return false
      },

      treeNodeDataFilter(treeId, parentNode, resp) {
        let data = []
        if (resp.data) {
          for (let i = 0; i < resp.data.results.length; i++) {
            if (!parentNode && resp.data.results[i].name != this.metricCategory) {
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
        console.log(treeNode)
        let queryMetric = this.$route.query.name
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
          }
        }
      }
    }
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
    background-color: unset;
    border: unset;
    color: #19a2b8;
    padding-top: 1px
  }
</style>
