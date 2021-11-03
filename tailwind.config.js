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
    columnCount: [1, 2, 3, 4, 5]
  },
  plugins: [
    require('tailwindcss-multi-column')(),
    require('tailwindcss-break')(),
  ]
};
