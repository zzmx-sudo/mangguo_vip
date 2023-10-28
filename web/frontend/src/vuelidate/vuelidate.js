import { required, numeric, minLength, maxLength } from "vuelidate/lib/validators"

const telephoneReValidator = (value) => /^1[3|5|7|8|9]\d{9}$/.test(value)
const exchangeCOdeReValidator = (value) => /^[A-Za-z0-9]{8}$/.test(value)

const telephone = {
  required,
  numeric,
  telephoneReValidator
}

const code = {
  required,
  numeric,
  minLength: minLength(6),
  maxLength: maxLength(6)
}

const exchangeCode = {
  required,
  exchangeCOdeReValidator
}

export {
  telephone,
  code,
  exchangeCode
}