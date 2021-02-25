<template>
  <b-modal id="datetime-modal" @show="onModalShow" title="时间选择">
    <b-row>
      <b-col cols="4">
        <b-button-group vertical>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-1h', 'now')">最近1小时</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-3h', 'now')">最近3小时</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-6h', 'now')">最近6小时</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-12h', 'now')">最近12小时</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-1d', 'now')">最近1天</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-2d', 'now')">最近2天</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-7d', 'now')">最近7天</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-15d', 'now')">最近15天</b-button>
          <b-button squared variant="info" size="sm" @click="onRelativeClick('-30d', 'now')">最近30天</b-button>
        </b-button-group>
      </b-col>
      <b-col cols="8">
        <b-form>
          <b-form-group
            label="From:"
            >
            <flat-pickr
              v-model="from"
              class="form-control"
              :config="fromConfig"
              @on-change="onFromChange"
            ></flat-pickr>
          </b-form-group>
          <b-form-group
            label="Until:"
            >
            <flat-pickr
              v-model="until"
              class="form-control"
              :config="untilConfig"
              @on-change="onUntilChange"
            ></flat-pickr>
          </b-form-group>
        </b-form>
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


  export default {
    name: 'DatetimeModal',
    data() {
      return {
        from: null,
        until: null,
        fromConfig: {
          allowInput: true,
          enableTime: true,
          time_24hr: true,
          dateFormat: 'Y-m-d H:i',
          defaultHour: 0,
          maxDate: null,

        },
        untilConfig: {
          allowInput: true,
          enableTime: true,
          time_24hr: true,
          dateFormat: 'Y-m-d H:i',
          defaultHour: 0,
          minDate: null
        }
      }
    },
    mounted() {
    },

    methods: {
      onModalShow: function () {
        this.from = null;
        this.until = null;
      },

      onSubmitClick: function () {
        if (this.from && this.until) {
          this.changeQueryFromUntil(
            new Date(this.from).getTime() / 1000,
            new Date(this.until).getTime() / 1000,
          )
        }
        this.$bvModal.hide('datetime-modal')
      },

      onRelativeClick(_from, _until) {
        this.changeQueryFromUntil(_from, _until)
        this.$bvModal.hide('datetime-modal')
      },

      changeQueryFromUntil(_from, _until) {
        this.$router.push({
          query: this.merge(this.$route.query, {from: _from, until: _until})
        })
      },

      onFromChange(selectedDates, dateStr, instance) {
        this.untilConfig.minDate = dateStr
      },
      onUntilChange(selectedDates, dateStr, instance) {
        this.fromConfig.maxDate = dateStr
      }
    }
  }
</script>
