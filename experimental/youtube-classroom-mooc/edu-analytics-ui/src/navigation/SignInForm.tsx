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

import { useTranslation } from 'next-i18next'
import { signInWithPopup } from 'firebase/auth'
import { auth, googleProvider } from '@/utils/firebase'
import { useRouter } from 'next/router'
import { userStore } from '@/store'
import { useState } from 'react'
import { classNames } from '@/utils/dom'
import Loading from '@/navigation/Loading'


const SignInForm = () => {
  const { t: ts } = useTranslation('signin')
  const router = useRouter()

  const [submitting, setSubmitting] = useState(false)
  const setUser = userStore(state => state.setUser)
  
  const signin = async () => {
    setSubmitting(true)

    try {
      const { user } = await signInWithPopup(auth, googleProvider)
      if (!user.email) throw new Error('User is missing email')
      setUser({
        ...user,
        email: user.email,
      })
      router.push('/')
    } catch (error) {
      console.error(error)
      setSubmitting(false)
    }
  }

  return (
    <button onClick={signin} disabled={submitting}
      className={classNames(
        'btn bg-base-100 w-full shadow-lg border-base-300',
        submitting
          ? 'cursor-not-allowed text-base-content'
          : 'cursor-pointer hover:border-primary hover:bg-base-100',
      )}
    >
      {
        submitting ?
          <div className="mr-4">
            <Loading />
          </div> :
          <img
            className="h-8 w-auto mr-4"
            src="/assets/images/google.png"
            alt="Google"
          />
      }
      <div className="font-semibold text-base-content">{ts('signin-google')}</div>
    </button>
  )
}

export default SignInForm
