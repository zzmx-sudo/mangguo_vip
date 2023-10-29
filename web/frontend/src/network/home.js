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

export function exchange({ telephone, sms_code, exchange_code }) {
  return request({
    url: "/exchange",
    method: "post",
    data: {
      telephone,
      sms_code,
      exchange_code
    }
  })
}

export function getExchangeStatus(telephone) {
  return request({
    url: "/exchange_status/" + telephone,
    method: "get"
  })
}