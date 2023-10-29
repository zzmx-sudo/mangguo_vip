<template>
  <div id="message-box" :style="{ color: color }" v-show="isShow">
    <div class="top">
      <span class="title">{{ title }}</span>
      <span class="close" @click="close">x</span>
    </div>
    <div class="message">{{ message }}</div>
  </div>
</template>

<script>
export default {
  name: "MessageBox",
  props: {
    title: {
      type: String,
      default() {
        return "";
      },
    },
    message: {
      type: String,
      default() {
        return "";
      },
    },
    color: {
      type: String,
      default() {
        return "green";
      },
    },
    timeout: {
      type: Number,
      default() {
        return 2000;
      },
    },
  },
  data() {
    return {
      isShow: false,
      timer: null,
    };
  },
  methods: {
    show() {
      this.isShow = true;
      this.timer = setTimeout(() => {
        this.isShow = false;
        clearTimeout(this.timer);
      }, this.timeout);
    },
    close() {
      this.isShow = false;
      if (this.timer) {
        clearTimeout(this.timer);
      }
    },
  },
};
</script>

<style scoped>
#message-box {
  position: fixed;
  top: 200px;
  left: 0;
  right: 0;
  width: 80%;
  margin: 0 auto;
  background-color: #fff;
  border: 1px solid #d4d4d5;
  border-radius: 10px;
}

#message-box .top {
  height: 40px;
  line-height: 40px;
  padding: 0 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  background-color: rgba(0, 0, 0, 0.3);
}

#message-box .top .title {
  font-size: 18px;
  font-weight: 500;
}

#message-box .top .close {
  float: right;
  color: rgba(0, 0, 0, 0.4);
}

.message {
  padding: 10px;
  font-size: 16px;
}
</style>