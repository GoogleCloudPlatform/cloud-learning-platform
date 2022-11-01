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

import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions'
import { getStorage, connectStorageEmulator } from 'firebase/storage'
import { OAuthScopes } from '@/utils/AppConfig'

const firebaseConfig = {
  apiKey:             process.env.NEXT_PUBLIC_FIREBASE_PUBLIC_API_KEY,
  authDomain:         process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId:          process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket:      process.env.NEXT_PUBLIC_FIREBASE_STORAGE_URL,
  messagingSenderId:  process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId:              process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  databaseURL:        process.env.NEXT_PUBLIC_FIREBASE_DATABASE_URL,
  measurementId:      process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
}

const app = initializeApp(firebaseConfig)

const auth = getAuth(app)
auth.useDeviceLanguage()

const db = getFirestore(app)
const functions = getFunctions(app)
const storage = getStorage(app)

const googleProvider = new GoogleAuthProvider()
OAuthScopes.forEach(scope => googleProvider.addScope(scope))


if (process.env.NODE_ENV === 'development') {
  connectStorageEmulator(storage, 'localhost', 9199)
  connectFunctionsEmulator(functions, 'localhost', 5001)
}

export {
  app,
  auth,
  db,
  functions,
  storage,
  googleProvider,
}
