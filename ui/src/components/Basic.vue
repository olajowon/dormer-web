<template>
  <div class="h-100">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Dormer</b-navbar-brand>

      <div style="position: absolute; right: 90px; top: 12px">
        <span>
          <span class="d-none d-sm-inline-block text-light" v-if="fromDatetime || untilDatetime"
                 style="vertical-align: middle; font-size: 1rem">
            {{ fromDatetime }} ~ {{ untilDatetime }}
          </span>
          <b-button variant="info" size="sm" v-b-modal.datetime-modal style="padding-top: 0.395rem; padding-bottom: 0.245rem;">
            <i class="fa fa-clock-o" style="font-size: 1.125rem"></i>
          </b-button>
        </span>
        <span style="margin-left: 10px">
          <span class="d-none d-sm-inline-block text-light" v-if="refreshInterval"
                 style="vertical-align: middle; font-size: 1rem">
            {{ refreshInterval }}
          </span>
          <b-button-group>
            <b-dropdown id="nav-refresh-dropdown" right split variant="info" size="sm" @click="onRefreshBtnClick()">
              <template #button-content  >
                <i class="fa fa-refresh" style="font-size: 0.95rem"></i>
              </template>
              <b-dropdown-item @click="changeRefreshInterval(0)">Off</b-dropdown-item>
              <b-dropdown-item @click="changeRefreshInterval(30)">30s</b-dropdown-item>
              <b-dropdown-item @click="changeRefreshInterval(60)">1m</b-dropdown-item>
              <b-dropdown-item @click="changeRefreshInterval(300)">5m</b-dropdown-item>
              <b-dropdown-item @click="changeRefreshInterval(600)">10m</b-dropdown-item>
            </b-dropdown>
          </b-button-group>
        </span>
      </div>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :class="{active: $route.name=='User'}" :href="'/#/user/' + username + '/'">用户</b-nav-item>

          <b-nav-item :class="{active: $route.name=='Organization'}" href="/#/organization/">组织</b-nav-item>

          <b-nav-item-dropdown id="nav-metric-dropdown" :class="{active: $route.name=='Metric'}" text="指标">
            <b-dropdown-item v-for="(c, idx) in categories"
                             :class="{active: $route.params.category==c.name}"
                             :key="idx"
                             :href="'/#/metric/' + c.name + '/'">
              {{ c.name }}
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <template v-slot:button-content>
              <i class="fa fa-user"></i>
            </template>
            <b-dropdown-item href="#" @click="logout">退出</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-container fluid id="basic-container">
      <router-view ref="content"/>
    </b-container>

    <DatetimeModal/>

  </div>
</template>

<script>
  import DatetimeModal from '@/components/common/DatetimeModal'

  export default {
    name: 'Basic',
    components: {
      DatetimeModal: DatetimeModal,
    },
    data() {
      return {
        categories: [],
        username: localStorage.getItem("username")
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
      },

      refreshInterval: function () {
        if (this.$route.query.refresh) {
          if (this.$route.query.refresh == 0) {
            return "Off"
          } else if (this.$route.query.refresh < 60) {
            return this.$route.query.refresh + "s"
          } else {
            return this.$route.query.refresh / 60 + "m"
          }
        } else {
          return "Off"
        }
      }
    },
    mounted() {
      console.log(this.$route)
      this.axios.get("/api/v1/metric/metric_categories/",)
        .then(response => {
          this.categories = response.data.data.results;
        })
    },

    methods: {
      logout () {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        localStorage.removeItem("jwt");
        this.$router.push("/login/");
      },

      changeRefreshInterval(refresh) {
        if (this.$route.query.refresh != refresh) {
          let q = this.$route.query;
          delete q["refresh"]
          this.$router.push({
            query: this.merge(q, {refresh: refresh})
          })
        }
      },

      onRefreshBtnClick() {
        this.$refs.content.refresh();
      }
    }
  }
</script>

<style>
  #nav-collapse > ul > li > a {
    margin-left: 10px !important;
    margin-right: 10px !important;
  }

  #basic-container {
    margin-top: 15px !important;
    height: calc(100% - 76px) !important;
    overflow: auto !important;
  }

  .navbar {
    font-size: 1.115rem !important;
  }

  .navbar-dark .navbar-nav .nav-link {
    color: #fff !important;
  }

  .navbar-dark .navbar-nav .active > .nav-link {
    color: #ffc107 !important;
  }

  .navbar-dark .navbar-nav .active > .nav-link:not(.dropdown-toggle) {
    pointer-events: none !important;
  }

  .navbar-dark .navbar-nav .active > .dropdown-item {
    color: #ffc107 !important;
    pointer-events: none !important;
  }

  #nav-metric-dropdown .dropdown-item {
    font-size: 1.125rem !important;
  }

  #nav-refresh-dropdown .dropdown-toggle {
    font-size: 0.96rem !important;
  }
</style>
