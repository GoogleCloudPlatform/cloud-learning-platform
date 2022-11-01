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

import { User } from 'firebase/auth'

const user: User = {
  uid: '1',
  displayName: 'Thomas Kurian',
  email: 'tk@acme.com',
  emailVerified: true,
  phoneNumber: '123456789',
  photoURL: 'https://lh3.googleusercontent.com/a-/AOh14GgeGwCRNIALP_N6QtZHVwZv-DFDorGkHNYNL8s=s96-c',
  tenantId: null,
  reload: () => Promise.resolve(),
  isAnonymous: false,
  metadata: {},
  providerId: 'google',
  providerData: [],
  refreshToken: '',
  getIdToken: () => Promise.resolve(''),
  getIdTokenResult: () => Promise.resolve({
    authTime: '',
    expirationTime: '',
    issuedAtTime: '',
    signInProvider: null,
    signInSecondFactor: null,
    token: '',
    claims: {},
  }),
  delete: () => Promise.resolve(),
  toJSON: () => ({}),
}

export default user
