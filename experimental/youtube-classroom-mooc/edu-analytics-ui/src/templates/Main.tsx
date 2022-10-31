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
