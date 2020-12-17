<template>
  <div class="h-100">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Dormer</b-navbar-brand>

      <div style="position: absolute; right: 90px; top: 13px">
        <span v-if="fromDatetime || untilDatetime"
               class="text-light"
               style="display: inline-block; vertical-align: middle; font-size: 14px">
          {{ fromDatetime }} ~ {{ untilDatetime }}
        </span>
        <b-button variant="info" size="sm" v-b-modal.datetime-modal>
          <i class="fa fa-clock-o fa-lg"></i>
        </b-button>
      </div>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown text="指标">
            <b-dropdown-item v-for="(c, idx) in categories" :key="idx" :href="'/#/metric/?name=' + c.name + '&leaf=0'">
              {{ c.name }}
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown text="用户" right>
            <b-dropdown-item href="#">退出</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-container fluid id="basic-container">
      <router-view/>
    </b-container>

    <DatetimeModal/>

  </div>
</template>

<script>
  import DatetimeModal from '@/components/DatetimeModal'

  export default {
    name: 'Basic',
    components: {
      DatetimeModal: DatetimeModal,
    },
    data() {
      return {
        categories: []
      }
    },
    computed: {
      fromDatetime: function () {
        if (this.$route.query.from) {
          if (/^\d+$/.test(this.$route.query.from)) {
            return this.utils.formatDatetime("YYYY-mm-dd HH:MM", new Date(this.$route.query.from * 1000))
          } else {
            return this.$route.query.from
          }
        }
      },
      untilDatetime: function () {
        if (this.$route.query.until) {
          if (/^\d+$/.test(this.$route.query.until)) {
            return this.utils.formatDatetime("YYYY-mm-dd HH:MM", new Date(this.$route.query.until * 1000))
          } else {
            return this.$route.query.until
          }
        }
      }
    },
    mounted() {
      this.axios.get("/api/v1/metric/metric_categories/",)
        .then(response => {
          this.categories = response.data.data.results;
        })

    },
  }
</script>

<style>
  #nav-collapse > ul > li > a {
    margin-left: 10px;
    margin-right: 10px;
  }

  #basic-container {
    margin-top: 15px;
    height: calc(100% - 76px);
    overflow: auto;
  }
</style>
