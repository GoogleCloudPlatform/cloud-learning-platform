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

import React from 'react';
import { GoogleLogin } from 'react-google-login'
import { useRouter } from 'next/router'
import { userStore } from '@/store'

const GoogleSignIn = () => {

    const router = useRouter();
    const setUser = userStore(state => state.setUser)
    const onLoginSuccess = (response) => {
        console.log('user logged in', response)
        setUser(response)
        router.push('/')
    }

    const onLoginFailure = (err) => {
        console.log('login failed', err)
        setUser(null)
    }

    return (
        <GoogleLogin
            clientId="<INSERT_CLIENT_ID_HERE>"
            buttonText="Sign in with google"
            onSuccess={onLoginSuccess}
            onFailure={onLoginFailure}
            cookiePolicy={'single_host_origin'}
        />
    )
}

export default GoogleSignIn;