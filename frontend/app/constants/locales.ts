export enum ELocale {
  ENGLISH = 'en',
  HEBREW = 'he',
}

export const LOCALE_I18N_KEY: Record<ELocale, string> = {
  [ELocale.ENGLISH]: 'locale.english',
  [ELocale.HEBREW]: 'locale.hebrew',
}
