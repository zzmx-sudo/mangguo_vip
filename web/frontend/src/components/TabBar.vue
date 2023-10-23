<template>
  <div id="tabbar">
    <div class="top">芒果TV</div>
    <slot name="content"></slot>
  </div>
</template>

<script>
export default {
  name: "TabBar"
}
</script>

<style scoped>
.top {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #ffff;
  background-color: #705a0bba;
  border-radius: 5px;
}
</style>