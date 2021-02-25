<template>
  <b-row v-if="this.$route.query.name" class="h-100">
    <b-col cols="12" sm="5" md="3">
      <Tree/>
      <div class="d-none d-sm-block metric-tree-border"></div>
    </b-col>
    <b-col cols="12" sm="7" md="9" class="h-100" style="overflow: auto">
      <Dash ref='metricDash'/>
    </b-col>
  </b-row>
</template>

<script>
  import Tree from '@/components/metric/Tree'
  import Dash from '@/components/metric/Dash'

  export default {
    name: 'Metric',
    components: {
      Tree: Tree,
      Dash: Dash
    },
    data() {
      return {}
    },
    mounted() {},

    methods: {
      refresh() {
        this.$refs.metricDash.refresh();
      }
    }
  }
</script>
<style>
  .metric-tree-border {
    height: 100%;
    border-right: 1px solid rgba(0, 0, 0, 0.125);
    position: absolute; right: 0px;
    top: 0px
  }
</style>
