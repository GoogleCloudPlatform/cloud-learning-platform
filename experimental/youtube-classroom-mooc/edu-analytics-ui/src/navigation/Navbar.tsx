/* This example requires Tailwind CSS v2.0+ */
import { Fragment } from 'react'
// import { useRouter } from 'next/router'
import { Link, useMatch } from 'react-router-dom'
import { useTranslation } from 'next-i18next'

import { Disclosure, Menu, Transition } from '@headlessui/react'
import { MenuIcon, XIcon } from '@heroicons/react/outline'
import { AppConfig } from '@/utils/AppConfig'
import { classNames } from '@/utils/dom'
import { User } from 'firebase/auth'
import { INavigationItem } from '@/utils/types'
// @ts-ignore
import themes from "@/styles/themes"
import ThemeChanger from '@/navigation/ThemeChanger'


const Nav = ({
  user,
  mainRoutes,
  userRoutes,
}: {
  user: any,
  mainRoutes: INavigationItem[],
  userRoutes: INavigationItem[],
}) => {
  const { t } = useTranslation()
  
  return (
    <>
      <div className="min-h-full mb-8">
        <Disclosure as="nav" className="bg-base-100 border-b border-base-200">
          {({ open }) => (
            <>
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                  <div className="flex">
                    <Link to="/">
                      <div className="flex items-center shrink-0">
                        <img
                          className="mr-4"
                          src={AppConfig.logoPath}
                          alt={t('app-title')}
                          height={33}
                          width={41}
                        />
                        <div className='text-xl font-bold text-base-content'>
                          {t('app-title')}
                        </div>
                      </div>
                    </Link>

                   
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:items-center gap-x-2">

                    {/* <ThemeChanger themes={themes} /> */}

                    {/* Profile dropdown */}
                    <Menu as="div" className="ml-3 relative">
                      <Menu.Button data-testid="user-menu-button"
                        className="max-w-xs bg-base-100 flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">  
                        <span className="sr-only">Open user menu</span>
                          {user.profileObj.imageUrl ?
                            <img data-testid="user-img" className="h-8 w-8 rounded-full" src={user.profileObj.imageUrl} alt={user.profileObj.name || ''} />
                            : <></>
                          }
                      </Menu.Button>
                      <Transition
                        as={Fragment}
                        enter="transition ease-out duration-200"
                        enterFrom="transform opacity-0 scale-90"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-90"
                      >
                        <Menu.Items className="origin-top-right absolute z-10 right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-base-100 ring-1 ring-base-300 focus:outline-none">
                          {userRoutes.map((item) => (
                            <Menu.Item key={item.name}>
                              {({ active }) => (
                                <Link to={item.href}
                                  key={item.name}
                                  className={classNames(
                                    active
                                      ? 'text-primary bg-base-100'
                                      : 'text-base-content hover:bg-base-200',
                                    'block px-4 py-2 text-sm font-semibold'
                                  )}
                                >
                                  {t(item.name)}
                                </Link>
                              )}
                            </Menu.Item>
                          ))}
                        </Menu.Items>
                      </Transition>
                    </Menu>
                  </div>
                  <div className="-mr-2 flex items-center sm:hidden">
                    {/* Mobile menu button */}
                    <Disclosure.Button className="bg-base-100 inline-flex items-center justify-center p-2 rounded-md text-base-content hover:text-base-content hover:bg-base-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                      <span className="sr-only">Open main menu</span>
                      {open ? (
                        <XIcon className="block h-6 w-6" aria-hidden="true" />
                      ) : (
                        <MenuIcon className="block h-6 w-6" aria-hidden="true" />
                      )}
                    </Disclosure.Button>
                  </div>
                </div>
              </div>

              {/* Mobile Menu */}
              <Disclosure.Panel className="sm:hidden shadow-lg">
                <div className="pt-2 pb-3 space-y-1">
                  {mainRoutes.map((item) => (
                    <Link to={item.href} key={item.name}>
                      <Disclosure.Button
                        key={item.name}
                        as="div"
                        className={classNames(
                          useMatch(item.href)
                            ? 'bg-base-100 border-primary text-primary'
                            : 'border-transparent text-base-content hover:bg-base-200 hover:border-base-300',
                          'block pl-3 pr-4 py-2 border-l-4 text-base font-medium'
                        )}
                        aria-current={useMatch(item.href) ? 'page' : undefined}
                      >
                        {t(item.name)}
                      </Disclosure.Button>
                    </Link>
                  ))}
                </div>
                <div className="pt-4 pb-3 border-t border-base-200">
                  <div className="flex items-center px-4">
                    <div className="flex-shrink-0">
                    {user.profileObj.imageUrl ?
                            <img data-testid="user-img" className="h-8 w-8 rounded-full" src={user.profileObj.imageUrl} alt={user.profileObj.name || ''} />
                            : <></>
                          }
                    </div>
                    <div className="ml-3">
                      <div className="text-base font-medium text-base-content">{user?.profileObj?.name}</div>
                      <div className="text-sm font-medium text-base-content">{user?.profileObj?.email}</div>
                    </div>
                  </div>
                  <div className="mt-3 space-y-1">
                    {userRoutes.map((item) => (
                      <Link to={item.href} key={item.name}>
                        <Disclosure.Button
                          key={item.name}
                          as="div"
                          className="block px-4 py-2 text-base font-medium text-base-content hover:text-base-content hover:bg-base-200"
                        >
                          {t(item.name)}
                        </Disclosure.Button>
                      </Link>
                    ))}
                  </div>
                </div>
              </Disclosure.Panel>
            </>
          )}
        </Disclosure>
      </div>
    </>
  )
}

export default Nav
