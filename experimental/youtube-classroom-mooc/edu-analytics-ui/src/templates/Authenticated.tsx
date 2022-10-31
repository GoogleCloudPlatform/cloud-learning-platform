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
