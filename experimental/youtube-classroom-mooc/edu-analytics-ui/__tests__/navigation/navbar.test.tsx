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

import { INavigationItem } from '@/utils/types'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Navbar from '@/navigation/Navbar'
import mockUser from '@/mocks/user'
import { BrowserRouter } from 'react-router-dom'

const mainRoutes: INavigationItem[] = [
  {
    name: 'Main Foo',
    href: '/main-foo',
  },
]

const userRoutes: INavigationItem[] = [
  {
    name: 'User Foo',
    href: '/user-foo',
  },
  {
    name: 'User Bar',
    href: '/user-bar',
  },
  {
    name: 'User Baz',
    href: '/user-baz',
  },
]

describe('Navbar', () => {
  it('contains links', async () => {
    render(
      <BrowserRouter>
        <Navbar user={mockUser} mainRoutes={mainRoutes} userRoutes={userRoutes} />
      </BrowserRouter>
    )

    const links = screen.getAllByRole('link')
    expect(links).toHaveLength(mainRoutes.length + 1) // The home route built into the Logo adds 1

    // Open user dropdown
    await waitFor(() => { // Must wait for animation
      fireEvent.click(screen.getByTestId('user-menu-button'))
      const moreLinks = screen.getAllByRole('link')
      expect(moreLinks).toHaveLength(userRoutes.length + mainRoutes.length + 1)
    })
  })

  it('shows users avatar', async () => {
    render(
      <BrowserRouter>
        <Navbar user={mockUser} mainRoutes={mainRoutes} userRoutes={userRoutes} />
      </BrowserRouter>
    )

    const img = await screen.findByTestId('user-img')

    // @ts-ignore
    expect(img.src).toEqual(mockUser.photoURL)
    // @ts-ignore
    expect(img.alt).toEqual(mockUser.displayName)
  })
})
