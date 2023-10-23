import baseQuery from '@/app/api'
import { createApi } from '@reduxjs/toolkit/query/react'

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: baseQuery(),
  endpoints: () => ({}),
})
