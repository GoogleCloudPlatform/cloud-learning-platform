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
import { BrowserRouter } from 'react-router-dom'

import AppRouter from '@/routes/AppRouter'
import Footer from '@/navigation/Footer'
import Navbar from '@/navigation/Navbar'
import {
  MainNavigation,
  UserNavigation,
  FooterNavigation,
} from '@/utils/AppConfig'

interface AuthenticatedProps {
  meta: React.ReactNode
  children: React.ReactNode
  user: User
}
 
const Authenticated: React.FunctionComponent<AuthenticatedProps> = ({
  meta,
  user
  // children, // NextJS children Nodes
}) => {
  return (
    <BrowserRouter>
      <div className="h-full w-full text-base-content">
        {meta}
    
        <div className="max-w-screen-xl mx-auto min-h-full flex flex-col">
          <Navbar user={user} mainRoutes={MainNavigation} userRoutes={UserNavigation} />
          <div className="flex-grow px-6 lg:px-8">
            <AppRouter />
          </div>
          <Footer routes={FooterNavigation} />
        </div>
    
      </div>
    </BrowserRouter>
  )
}
 
export default Authenticated;
