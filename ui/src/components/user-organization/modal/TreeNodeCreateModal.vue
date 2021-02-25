<template>
  <b-modal :visible="visible" scrollable @hidden="onModalHidden" title="创建节点">
    <b-row>
      <b-col cols="12">
        <b-form>
          <b-form-group label="Path *">
            <b-form-input
              v-model="form.path"
              type="text"
              size="sm"
              required
            ></b-form-input>
          </b-form-group>
          <b-form-group label="类型 *">
            <b-form-radio-group
              v-model="form.type"
              :options="typeOptions"
              value-field="value"
              text-field="text"
              size="sm"
            ></b-form-radio-group>
          </b-form-group>
        </b-form>
      </b-col>
    </b-row>
    <template #modal-footer>
      <div class="w-100">
        <b-button :disabled="submitting" variant="info" size="sm" class="float-right" @click="onSubmitClick">
          提 交
        </b-button>
      </div>
    </template>
  </b-modal>
</template>
<script>

  export default {
    name: 'TreeNodeCreateModal',

    data() {
      return {
        form: {
          path: null,
          type: null,
        },
        typeOptions: [
          {value: "branch", text: "分支(Branch)"},
          {value: "alarm", text: "报警(Alarm)"},
          {value: "screen", text: "聚合图形(Screen)"},
        ],
        submitting: false,
        visible: true
      }
    },

    mounted() {
      this.init();
    },

    methods: {
      init() {
        this.form.path = this.parentNode.path + ".";
      },

      onSubmitClick() {
        this.submitting = true;
        this.axios.post("/api/v1/tree/nodes/", this.form)
          .then(response => {
            this.$root.$bvToast.toast("创建成功", {
              title: "提示",
              variant: "success",
              toaster: "b-toaster-top-center",
              solid: true
            })
            this.submitting = false;
            this.visible = false;
            this.$router.push({
              query: this.merge(this.$route.query, {path: this.form.path, type: this.form.type})
            });
          })
          .catch(error => {
            this.submitting = false;
          })
      },

      onModalHidden: function () {
        this.$emit("update:show", false)
      },
    },
    props: ["parentNode", "show"]
  }
</script>
