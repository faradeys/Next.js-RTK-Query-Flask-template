import type { ReactElement } from 'react'
import Layout from './layout'
import { NextPageWithLayout } from './_app'
import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import style from './index.module.scss'
import Head from 'next/head'

const Page: NextPageWithLayout = () => {
  return (
    <div className={style.Index}>
      <Head>
        <title>Nextjs Rtk Flask</title>
      </Head>
      Hello world! I will fuck you!
    </div>
  )
}

const getLayout = (page: ReactElement) => {
  return <Layout>{page}</Layout>
}

Page.getLayout = getLayout

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translationsProps = await serverSideTranslations(locale ?? 'ru')

  return {
    props: {
      ...translationsProps,
    },
  }
}

export default Page
