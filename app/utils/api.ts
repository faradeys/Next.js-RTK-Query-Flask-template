import { isArray, isString } from 'lodash'

export const getErrorMessage = (error?: any): string => {
  if (!error) {
    return 'Unknown error'
  }

  if (isString(error)) {
    return error
  }

  if (error.data) {
    return getErrorMessage(error.data)
  }

  if (error.errors) {
    return error.errors.join(', ')
  }

  if (error.message) {
    return error.message
  }

  if (error.code) {
    return error.code
  }

  if (isArray(error)) {
    return error.map(getErrorMessage).join(', ')
  }

  return JSON.stringify(error, undefined, 2)
}
