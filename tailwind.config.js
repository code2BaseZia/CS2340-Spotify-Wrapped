import daisyui from "daisyui";

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.js"],
  safelist: ['text-success', 'text-danger'],
  theme: {
    extend: {
      fontFamily: {
        'title': ['area-normal', 'sans-serif'],
        'body': ['indivisible', 'sans-serif'],
      },
      gridTemplateColumns: {
        'content-lg': 'repeat(12, 4.5rem)',
        'content-md': 'repeat(8, 4.5rem)',
        'content-sm': 'repeat(4, 4.5rem)',
      }
    },
  },
  daisyui: {
    themes: [
      {
        spotifyDark: {
          'base-100': '#2C272E',
          'base-200': '#38323B',
          'base-300': '#47404A',
          'neutral': '#6d6670',
          'accent': '#53DD6C',
          'primary': '#753188',
          'secondary': '#E59934',
        }
      },
      {
        spotifyLight: {
          'base-100': '#FBFAFC',
          'base-200': '#F0EDF2',
          'base-300': '#E1DEE3',
          'neutral': '#c1bbc4',
          'accent': '#53DD6C',
          'primary': '#AF53C9',
          'secondary': '#F8AE4C',
        }
      }
    ]
  },
  plugins: [daisyui],
}