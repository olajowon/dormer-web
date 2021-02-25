<template>
  <b-row class="h-100">
    <b-col v-show="role.viewer == false" cols="12">
      <b-alert show variant="danger">没有 {{ $route.query.path }} 查看权限！</b-alert>
    </b-col>

    <b-col v-if="role.owner" cols="12">
      <div class="screen-btn-group">
        <b-button variant="success" size="xs" @click="onAddScreenCardBtnClick">
          <i class="fa fa-plus fa-fw" aria-hidden="true"></i> 添加
        </b-button>

        <template v-if="!settingsChanged">
          <b-button disabled variant="info" size="xs" @click="onSaveScreenBtnClick">
            <i class="fa fa-floppy-o fa-fw" aria-hidden="true"></i> 保存
          </b-button>
          <b-button disabled variant="warning" size="xs" @click="onResetScreenBtnClick">
            <i class="fa fa-undo fa-fw" aria-hidden="true"></i> 重置
          </b-button>
        </template>
        <template v-else>
          <b-button class="save-screen-alert" variant="info" size="xs" @click="onSaveScreenBtnClick">
            <i class="fa fa-floppy-o fa-fw" aria-hidden="true"></i> 保存
          </b-button>
          <b-button variant="warning" size="xs" @click="onResetScreenBtnClick">
            <i class="fa fa-undo fa-fw" aria-hidden="true"></i> 重置
          </b-button>
        </template>
      </div>
    </b-col>

    <div :class="['screen-panel', {'screen-panel-height': role.owner, 'screen-panel-position': !role.owner}]">
      <grid-layout
        :layout.sync="settings.cards"
        :col-num="12"
        :row-height="10"
        :is-draggable="role.owner"
        :is-resizable="role.owner"
        :is-mirrored="false"
        :autoSize="true"
        :vertical-compact="true"
        :margin="[15, 15]"
        :use-css-transforms="true"
      >
        <grid-item v-for="card, idx in settings.cards"
                   :x="card.x"
                   :y="card.y"
                   :w="card.w"
                   :h="card.h"
                   :i="card.i"
                   :key="card.i"
                   @resized="onScreenCardResized"
        >
          <b-card
            class="card-sm screen-card"
            header-tag="header"
          >
            <template v-slot:header>
              <div>
              <span class="mb-0">{{ card.title || "标题" }}</span>
              <b-dropdown v-if="role.owner" class="card-option" right size="sm" variant="light">
                <b-dropdown-item href="#" @click="onEditScreenCardBtnClick(card)">编辑</b-dropdown-item>
                <b-dropdown-item href="#" @click="onRemoveScreenCardBtnClick(idx)">删除</b-dropdown-item>
              </b-dropdown>
              </div>
            </template>
            <Chart
              v-if="card.targets"
              :ref="'screen-' + card.i + '-chart'"/>
          </b-card>
        </grid-item>
      </grid-layout>
    </div>

    <ScreenCardEditModal
      v-if="editCardModalShow"
      v-bind:card.sync="editCard"
      v-bind:show.sync="editCardModalShow"/>
    </b-row>
</template>

<script>
  import Chart from '@/components/common/Chart'
  import ScreenCardEditModal from '@/components/user-organization/modal/ScreenCardEditModal'
  import VueGridLayout from 'vue-grid-layout'
  import { v4 as uuidv4 } from 'uuid';

  export default {
    name: 'OrganizationScreen',
    components: {
      Chart: Chart,
      ScreenCardEditModal: ScreenCardEditModal,
      GridLayout: VueGridLayout.GridLayout,
      GridItem: VueGridLayout.GridItem
    },

    data() {
      return {
        interval: null,
        bakSettingsStr: "",
        //settingsChanged: true,
        settings: {
          cards: []
        },
        role: {
          owner: null,
          viewer: null
        },
        cards: [],
        charts: [],
        from: null,
        until: null,
        editCard: null,
        editCardModalShow: false
      }
    },

    watch: {
      "$route.query": function (n, o) {
        if (n.path != o.path) {
          this.setFromUntil();
          this.$nextTick(() => {
            this.makeScreens();
          });
          this.makeInterval();
        } else if (n.from != o.from || n.until != o.until) {
          this.setFromUntil();
          this.$nextTick(() => {
            this.renderCharts();
          });
          this.makeInterval();
        } else if (n.refresh != o.refresh) {
          this.makeInterval();
        }
      },
    },

    computed: {
      settingsChanged() {
        return this.bakSettingsStr != JSON.stringify(this.settings)
      }
    },

    mounted() {
      this.setFromUntil();
      this.makeScreens();
      this.makeInterval();
    },

    beforeDestroy() {
      this.interval && clearInterval(this.interval);
    },

    methods: {
      onAddScreenCardBtnClick() {
        this.settings.cards.forEach(function (v) {
          v.y += 1
          return v
        })

        this.settings.cards.push({
          x: 0,
          y: 0,
          w: 6,
          h: 10,
          i: uuidv4(),
          title: "",
          targets: []
        })
      },

      onSaveScreenBtnClick() {
        let settings = this.settings;
        this.axios.put("/api/v1/screen/screens/" + this.$route.query.path + "/settings/", settings)
          .then(response => {
            this.bakSettingsStr = JSON.stringify(settings)
            this.$bvToast.toast("保存成功", {
              title: "提示",
              variant: "success",
              toaster: "b-toaster-top-center",
              solid: true
            })
          })
      },

      onResetScreenBtnClick() {
        this.settings = JSON.parse(this.bakSettingsStr);
        this.reflowCharts();
        this.renderCharts();
      },

      setFromUntil() {
        if (this.$route.query.from || this.$route.query.until) {
          this.from = this.$route.query.from;
          this.until = this.$route.query.until;
        } else {
          this.from = "-1h"
          this.until = "now"
        }
      },

      makeScreens() {
        this.clearScreens();

        this.axios.get("/api/v1/screen/screens/" + this.$route.query.path + "/dashboard/")
          .then(response => {
            let res = response.data.data.results;
            this.role.owner = res.role.owner;
            this.role.viewer = res.role.viewer;
            if (this.role.viewer) {
              this.settings.cards = res.settings.cards || [];
              this.bakSettingsStr = JSON.stringify(this.settings);
              this.reflowCharts();
              this.renderCharts();
            }
          })
          .catch(error => {
            this.bakSettingsStr = JSON.stringify(this.settings);
          })
      },

      makeInterval() {
        this.interval && clearInterval(this.interval)

        let refresh = this.$route.query.refresh;
        if (refresh && refresh > 0) {
          this.interval = setInterval(this.renderCharts, refresh * 1000)
        }
      },

      onEditScreenCardBtnClick(card) {
        this.editCard = card;
        this.editCardModalShow = true;
      },

      onRemoveScreenCardBtnClick(idx) {
        this.settings.cards.splice(idx, 1);
      },

      onScreenCardResized(i){
        this.$nextTick(() => {
          this.reflowChart(i);
        })
      },

      clearScreens() {
        this.settings = {
          cards: []
        };
        this.role = {
          owner: null,
          viewer: null
        }
      },

      reflowCharts() {
        this.$nextTick(() => {
          for (let i = 0; i < this.settings.cards.length; i++) {
            this.reflowChart(this.settings.cards[i].i);
          }
        })
      },

      reflowChart(i) {
        this.$refs["screen-" + i + "-chart"][0].reflow();
      },

      renderCharts() {
        this.$nextTick(() => {
          for (let i = 0; i < this.settings.cards.length; i++) {
            let targets = this.settings.cards[i].targets.map(function (t) {
              return t.target
            })
            this.renderChart(this.settings.cards[i].i, targets);
          }
        });
      },

      renderChart(i, targets) {
        let params = {
          target: targets,
          from: this.from,
          until: this.until
        }
        this.$refs["screen-" + i + "-chart"][0].render(params);
      },

      refresh() {
        this.renderCharts();
      }
    }
  }
</script>
<style>
  .screen-panel {
    width: 100% !important;
    overflow: auto !important;
  }

  .screen-panel-height {
    height: calc(100% - 30px) !important;
  }

  .screen-panel-position {
    position: relative !important;
    top: -15px !important;
  }

  .screen-card {
    margin-bottom: 0.875rem !important;
    height: 100% !important;
    width: 100% !important;
  }

  .screen-card .card-body {
    height: 100% !important;
    width: 100% !important;
  }

  .screen-btn-group {
    padding-top: 2px !important;
  }

  .save-screen-alert {
    animation: spinner-grow 1.5s ease-out infinite !important;
    padding-top: 0.16rem !important;
    padding-bottom: 0.14rem !important;
  }

</style>
