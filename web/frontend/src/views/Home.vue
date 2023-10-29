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
          <div class="bottomContainer"  v-if="isGetCode">
            <div class="exchangeCodebox">
              <span class="exchangeCodeText">兑换码:</span>
              <div class="exchangeCodeEdit">
                <input v-model="$v.user.exchangeCode.$model" type="text" placeholder="请输入兑换码">
              </div>
              <div class="error" v-show="validateState('exchangeCode')">请输入正确的兑换码</div>
            </div>
            <div class="exchangeButton" @click="exchangeClick" :style="exchangeButton.style">
              {{ exchangeButton.text }}
            </div>
          </div>
        </div>
      </div>
    </tab-bar>
    <message-box ref="messageBox" :title="messageTitle" :message="messageContent" :color="messageColor">
    </message-box>
  </div>
</template>

<script>
import TabBar from "@/components/TabBar.vue"
import MessageBox from "@/components/MessageBox.vue"

import { telephone, code, exchangeCode } from "@/vuelidate/vuelidate"
import { getCode, exchange } from "@/network/home"

export default {
  name: "Login",
  components: {
    TabBar,
    MessageBox
  },
  data() {
    return {
      user: {
        telephone: "",
        code: "",
        exchangeCode: ""
      },
      codeButton: {
        text: "获取验证码",
        clicking: false,
        style: {
          color: "black",
          backgroundColor: "#fff",
          fontSize: "15px"
        }
      },
      exchangeButton: {
        text: "点击兑换",
        clicking: false,
        style: {
          color: "#fff",
          backgroundColor: "#fb5c12c6",
          foneSize: "18px"
        }
      },
      isGetCode: false,
      messageTitle: "",
      messageContent: "",
      messageColor: ""
    }
  },
  validations: {
    user: {
      telephone: telephone,
      code: code,
      exchangeCode: exchangeCode
    },
  },
  methods: {
    exchangeClick() {
      if (this.exchangeButton.text !== "点击兑换" || this.exchangeButton.clicking) {
        return
      }
      console.log("exchangeClick...");
      if (!this.user.telephone || !this.user.code || ! this.user.exchangeCode) {
        this.showMessage(
          "参数不完整",
          "请输入正确的手机号、验证码和兑换码后再点击兑换",
          "red"
        )
        return
      }
      if (
        this.validateState("telephone") || 
        this.validateState("code") || 
        this.validateState("exchangeCode")
      ) {
        this.showMessage(
          "参数不完整",
          "请输入正确的手机号、验证码和兑换码后再点击兑换",
          "red"
        )
        return
      }
      this.exchangeButton.clicking = true;
      this.exchangeButton.text = "兑换中。。。"
      // 调用api实现兑换
      exchange(this.user).then(res => {
        if (res.errno !== "200") {
          this.showMessage(
            "兑换失败",
            res.errmsg,
            "red"
          )
          this.exchangeButton.clicking = false;
          this.exchangeButton.text = "点击兑换"
        } else {
          this.showMessage(
            "兑换成功",
            "发起兑换成功, 预计10分钟之内可兑换完成, 您可在芒果TV中查看结果",
            "green"
          )
          this.exchangeButton.text = "兑换成功";
          this.exchangeButton.style = {
            color: "black",
            backgroundColor: "rgb(200, 200, 200)"
          }
        }
      }).catch(error => {
        this.showMessage(
          "兑换失败",
          "兑换发生网络错误",
          "red"
        )
        this.exchangeButton.clicking = false;
        this.exchangeButton.text = "点击兑换"
      })
    },
    codeButtonClick() {
      if (this.codeButton.text !== "获取验证码" || this.codeButton.clicking) {
        return
      }
      if (!this.user.telephone || this.validateState("telephone")) {
        this.showMessage(
          "非法手机号",
          "手机号格式不正确, 请输入正确手机号后再获取验证码！",
          "red"
        )
        return
      }
      // 调用api获取验证码
      getCode(this.user.telephone).then(res => {
        if (res.errno !== "200") {
          this.showMessage(
            "获取验证码失败",
            res.errmsg,
            "red"
          )
        } else {
          this.isGetCode = true;
          this.codeButton.clicking = true;
          this.codeButton.style = {
            color: "black",
            backgroundColor: "rgb(200, 200, 200)",
            fontSize: "15px",
            border: "none"
          };
          let second = 60;
          this.codeButton.text = String(second) + " 秒"
          let interval = setInterval(() => {
            second -= 1;
            if (second === 0) {
              this.codeButton.text = "获取验证码";
              this.codeButton.clicking = false;
              this.codeButton.style = {
                color: "black",
                backgroundColor: "#fff",
                fontSize: "15px",
                border: "1px solid #fb5c12c6"
              }

              clearInterval(interval);
              return
            }
            this.codeButton.text = String(second) + " 秒"
          }, 1000)
        }
      }).catch(err => {
        this.showMessage(
          "获取验证码失败",
          "获取验证码发生网络错误",
          "red"
        )
      })
    },
    validateState(name) {
      const { $dirty, $error } = this.$v.user[name];
      return $dirty ? $error: null;
    },
    showMessage(title, content, color) {
      this.messageTitle = title;
      this.messageContent = content;
      this.messageColor = color;
      this.$refs.messageBox.show();
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

.phoneBox input, .exchangeCodebox input {
  width: 100%;
}
.phoneBox input, .codeBox input, .exchangeCodebox input {
  height: 40px;
  line-height: 40px;
  font-size: 16px;
  padding-left: 15px;
  border: 1px solid #fff;
  background-color: #c0bebd76;
  border-radius: 8px;
}

.phoneBox .phoneEdit, .codeBox .codeEdit, .exchangeCodeBox .exchangeCodeEdit {
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

.exchangeCodeEdit {
  margin-top: 10px;
}

.exchangeButton {
  margin-top: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border-radius: 10px;
}
</style>