/** @type {import('tailwindcss').Config} */
console.log('Tailwind config is loading');
module.exports = {
  content: ["./src/**/*.{html,tsx}"],
  theme: {
    extend: {
      colors: {
        'custom-blue': '#007ace',
        'custom-pink': '#ff49db',
        'custom-green': '#13ce66',
        'custom-orange': '#ff7849',
        'msg-resp-gray': '#a9a9a9',

      },
    }
  },
  plugins: [],
}

