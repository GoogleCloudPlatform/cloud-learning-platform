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