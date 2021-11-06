module.exports = {
  theme: {
    fontFamily: {
      // sans: ['Graphik', 'sans-serif'],
      // sans: ['Zen Maru Gothic', 'sans-serif'],
      // sans: ['Work Sans', 'sans-serif'],
      // sans: ['Palanquin', 'sans-serif'],
      // sans: ['Mulish', 'sans-serif'],
      'work-sans': ['Work Sans', 'sans-serif'],

      sans: ['Rubik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    columnCount: [1, 2, 3, 4, 5],

    extend: {
      colors: {
        'moody-blue': {
          '50': '#f8f8fd',
          '100': '#f2f1fa',
          '200': '#dedcf3',
          '300': '#cac7eb',
          '400': '#a39ddd',
          '500': '#7b73ce',
          '600': '#6f68b9',
          '700': '#5c569b',
          '800': '#4a457c',
          '900': '#3c3865'
        }
      },
      'wewak': {
        '50': '#fefbfb',
        '100': '#fef7f7',
        '200': '#fceaea',
        '300': '#fadddd',
        '400': '#f7c4c4',
        '500': '#f3abaa',
        '600': '#db9a99',
        '700': '#b68080',
        '800': '#926766',
        '900': '#775453'
      },
      'corvette': {
        '50': '#fffdfb',
        '100': '#fffbf6',
        '200': '#fef5e9',
        '300': '#fdefdc',
        '400': '#fce4c1',
        '500': '#fbd8a7',
        '600': '#e2c296',
        '700': '#bca27d',
        '800': '#978264',
        '900': '#7b6a52'
      },
      'shadow-green': {
        '50': '#fafcfc',
        '100': '#f4f9f9',
        '200': '#e4f0f0',
        '300': '#d4e7e7',
        '400': '#b3d6d6',
        '500': '#93c4c4',
        '600': '#84b0b0',
        '700': '#6e9393',
        '800': '#587676',
        '900': '#486060'
      }
    }
  },
  plugins: [
    require('tailwindcss-multi-column')(),
    require('tailwindcss-break')(),
  ]
};
