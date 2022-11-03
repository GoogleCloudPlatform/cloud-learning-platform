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

import { ReactNode, useEffect } from 'react'

type IUnauthenticatedProps = {
  meta: ReactNode
  children: ReactNode
}

const Unauthenticated = (props: IUnauthenticatedProps) => {
  // NextJS doesn't allow editing this field with className
  useEffect(() => {
    document.querySelector('#__next')?.classList.add('h-full')
  })
  
  return (
    <div className="h-full w-full text-base-content">
      {props.meta}
  
      <div className="max-w-screen-xl mx-auto min-h-full">
        {props.children}
      </div>
  
    </div>
  )  
} 
export default Unauthenticated
