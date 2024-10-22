import daisyui from "daisyui";
import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.js"],
  theme: {
    extend: {},
  },
  daisyui: {
    theme: [
      {
        'spotify-dark': {
          'base-100': '#100B12',
          'base-200': '#2C272E',
          'base-300': '#47404A',
          'neutral': '#A39CA6',
          'accent': '#53DD6C',
          'primary': '#753188',
          'secondary': '#E59934',
        }
      },
      {
        'spotify-light': {
          'base-100': '#FBFAFC',
          'base-200': '#F0EDF2',
          'base-300': '#E1DEE3',
          'neutral': '#BEB8C2',
          'accent': '#53DD6C',
          'primary': '#AF53C9',
          'secondary': '#F8AE4C',
        }
      }
    ]
  },
  plugins: [daisyui, typography],
}