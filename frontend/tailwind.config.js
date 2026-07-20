/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: {
    extend: {
      colors: {
        ember: {
          400: "#fb923c",
          500: "#f97316",
        },
      },
    },
  },
  plugins: [],
};
