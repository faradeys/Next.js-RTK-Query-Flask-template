module.exports = {
  i18n: {
    defaultLocale: 'ru',
    locales: ['ru', 'en'],
    defaultNS: 'lang',
    localeExtension: 'json',
    localeStructure: '{{lng}}/{{ns}}',
    localePath: typeof window === 'undefined' ? require('path').resolve('./public/locales') : '/locales',
  },
}
