import { IFieldFormProps } from '@/app/@types/common'
import React, { useCallback, useMemo } from 'react'
import { useController } from 'react-hook-form'
import style from './TextInput.module.scss'

interface IProps extends IFieldFormProps {
  onChange?: (value: any) => void
  placeholder?: string
}

const TextInput: React.FC<IProps> = (props) => {
  const { control, name, className, onChange, placeholder } = props

  const { field, fieldState } = useController({ name, control })

  const errorText = useMemo(() => {
    return fieldState?.error?.message
  }, [fieldState?.error])

  const handleChange = useCallback(
    (value: any) => {
      if (onChange) {
        onChange(value)
      }
      field.onChange(value)
    },
    [field, onChange],
  )

  return (
    <div>
      <input onChange={handleChange} className={className} type='text' name={name} placeholder={placeholder} />
      <div className={style.TextInput__error}>{errorText}</div>
    </div>
  )
}

export default React.memo(TextInput)
