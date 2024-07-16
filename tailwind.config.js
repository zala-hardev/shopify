/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './apps/templates/*.html',
    './apps/templates/admin_panel/*.html',
    './apps/static/js/*.js',  // Include paths to your JS files if you use them
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

