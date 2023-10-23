import type { BaseQueryFn } from '@reduxjs/toolkit/query'
import type { AxiosError } from 'axios'
import axios from 'axios'
import qs from 'query-string'
import { getErrorMessage } from './utils/api'
import { clearToken } from '@/lib/redux/actions/authDataActions'
import { IBaseQuery } from './@types/api'

export const api = axios.create({
  baseURL: process.env.BASE_API_URL,
  withCredentials: false,
  paramsSerializer: (params) => {
    return qs.stringify(params)
  },
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

const baseQuery = (): BaseQueryFn<IBaseQuery, unknown, unknown> => {
  return async ({ endpoint, headers = {}, ...axiosConfig }, { dispatch }) => {
    try {
      const result = await api({
        url: endpoint,
        headers: {
          // TODO: auth logic
          // @ts-ignore
          // Authorization: getState().authData.token,
          ...headers,
        },
        ...axiosConfig,
      })
      return { data: result.data }
    } catch (axiosError) {
      const err = axiosError as AxiosError
      const status = err?.response?.status
      const errorText = getErrorMessage(err.response?.data)

      switch (status) {
        case 401:
          dispatch(clearToken())
          break
      }

      return {
        error: {
          status: err.response?.status,
          data: err.response?.data || errorText,
        },
      }
    }
  }
}

export default baseQuery
