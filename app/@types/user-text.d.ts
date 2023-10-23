export interface ISendUserTextResponse {
  id: string
}

export interface ISendUserTextForm {
  title?: string
  name: string
  email?: string
  phone: string
  text?: string
  utm?: string
  token?: string
  from?: string
}
