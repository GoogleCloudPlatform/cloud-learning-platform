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

import { ReactNode, useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { auth } from '@/utils/firebase'
import { userStore } from '@/store'
import Loading from '@/navigation/Loading'
import Authenticated from '@/templates/Authenticated'
import Unauthenticated from '@/templates/Unauthenticated'

type IMainProps = {
  meta: ReactNode
  children: ReactNode
}

const Main = (props: IMainProps) => {
  const router = useRouter()
  const [isLoading, setLoading] = useState(true)
  const user = userStore(state => state.user)
  const setUser = userStore(state => state.setUser)

  // Ensure only authenticated users can view items in the Main template
  useEffect(() => {

    if (!user) {
      router.push('/signin')
    }
  },[]);

  return user
    ? <Authenticated user={user} {...props} />
    : <Unauthenticated {...props} />

  // return (
  //   <div className="h-full w-full text-base-content">
  //     {props.meta}

  //     <div className="max-w-screen-xl mx-auto min-h-full flex flex-col">
  //       <Navbar user={user} mainRoutes={MainNavigation} userRoutes={UserNavigation} />
  //       <div className="flex-grow px-6 lg:px-8">
  //         {props.children}
  //       </div>
  //       <Footer routes={FooterNavigation} />
  //     </div>

  //   </div>
  // )
}
export { Main }
