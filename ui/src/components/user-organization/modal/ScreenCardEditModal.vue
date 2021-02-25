<template>
  <b-modal :visible="visible" size="lg" scrollable @hidden="onModalHidden" title="图形编辑">
    <b-row>
      <b-col cols="12" v-if="form">
        <b-card
          class="card-sm  metric-card"
          header-tag="header"
        >
          <template v-slot:header>
            <span class="mb-0">{{ form.title || "--" }}</span>
          </template>
          <Chart
            :ref="'screen-card-edit-chart'"/>
        </b-card>
        <b-card no-body>
          <b-tabs card small>
            <b-tab title="设置" active title-link-class="text-secondary">
              <b-card-text>
                <b-form>
                  <b-form-group
                    label="标题"
                    >
                    <b-form-input
                      v-model="form.title"
                      type="text"
                      size="sm"
                      required
                    ></b-form-input>
                  </b-form-group>
                </b-form>
              </b-card-text>
            </b-tab>
            <b-tab title="指标" title-link-class="text-secondary">
              <b-card-text>
                <b-form>
                  <b-form-group
                    v-for="target, idx in form.targets"
                    :key="idx"
                    :label="'指标 ' + (idx + 1)"
                    >
                    <b-input-group>
                      <b-form-input
                        v-model="target.target"
                        type="text"
                        size="sm"
                        required
                        @change="onFormTargetsChange"
                      ></b-form-input>
                      <b-input-group-append>
                        <b-button variant="outline-info" size="sm" @click="onRemoveFormTargetBtnClick(idx)">
                          <i class="fa fa-minus fa-fw" aria-hidden="true"></i>
                        </b-button>
                      </b-input-group-append>
                    </b-input-group>
                  </b-form-group>
                </b-form>
                <b-button variant="outline-info" size="sm" @click="onAddFormTargetBtnClick"><i class="fa fa-plus fa-fw"></i></b-button>
              </b-card-text>
            </b-tab>
          </b-tabs>
        </b-card>
      </b-col>
    </b-row>
    <template #modal-footer>
      <div class="w-100">
        <b-button variant="info" size="sm" class="float-right" @click="onSubmitClick()">
          确定
        </b-button>
      </div>
    </template>
  </b-modal>
</template>
<script>
  import Chart from '@/components/common/Chart'

  export default {
    name: 'ScreenCardEditModal',
    components: {
      Chart: Chart,
    },
    data() {
      return {
        form: {
          title: "",
          targets: []
        },
        chart: {
          target: null,
          from: "-1h",
          until: "now",
        },
        visible: true
      }
    },

    mounted() {
      this.init();
    },

    methods: {
      init() {
        let card = JSON.parse(JSON.stringify(this.card));
        this.form = {
          title: card.title || "",
          targets: card.targets || [],
        }

        if (this.form.targets.length == 0) {
          this.addTarget();
        }

        this.$nextTick(() => {
          this.updateChartTargets();
        })
      },

      onSubmitClick() {
        this.card.title = this.form.title;
        this.card.targets = this.form.targets;
        this.$parent.renderChart(this.card.i, this.chart.target);
        this.$parent.reflowChart(this.card.i);
        this.visible = false;
      },

      onModalHidden() {
        this.$emit("update:show", false)
      },

      onFormTargetsChange() {
        this.updateChartTargets();
      },

      onAddFormTargetBtnClick() {
        this.addTarget();
      },

      onRemoveFormTargetBtnClick(idx) {
        this.form.targets.splice(idx, 1);
      },

      updateChartTargets() {
        this.chart.target = (this.form.targets || []).filter(function (t) {
          return t.target;
        }).map(function (t) {
          return t.target;
        })

        this.renderChart();
      },

      renderChart() {
        this.$nextTick(() => {
          this.$refs["screen-card-edit-chart"].render(this.chart);
        });
      },

      addTarget() {
        this.form.targets.push({
          target: ""
        })
      }
    },
    props: ["card", "show"]
  }
</script>
