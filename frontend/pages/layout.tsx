/* Components */
import { Providers } from '@/lib/providers'

/* Instruments */
import styles from './layout.module.scss'
import '@/app/styles/globals.scss'

const RootLayout = (props: React.PropsWithChildren) => {
  return (
    <Providers>
      <main className={styles.main}>{props.children}</main>
    </Providers>
  )
}

export default RootLayout
