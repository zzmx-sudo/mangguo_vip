import axios from "axios"

export function request(config) {
  // 创建axios实例
  const axiosInstance = axios.create({
    baseURL: "",
    timeout: 5000
  })

  // 拦截器
  axiosInstance.interceptors.request.use(config => {
    // 请求前必须携带Authorization
    Object.assign(config.headers, { Authorization: `Bearer mangguo-web-client` })
    return config
  }, err => {
    console.log(err);
  })

  axiosInstance.interceptors.response.use(result => {
    return result.data
  }, err => {
    console.log(err);
  })

  return axiosInstance(config)
}