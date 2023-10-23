import type { PayloadAction } from '@reduxjs/toolkit'
import { createSlice } from '@reduxjs/toolkit'

const initialState: any = {}

const serviceSliceSlice = createSlice({
  name: 'serviceSlice',
  initialState,
  reducers: {
    setServiceSlice: (state, action: PayloadAction<any>) => {
      return action.payload
    },
    clearServiceSlice: () => {
      return initialState
    },
  },
})

export const { setServiceSlice, clearServiceSlice } = serviceSliceSlice.actions
export const service = serviceSliceSlice.reducer
