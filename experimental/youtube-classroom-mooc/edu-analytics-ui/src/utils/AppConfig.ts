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

// Make sure you update your public/locales JSON files
export const AppConfig = {
  siteName: 'Rapid Integration Service',
  locale: 'en',
  logoPath: '/assets/images/gcp.png',
  theme: 'light',
}

// These are i18n link names, put the label in the common.json file
export const MainNavigation: INavigationItem[] = [
  { name: 'link-about', href: '/about' },
  { name: 'link-1',     href: '/link1' },
  { name: 'link-2',     href: '/link2' },
]

export const UserNavigation: INavigationItem[] = [
  { name: 'link-profile',   href: '/profile' },
  { name: 'link-settings',  href: '/settings' },
  { name: 'link-signout',   href: '/signout' },
]

export const FooterNavigation: INavigationItem[] = [
  { name: 'link-about',      href: '/about' },
]

// Full list of scopes: https://developers.google.com/identity/protocols/oauth2/scopes
export const OAuthScopes: string[] = [

]
