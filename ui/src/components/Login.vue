<template>
  <div class="h-100" style="width: 400px; margin:0 auto; margin-top: 50px; padding: 0px 10px">
    <b-card>
      <div class="text-center" style="margin-bottom: 20px">
        <span style="font-size: 30px; font-weight: 500;" class="text-info">Dormer</span>
      </div>
      <div>
        <b-form @submit="login">
          <b-form-group
            label="用户名："
          >
            <b-input-group>
              <template v-slot:prepend>
                <b-input-group-text><i class="fa fa-user fa-fw"></i></b-input-group-text>
              </template>
              <b-form-input v-model="loginForm.username" type="text" required></b-form-input>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label="密码："
          >
            <b-input-group>
              <template v-slot:prepend>
                <b-input-group-text><i class="fa fa-key fa-fw"></i></b-input-group-text>
              </template>
              <b-form-input v-model="loginForm.password" type="password" required></b-form-input>
            </b-input-group>
          </b-form-group>

          <b-form-group class="text-right">
            <b-button type="submit" variant="info">登录</b-button>
          </b-form-group>
        </b-form>
      </div>
    </b-card>
  </div>
</template>

<script>
  export default {
    name: 'Login',
    data() {
      return {
        loginForm: {
          username: null,
          password: null
        }
      }
    },
    mounted() {

    },
    methods: {
      login: function (evt) {
        evt.preventDefault()
        console.log(this.loginForm)
        this.axios.post("/api/auth/", this.loginForm)
          .then(response => {
            this.axios.defaults.headers.common["Authorization"] = "JWT " + response.data.token;
            localStorage.setItem("username", this.loginForm.username);
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("jwt", `JWT ${response.data.token}`);

            let nextRoute = localStorage.getItem("nextRoute");
            if (nextRoute) {
              nextRoute = JSON.parse(nextRoute);
              if (nextRoute.path != "/") {
                this.$router.replace(nextRoute);
                return
              }
            }

            let path = "/user/" + this.loginForm.username + "/";
            let query = localStorage.getItem(path + ".query") || "{}";
            query = JSON.parse(query);
            this.utils.checkQueryFromUntil(query);
            this.utils.checkQueryRefresh(query);
            this.$router.replace({
              path: path,
              query: query
            });
          })
          .catch(error => {
            switch (error.response.status) {
              case 400:
                this.loginError = "请输入正确的用户名密码";
              default:
                this.loginError = "认证失败，请联系管理员";
            }
          })
      }
    }
  }
</script>

<style>

</style>
