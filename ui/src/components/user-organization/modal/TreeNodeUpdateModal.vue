<template>
  <b-modal :visible="visible" scrollable @hidden="onModalHidden" title="修改节点">
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
    name: 'TreeNodeUpdateModal',

    data() {
      return {
        form: {
          path: null,
        },
        submitting: false,
        visible: true
      }
    },

    mounted() {
      this.init();
    },

    methods: {
      init() {
        this.form.path = this.node.path;
      },

      onSubmitClick() {
        console.log(this.form)
        this.submitting = true;
        this.axios.put("/api/v1/tree/nodes/" + this.node.path + "/", this.form)
          .then(response => {
            this.$root.$bvToast.toast("修改成功", {
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
    props: ["node", "show"]
  }
</script>
