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
