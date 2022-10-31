import { useTranslation } from 'next-i18next'
import Student from '@/components/Student';
import Tutor from '@/components/Tutor';
import { userStore } from '@/store'
interface HomeProps {

}

const Home: React.FunctionComponent<HomeProps> = ({

}) => {
  const { t } = useTranslation('home')
  const user = userStore(state => state.user)
  const isStudent = user.profileObj.email === "INSERT_FACULT_EMAIL" ? false : true;
  return (

    <>
      {isStudent ? <Student /> : <Tutor />}
    </>
  );
}

export default Home;
