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

export function exchange({ telephone, code, exchangeCode }) {
  return request({
    url: "/exchange",
    method: "post",
    data: {
      telephone,
      sms_code: code,
      exchange_code: exchangeCode
    }
  })
}

export function getExchangeStatus(telephone) {
  return request({
    url: "/exchange_status/" + telephone,
    method: "get"
  })
}