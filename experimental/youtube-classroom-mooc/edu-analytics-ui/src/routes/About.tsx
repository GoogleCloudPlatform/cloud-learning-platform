import { useTranslation } from 'next-i18next'

interface AboutProps {
  
}
 
const About: React.FunctionComponent<AboutProps> = ({}) => {
  const { t: tc } = useTranslation('common')

  return (
    <>
      <div className='text-xl font-bold mb-2'>
        {tc('app-title')}
      </div>

      {tc('app-description')}
    </>
  );
}
 
export default About;
