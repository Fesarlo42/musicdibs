/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Georama", "sans-serif"],
        grace: ['"Covered By Your Grace"', "cursive"],
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["synthwave"],
  },
};
