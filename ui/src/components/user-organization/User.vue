<template>
  <b-row :key="this.$route.params.root" class="h-100">
    <b-col cols="12" sm="5" md="3" style="max-height: 100%">
      <Tree v-bind:space="space" v-bind:root="this.$route.params.root"/>
      <div class="d-none d-sm-block user-tree-border"></div>
    </b-col>
    <b-col cols="12" sm="7" md="9" style="max-height: 100%">
      <Screen v-if="this.$route.query.type == 'screen'" ref='userScreen'/>
      <Screen v-else-if="this.$route.query.type == 'alarm'" />
    </b-col>
  </b-row>
</template>

<script>
  import Tree from '@/components/user-organization/Tree'
  import Screen from '@/components/user-organization/Screen'

  export default {
    name: 'User',
    components: {
      Tree: Tree,
      Screen: Screen
    },
    data() {
      return {
        space: "user",
      }
    },

    computed: {
    },

    mounted() {
    },

    methods: {
      refresh() {
        this.$refs.userScreen.refresh();
      }
    }
  }
</script>
<style>
  .user-tree-border {
    height: 100% !important;
    border-right: 1px solid rgba(0, 0, 0, 0.125) !important;
    position: absolute !important;
    right: 0px !important;
    top: 0px !important;
  }
</style>
