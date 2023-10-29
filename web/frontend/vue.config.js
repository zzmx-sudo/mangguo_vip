const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: "8080",
    open: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000",
        ws: false,
        changeOrigin: true,
        pathRewrite: {
          "^/api": ""
        }
      }
    }
  }
})
