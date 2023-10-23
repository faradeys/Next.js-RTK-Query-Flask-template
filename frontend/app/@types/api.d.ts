import { AxiosRequestConfig } from 'axios'

export interface IBaseQuery extends AxiosRequestConfig {
  endpoint: string
}
