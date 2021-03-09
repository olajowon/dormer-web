<template>
  <b-row class="metric-dash">
    <b-col v-for="metric, idx in metrics" :key="metric.name" cols="12" sm="12" md="6">
      <b-card
        :header="metric.name"
        class="card-sm metric-card"
      >
        <Chart
          :ref="'metric-' + metric.name + '-chart'"/>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import Chart from '@/components/common/Chart'

  export default {
    name: 'Dash',
    components: {
      Chart: Chart,
    },

    data() {
      return {
        metrics: [],
        charts: [],
        from: null,
        until: null,
        interval: null
      }
    },

    watch: {
      "$route.query": function (n, o) {
        if (n.name != o.name) {
          this.clearCharts();
          this.makeFromUntil();
          this.$nextTick(() => {
            this.makeCharts();
          });
        } else if (n.from != o.from || n.until != o.until) {
          this.makeFromUntil();
          this.renderCharts();
        } else if (n.refresh != o.refresh) {
          this.makeInterval();
        }
      }
    },

    mounted() {
      this.makeFromUntil();
      this.makeCharts();
      this.makeInterval();
    },

    beforeDestroy() {
      this.interval && clearInterval(this.interval);
    },

    methods: {
      makeFromUntil() {
        if (this.$route.query.from || this.$route.query.until) {
          this.from = this.$route.query.from;
          this.until = this.$route.query.until;
        } else {
          this.from = "-1h"
          this.until = "now"
        }
      },

      makeInterval() {
        this.interval && clearInterval(this.interval)

        let refresh = this.$route.query.refresh;
        if (refresh && refresh > 0) {
          this.interval = setInterval(this.renderCharts, refresh * 1000)
        }
      },

      makeCharts() {
        if (this.$route.query.leaf != 1) {
          let params = {
            name: this.$route.query.name,
            keyword: this.$route.query.keyword || "*",
            leaf: 1
          }

          this.axios.get("/api/v1/metric/metric_offsprings/", {params: params})
            .then(response => {
              this.metrics = response.data.data.results
              this.renderCharts();
            })
        } else {
          this.metrics = [{name: this.$route.query.name}];
          this.renderCharts();
        }
      },

      clearCharts() {
        this.metrics = [];
      },

      renderCharts() {
        this.$nextTick(() => {
          for (let i = 0; i < this.metrics.length; i++) {
            let params = {
              target: this.metrics[i].name,
              from: this.from,
              until: this.until,
            }
            this.$refs["metric-" + this.metrics[i].name + "-chart"][0].render(params);
          }
        });
      },

      refresh() {
        this.renderCharts();
      }
    }
  }
</script>
<style>
  .metric-dash {
    height: 100%;
    overflow: auto
  }
</style>
