type TProps = <T>(tags: T[]) => unknown

export const getInvalidatesTags: TProps = (tags) => {
  return (result: unknown, err: unknown) => {
    return !result && err ? [] : tags
  }
}
