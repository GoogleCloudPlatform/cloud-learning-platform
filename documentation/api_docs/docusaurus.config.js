// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/palenight');

const appUrl = `https://${process.env.API_DOMAIN}`;

if (!appUrl) {
  throw Error("app url is not provided")
}


let clpServices = require("./clp_services.json")
let redocusaurusSpecs = []


for (let service of clpServices) {
  let data = {
    route: service.route,
    spec: `${appUrl}${service.spec}`
  }
  redocusaurusSpecs.push(data)
}


/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Cloud Learning Platform',
  tagline: 'CLP',
  url: appUrl,
  baseUrl: '/docs/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Google', // Usually your GitHub org/user name.
  projectName: 'Cloud Learning Platform', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: require.resolve('./sidebars.js')
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
    [
      'redocusaurus',
      {
        specs: [...redocusaurusSpecs],
        // Theme Options for modifying how redoc renders them
        theme: {
          // Change with your site colors
          primaryColor: '#1890ff',
        },
      },
    ]
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      releaseTag: process.env.RELEASE_TAG ?? null,
      navbar: {
        title: 'Cloud Learning Platform',
        items: [
          {
            type: "custom-logout-button",
            position: 'right'
          }
        ],
      },
      docs: {
        sidebar: {
          hideable: true,
        },
      },
      // footer: {
      //   style: 'dark',
      //   copyright: `Copyright © ${new Date().getFullYear()} Cloud Learning Platform`,
      // },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
  plugins: [
    [
      'docusaurus2-dotenv',
      {
        // path: "./.env",
        systemvars: true
      }
    ]
  ]
};

module.exports = config;
