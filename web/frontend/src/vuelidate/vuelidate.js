import { required, numeric, minLength, maxLength } from "vuelidate/lib/validators"

const telephoneReValidator = (value) => /^1[3|5|7|8|9]\d{9}$/.test(value)

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

export {
  telephone,
  code
}