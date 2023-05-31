import React, { useState, useEffect } from 'react';
import { auth, googleProvider, getCurrentLoginStatus, passLoginConditions } from '../contexts/firebase';
import LoginPage from '../components/LoginPage/LoginPage';
import Loading from '../components/Loading/Loading';
import { signInWithPopup, signInWithEmailAndPassword } from 'firebase/auth';

export default function Root({ children }) {
  const [isLoading, setLoading] = useState(true);
  const [isLoggedIn, setLoginStatus] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const status = getCurrentLoginStatus()
    setLoginStatus(status)
    setTimeout(() => {
      setLoading(false)
    }, 1000);
  }, []);

  auth.onAuthStateChanged(function (user) {
    if (!user) {
      typeof window !== "undefined" && localStorage.removeItem("idToken")
      setLoginStatus(false);
      // logout actions
      // if user had logged in before in running state, then redirect the page to default route  
      if (isLoggedIn == true) {
        location.replace("/docs");
      }
    }
  });

  const signInWithCred = async (email, password) => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      setErrorMessage("")
      setLoginStatus(true)
    } catch (err) {
      setLoginStatus(false)
      if (err?.code == "auth/user-not-found" || err?.code == "auth/wrong-password") {
        setError("Invalid credentials")
      } else {
        setError("Something went wrong")
      }
    }
  };

  const signInWithGoogle = async () => {
    try {
      const res = await signInWithPopup(auth, googleProvider);
      const passedConditions = await passLoginConditions()
      setLoginStatus(passedConditions.status)
      setError(passedConditions.msg)
    } catch (err) {
      setError("Please try again")
    }
  };

  const setError = (msg) => {
    setErrorMessage(msg)
    setTimeout(() => {
      setErrorMessage("")
    }, 5000);
  }

  return (
    <React.Fragment>
      {isLoading ?
        <Loading />
        :
        isLoggedIn ? (
          <>{children}</>
        ) : (
          <LoginPage submit={signInWithCred} signInWithGoogle={signInWithGoogle} errorMessage={errorMessage} />
        )}
    </React.Fragment>
  );
}