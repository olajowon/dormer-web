<template>
  <b-row>
    <b-col v-for="metric, idx in metrics" :key="metric.name" cols="12" sm="12" md="6">
      <b-card
        :header="metric.name"
        class="metric-card"
      >
        <MetricChart
          v-bind:metric.sync="metric.name"
          v-bind:from.sync="from"
          v-bind:until.sync="until"
          :ref="'metric-' + metric.name + '-chart'"/>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import MetricChart from '@/components/metric/MetricChart'

  export default {
    name: 'MetricDash',
    components: {
      MetricChart: MetricChart,
    },

    data() {
      return {
        metrics: [],
        charts: [],
        from: null,
        until: null,
      }
    },

    watch: {
      "$route.query": function (n, o) {
        if (n.name != o.name) {
          this.clearCharts();
          this.setFromUntil();
          this.$nextTick(() => {
            this.makeCharts();
          });
        } else if (n.from != o.from || n.until != o.until) {
          this.setFromUntil();
          this.$nextTick(() => {
            this.refreshCharts();
          });
        }
      }
    },

    mounted() {
      this.setFromUntil();
      this.makeCharts();
    },

    methods: {
      setFromUntil() {
        if (this.$route.query.from || this.$route.query.until) {
          this.from = this.$route.query.from;
          this.until = this.$route.query.until;
        } else {
          this.from = "-1h"
          this.until = "now"
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
            })
        } else {
          this.metrics = [{name: this.$route.query.name}];
        }
      },

      clearCharts() {
        this.metrics = [];
      },

      refreshCharts() {
        for (let i = 0; i < this.metrics.length; i++) {
          this.$refs["metric-" + this.metrics[i].name + "-chart"][0].refresh();
        }
      }
    }
  }
</script>
<style>
  .metric-card {
    margin-bottom: 15px;
  }

  .metric-card .card-header {
    font-size: 14px;
    padding: 0.45rem 0.95rem;
  }

  .metric-card .card-body {
    padding: 0.45rem 0.55rem;
    height: 220px;
  }
</style>
