<template>
  <b-row class="h-100">
    <b-col cols="12" sm="5" md="3" style="max-height: 100%">
      <Tree v-bind:space="space" />
      <div class="d-none d-sm-block org-tree-border"></div>
    </b-col>
    <b-col cols="12" sm="7" md="9" style="max-height: 100%">
      <Screen v-if="this.$route.query.type == 'screen'" ref='organizationScreen'/>
      <Screen v-else-if="this.$route.query.type == 'alarm'" />
    </b-col>
  </b-row>
</template>

<script>
  import Tree from '@/components/user-organization/Tree'
  import Screen from '@/components/user-organization/Screen'

  export default {
    name: 'Organization',
    components: {
      Tree: Tree,
      Screen: Screen
    },
    data() {
      return {
        space: "organization"
      }
    },
    mounted() {
    },

    methods: {
      refresh() {
        this.$refs.organizationScreen.refresh();
      }
    }
  }
</script>
<style>
  .org-tree-border {
    height: 100%;
    border-right: 1px solid rgba(0, 0, 0, 0.125);
    position: absolute; right: 0px;
    top: 0px
  }
</style>
