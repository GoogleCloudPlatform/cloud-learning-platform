/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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
