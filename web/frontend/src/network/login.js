import { request } from "./request";

export function getCode(telephone) {
  return request({
    url: "/get_sms",
    method: "post",
    data: {
      telephone
    }
  })
}

export function login({ telephone, sms_code }) {
  return request({
    url: "/login",
    method: "post",
    data: {
      telephone,
      sms_code
    }
  })
}