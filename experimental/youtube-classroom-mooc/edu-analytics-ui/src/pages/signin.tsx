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

import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { useTranslation } from 'next-i18next'

import { Meta } from '@/layout/Meta'
import Unauthenticated from '@/templates/Unauthenticated'
import SignInForm from '@/navigation/SignInForm'
import GoogleSignIn from '@/navigation/GoogleSignIn'
import { AppConfig } from '@/utils/AppConfig'

const Signin = () => {
  const { t } = useTranslation('common')
  const { t: ts } = useTranslation('signin')

  return (
    <Unauthenticated meta={<Meta title={ts('signin-title')} description={ts('signin-description')} />}>
      <div className="bg-base-100 min-h-screen px-4 md:px-10">
        <div className="flex justify-center items-center min-h-screen max-w-6xl">

          <div className="mx-auto w-3/4 md:w-1/2 text-center">
            <div className='flex items-center justify-center'>
              <img
                className="h-10 w-auto mr-2"
                src={AppConfig.logoPath}
                alt={t('app-title')}
              />
              <div className='text-xl text-center font-semibold'>
                {t('app-title')}
              </div>
            </div>

            <div className='mt-4 mb-16'>
              {t('app-description')}
            </div>

            <div className="sm:px-20 md:px-10 lg:px-0 xl:px-20">
              {/* <SignInForm /> */}<GoogleSignIn />
            </div>
          </div>

        </div>
      </div>
    </Unauthenticated>
  )
}

export async function getServerSideProps({ locale }: { locale: string }) {
  return {
    props: {
      ...(await serverSideTranslations(locale, ['common', 'signin'])),
    }
  }
}

export default Signin

