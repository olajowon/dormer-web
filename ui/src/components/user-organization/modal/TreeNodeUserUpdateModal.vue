<template>
  <b-modal :visible="visible" scrollable @hidden="onModalHidden" title="修改节点用户">
    <b-row>
      <b-col cols="12">
        <b-form>
          <b-form-group label="Owners" v-show="node.space != 'user'">
            <b-form-tags
              v-model="form.owners"
              size="sm"
              separator=" ,;"
              placeholder=""
            ></b-form-tags>
          </b-form-group>
          <b-form-group label="Viewers">
            <b-form-tags
              v-model="form.viewers"
              size="sm"
              separator=" ,;"
              placeholder=""
            ></b-form-tags>
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
    name: 'TreeNodeUserUpdateModal',

    data() {
      return {
        form: {
          owners: [],
          viewers: []
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
        this.axios.get("/api/v1/tree/nodes/" + this.node.path + "/users/")
          .then(response => {
            this.form.owners = response.data.data.results.owners;
            this.form.viewers = response.data.data.results.viewers;
          })
      },

      onSubmitClick() {
        this.submitting = true;
        this.axios.put("/api/v1/tree/nodes/" + this.node.path + "/users/", this.form)
          .then(response => {
            this.$root.$bvToast.toast("修改成功", {
              title: "提示",
              variant: "success",
              toaster: "b-toaster-top-center",
              solid: true
            })
            this.submitting = false;
            this.visible = false;
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
