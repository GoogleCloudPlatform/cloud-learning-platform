import { useEffect } from 'react'
// @ts-expect-error // No @types/theme-change available
import { themeChange } from 'theme-change'
interface ThemeChangerProps {
  themes: string[],
}
 
const ThemeChanger: React.FunctionComponent<ThemeChangerProps> = ({
  themes,
}) => {
  useEffect(() => {
    themeChange(false)
    // 👆 false parameter is required for react project
  }, [])

  return (
    <select className="select select-bordered" data-choose-theme>
      {themes.map(theme => 
        <option value={theme} key={theme}>{theme}</option>
      )}
    </select>
  );
}
 
export default ThemeChanger;
