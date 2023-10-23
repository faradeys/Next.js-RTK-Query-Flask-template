import { createAction } from '@reduxjs/toolkit'

export const CLEAR_TOKEN = 'authData/clearToken'

export const clearToken = createAction<void>(CLEAR_TOKEN)
