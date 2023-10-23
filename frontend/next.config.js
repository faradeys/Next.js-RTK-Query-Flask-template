// @ts-nocheck
const { i18n } = require('./next-i18next.config')

/**
 * @type {import('next').NextConfig}
 **/
const nextConfig = {
  env: {
    BASE_API_URL: process.env.BASE_API_URL,
    RECAPTCHA_TOKEN: process.env.RECAPTCHA_TOKEN,
    DEBUG: process.env.DEBUG,
  },
  reactStrictMode: true,
  sassOptions: {
    additionalData: `@import "app/styles/utils/colors.scss"; @import "app/styles//utils/func.scss"; @import "app/styles/utils/mixins.scss"; @import "app/styles/utils/vars.scss";`,
  },
  i18n: {
    locales: i18n.locales,
    defaultLocale: i18n.defaultLocale,
    localeDetection: false,
  },
  output: 'standalone',
  // eslint-disable-next-line prefer-arrow/prefer-arrow-functions
  async rewrites() {
    return [
      {
        source: `${process.env.BASE_API_URL}/:path*`,
        destination: `${process.env.BASE_API_HOST}/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
