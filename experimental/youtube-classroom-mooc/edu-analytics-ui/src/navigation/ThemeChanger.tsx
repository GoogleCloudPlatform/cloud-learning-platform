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
