/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          500: '#6d28d9',
          600: '#5b21b6',
        },
      },
    },
  },
  plugins: [],
}
