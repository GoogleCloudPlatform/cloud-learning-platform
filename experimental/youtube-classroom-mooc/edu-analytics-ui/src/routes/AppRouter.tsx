import {
  Route,
  Routes,
} from 'react-router-dom'

import About from '@/routes/About'
import Home from '@/routes/Home'
import SignOut from '@/routes/SignOut'
import NotFound from '@/routes/NotFound'

interface AppRouterProps {
  
}
 
const AppRouter: React.FunctionComponent<AppRouterProps> = ({}) => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/about" element={<About />} />

      <Route path="/signout" element={<SignOut />} />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
 
export default AppRouter;
