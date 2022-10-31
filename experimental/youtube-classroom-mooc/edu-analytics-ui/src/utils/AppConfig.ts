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
