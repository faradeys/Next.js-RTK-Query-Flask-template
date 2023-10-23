import { baseApi } from './baseApi'

const ENDPOINT_SCOPE = 'service'

enum EServiceTags {
  getParams = 'getParams',
}

export const serviceApi = baseApi.enhanceEndpoints({ addTagTypes: Object.values(EServiceTags) }).injectEndpoints({
  endpoints: (build) => ({
    getParams: build.query<void, void>({
      query: () => ({ endpoint: `${ENDPOINT_SCOPE}/params`, method: 'get' }),
      providesTags: [EServiceTags.getParams],
    }),
    sendOrderForm: build.mutation<void, void>({
      query: (data) => ({ endpoint: `${ENDPOINT_SCOPE}/send`, method: 'post', data }),
      invalidatesTags: [EServiceTags.getParams],
    }),
  }),
})

export const { useGetParamsQuery, useSendOrderFormMutation } = serviceApi
