<template>
  <div style="height: 100%; width: 100%; position: relative">
    <i v-show="refreshing" class="fa fa-spinner chart-spinner text-secondary"></i>
    <div :id="id" style="height: 100%; width: 100%"></div>
  </div>
</template>
<script>
  import { v4 as uuidv4 } from 'uuid';

  export default {
    name: "Chart",
    data() {
      return {
        chart: null,
        id: "chart-" + uuidv4(),
        refreshing: false
      }
    },

    mounted() {
      this.makeChart();
    },
    beforeDestroy() {
      this.destory();
    },
    methods: {
      render(params) {
        if (this.refreshing == true) {
          return
        }
        this.refreshing = true;
        if (params.target.length > 0) {
          this.axios.get("/api/v1/render/", {params: params})
            .then(response => {
              let data = response.data;
              if (!this._isDestroyed) {
                this.updateChart(data)
              }
              this.refreshing = false;
            })
            .catch(error => {
              this.refreshing = false;
            })
        } else {
          if (!this._isDestroyed) {
            this.updateChart([])
          }
          this.refreshing = false;
        }
      },

      destory() {
        this.chart && this.chart.destroy()
      },

      updateChart(data) {
        let series = []
        let min, max
        if (data.length > 0 && data[0]["datapoints"].length > 0) {
          min = data[0]["datapoints"][0][1] * 1000
          max = data[0]["datapoints"][data[0]["datapoints"].length - 1][1] * 1000

          for (let i = 0; i < data.length; i++) {
            series.push({
              name: data[i].target,
              data: data[i].datapoints.map(function (v) {
                return [v[1] * 1000, v[0]]
              })
            })
          }

        }

        this.chart.xAxis[0].update({"min": min, "max": max})

        let diff = this.chart.series.length - series.length;

        if (diff > 0) {
          for (let i = 0; i<diff; i++) {
            this.chart.series[i].remove(true);
          }
        } else if (diff < 0) {
          for (let i = this.chart.series.length; i < series.length; i++) {
            this.chart.addSeries({});
          }
        }

        this.chart.update({
          series: series
        })
      },

      makeChart() {
        this.chart = new this.HighCharts.chart(this.id, {
          chart: {
            type: "line",
            zoomType: "x",
            resetZoomButton: {
              position: {
                x: 0,
                y: -25
              },
            },
            spacing: [25, 10, 0, 10],
            style: {
              fontFamily: "unset"
            }
          },

          title: {
            text: null,
          },

          xAxis: {
            type: "datetime",
            title: {
              text: ""
            },
            gridLineWidth: 1,
          },
          yAxis: {
            title: {
              text: ""
            },
            min: 0
          },
          tooltip: {
            valueSuffix: "",
            shared: true,
            crosshairs: true,
            backgroundColor: "#fff",
			      borderColor: "rgba(0, 0, 0, 0.125)",
            shadow: false,
            dateTimeLabelFormats: {
              minute: "%Y-%m-%d %H:%M",
            },
          },
          legend: {
            itemStyle: {
              fontWeight: "400"
            },
            align: "left",
          },
          plotOptions: {
            line: {
              lineWidth: 1.5,
              marker: {
                enabled: false,
              }
            },
          },
          series: [],
          credits: {
            text: "",
            href: ""
          },
          global: {
            useUTC: false,
          }
        });
      },

      reflow() {
        console.log()
        this.chart && this.chart.reflow();
      }
    },
  }
</script>
<style>
  .chart-spinner {
    position: absolute;
    z-index: 1;
    right: 2.5px;
    top: 5px;
    -webkit-animation: spin 1.5s linear infinite;
    animation: spin 1.5s linear infinite;
  }
</style>
