/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

const themes = require('./src/styles/themes')

module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    // Omit Tailwind colors. Use DaisyUI colors instead
    colors: {},
    extend: {
      screens: {
        'xs': '480px',
      },
    },
  },
  variants: {
    backgroundColor: ['active'],
  },
  daisyui: {
    // https://daisyui.com/docs/themes/
    themes: [
      ...themes,
      {
        light: {
          ...require('daisyui/src/colors/themes')['[data-theme=light]'],
          "base-100": "#ffffff",
          "base-200": "#f1f5f9",
          "base-300": "#e2e8f0",
          
          "primary": "#4885ed",
          "secondary": "#3cba54",
          "accent": "#f4c20d",
          "neutral": "#0f172a",

          "info": "#93c5fd",
          "success": "#86efac",
          "warning": "#fde047",
          "error": "#fca5a5",
        },
      },
      {
        dark: {
          ...require('daisyui/src/colors/themes')['[data-theme=dark]'],
          "primary": "#a78bfa",
          "base-content": "#f5f3ff",
        },
      },
    ],
  },
  plugins: [
    require('@tailwindcss/forms'),
    require("daisyui"),
  ],
};
