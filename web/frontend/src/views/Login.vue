<template>
  <div id="login">
    <tab-bar>
      <div slot="content">
        <div class="container">
          <div class="phoneBox">
            <span class="phoneText">手机号:</span>
            <div class="phoneEdit">
              <input v-model="$v.user.telephone.$model" type="number" placeholder="请输入手机号" />
            </div>
            <div class="error" v-show="validateState('telephone')">手机号不符合要求</div>
          </div>
          <div class="codeBox">
            <span class="codeText">验证码:</span>
            <div class="codeEdit">
              <input v-model="$v.user.code.$model" type="number" placeholder="请输入验证码">
              <div class="get-code" :style="codeButton.style" @click="codeButtonClick">{{ codeButton.text }}</div>
            </div>
            <div class="error" v-show="validateState('code')">验证码为6位数字</div>
          </div>
          <div class="loginButton" @click="loginClick">
            点击登录
          </div>
        </div>
      </div>
    </tab-bar>
  </div>
</template>

<script>
import TabBar from "@/components/TabBar.vue"

import { telephone, code } from "@/vuelidate/vuelidate"

export default {
  name: "Login",
  components: {
    TabBar
  },
  data() {
    return {
      user: {
        telephone: "",
        code: ""
      },
      codeButton: {
        text: "获取验证码",
        style: {
          color: "black",
          backgroundColor: "#fff",
          fontSize: "15px"
        }
      },
      codeIsClick: false
    }
  },
  validations: {
    user: {
      telephone: telephone,
      code: code
    },
  },
  methods: {
    loginClick() {
      if (!this.phone || !this.code) {
        console.log("请输入正确的手机号和验证码后再登录");
      }
    },
    codeButtonClick() {
      if (this.codeIsClick) {
        return
      }
      if (!this.validateState("telephone")) {
        console.log("请输入正确的手机号后再获取验证码");
      }
      // 调用api获取手机验证码
      
    },
    validateState(name) {
      const { $dirty, $error } = this.$v.user[name];
      return $dirty ? $error: null;
    }
  }
}
</script>

<style scoped>
.container {
  margin-top: 20px;
  padding: 0 20px;
  height: 600px;
}

.container>div {
  margin-top: 20px;
  margin-bottom: 20px;
  font-size: 18px;
}

.container .error {
  font-size: 15px;
  margin-top: 10px;
  color: red;
  padding-left: 10px;
}

.phoneBox input {
  width: 100%;
}
.phoneBox input, .codeBox input {
  height: 40px;
  line-height: 40px;
  font-size: 16px;
  padding-left: 15px;
  border: 1px solid #fff;
  background-color: #c0bebd76;
  border-radius: 8px;
}

.phoneBox .phoneEdit, .codeBox .codeEdit {
  margin-top: 10px;
}

.codeBox span {
  display: block;
}

.codeBox .codeEdit {
  height: 40px;
  line-height: 40px;
}

.codeEdit input {
  width: 60%;
  float: left;
}

.codeEdit .get-code {
  width: 35%;
  float: right;
  height: 40px;
  text-align: center;
  border: 1px solid #fb5c12c6;
  border-radius: 5px;
}

.loginButton {
  margin-top: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border-radius: 10px;
  color: #fff;
  background-color: #fb5c12c6;
}
</style>