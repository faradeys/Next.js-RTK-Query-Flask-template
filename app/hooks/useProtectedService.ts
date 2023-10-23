import { useAppSelector } from '@/lib/redux'
import { serviceSelector } from '@/lib/redux/selector/serviceSelector'
import { useRouter } from 'next/router'
import { useEffect } from 'react'

export const useProtectedService = () => {
  const router = useRouter()
  const service = useAppSelector(serviceSelector)
  const { damages, model, problems, serviceType } = service

  useEffect(() => {
    if (!serviceType) {
      void router.replace('/')
    }

    if (serviceType && (!damages || !model || !problems)) {
      void router.replace(serviceType)
    }
  }, [damages, model, problems, router, serviceType])
}
