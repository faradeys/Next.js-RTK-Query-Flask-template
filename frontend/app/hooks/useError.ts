import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { getErrorMessage } from '../utils/api'

interface IProps {
  errorTitle?: string
  successTitle?: string
  isSuccess?: boolean
  error?: unknown
}

export const useError = (props: IProps) => {
  const { errorTitle, error, successTitle, isSuccess } = props

  const { t } = useTranslation()

  useEffect(() => {
    if (!error) {
      return
    }

    const errorText = getErrorMessage(error)

    // TODO: https://trello.com/c/nnYskw45
    // eslint-disable-next-line no-console
    console.log(errorTitle, errorText)
  }, [error, errorTitle])

  useEffect(() => {
    if (!isSuccess) {
      return
    }
    // TODO: https://trello.com/c/nnYskw45
    // eslint-disable-next-line no-console
    console.log(successTitle)
  }, [isSuccess, successTitle, t])
}
