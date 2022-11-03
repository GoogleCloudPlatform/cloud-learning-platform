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

import { useEffect } from 'react'
import { AppProps } from 'next/app'
import { appWithTranslation } from 'next-i18next'
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check'
import { app } from '@/utils/firebase'

import '../styles/global.css'

let initRecaptcha = false
  
const MyApp = ({ Component, pageProps }: AppProps) => {

  // Enable Firebase App Check
  const recaptchaKey = process.env.NEXT_PUBLIC_RECAPTCHA_PUBLIC_SITE_KEY
  useEffect(() => {
    if (recaptchaKey && !initRecaptcha) {
      initializeAppCheck(app, {
        provider: new ReCaptchaV3Provider(recaptchaKey),
        isTokenAutoRefreshEnabled: true,
      })
    }
    initRecaptcha = true
  })

  return (
    <div suppressHydrationWarning className="min-h-screen h-full">
      {typeof window === 'undefined' ? null : <Component {...pageProps} />}
    </div>
  )
}

export default appWithTranslation(MyApp)
