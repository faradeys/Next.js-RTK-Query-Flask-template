import { ISendUserTextForm, ISendUserTextResponse } from '@/app/@types/user-text'
import { baseApi } from './baseApi'

const ENDPOINT_SCOPE = 'user_text'

export const userTextApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    sendUserText: build.mutation<ISendUserTextResponse, ISendUserTextForm>({
      query: (data) => ({ endpoint: `${ENDPOINT_SCOPE}/send`, method: 'post', data }),
    }),
  }),
})

export const { useSendUserTextMutation } = userTextApi
