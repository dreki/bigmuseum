module.exports = {
  theme: {
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      // sans: ['Rubik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    columnCount: [1, 2, 3, 4, 5]
  },
  plugins: [
    require('tailwindcss-multi-column')()
  ]
};
