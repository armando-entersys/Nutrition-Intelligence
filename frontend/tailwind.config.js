/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3498db',
          dark: '#2980b9',
          light: '#5dade2',
        },
        secondary: {
          DEFAULT: '#27ae60',
          dark: '#229954',
          light: '#52be80',
        },
        accent: {
          orange: '#f39c12',
          red: '#e74c3c',
          purple: '#9b59b6',
        },
      },
    },
  },
  plugins: [],
}
