import { PropsWithChildren, memo } from 'react'
import styles from './Button.module.scss'
import Link from 'next/link'
import cn from 'classnames'

interface IButtonProps {
  to?: string
  onClick?: () => void
  className?: string
  disabled?: boolean
}

const Button: React.FC<PropsWithChildren<IButtonProps>> = (props) => {
  const { to, onClick, children, className, disabled } = props

  if (to) {
    return (
      <Link className={cn(styles.Button, className, { [styles.Button__disabled]: disabled })} href={to}>
        {children}
      </Link>
    )
  }

  return (
    <button onClick={onClick} className={cn(styles.Button, className, { [styles.Button__disabled]: disabled })}>
      {children}
    </button>
  )
}

export default memo(Button)
