import Document, { Html, Head, Main, NextScript } from 'next/document'
import { AppConfig } from '@/utils/AppConfig'

// Need to create a custom _document because i18n support is not compatible with `next export`.
class MyDocument extends Document {
  render() {
    return (
      <Html
        className='h-full text-base-content bg-base-100'
        lang={AppConfig.locale}
        data-theme={'light'}
      >
        <Head />
        <body className='h-full antialiased'>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
