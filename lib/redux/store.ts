/* Core */
import { configureStore, combineReducers, ThunkAction, Action } from '@reduxjs/toolkit'
import { useDispatch, type TypedUseSelectorHook, useSelector } from 'react-redux'

/* Instruments */
import { middleware } from './middleware'
import { baseApi } from './query/baseApi'
import {
  FLUSH,
  PAUSE,
  PERSIST,
  PURGE,
  PersistConfig,
  REGISTER,
  REHYDRATE,
  persistReducer,
  persistStore,
} from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import { service } from './slices/serviceSlice'

const persistConfig: PersistConfig<any> = {
  key: 'root',
  version: 1,
  storage,
  whitelist: ['authData'],
}

const reducer = combineReducers({
  [baseApi.reducerPath]: baseApi.reducer,
  service,
})

const persistedReducer = persistReducer(persistConfig, reducer)

const reduxStore = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
      .concat(process.env.DEBUG ? middleware : [])
      .concat(baseApi.middleware),
})

export type TRootState = ReturnType<typeof reducer>
export type TAppDispatch = typeof reduxStore.dispatch
export type ReduxState = ReturnType<typeof reduxStore.getState>
export type ReduxThunkAction<ReturnType = void> = ThunkAction<ReturnType, ReduxState, unknown, Action>
export type ReduxDispatch = typeof reduxStore.dispatch

export const useAppSelector: TypedUseSelectorHook<TRootState> = useSelector
export const useAppDispatch = () => useDispatch<TAppDispatch>()

export const persistor = persistStore(reduxStore)

export default reduxStore
