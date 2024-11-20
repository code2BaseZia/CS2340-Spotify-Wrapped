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
        'display': ['area-extended', 'sans-serif']
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
      },
      {
        wrapped1: {
          'base-100': '#000000',
          'base-200': '#111111',
          'base-300': '#222222',
          'neutral': '#98CE00',
          'accent': '#FFC600',
          'primary': '#5800FF',
          'secondary': '#E900FF',
        },
        wrapped2: {
          'base-100': '#000000',
          'base-200': '#111111',
          'base-300': '#222222',
          'neutral': '#56E39F',
          'accent': '#EBF400',
          'primary': '#F72798',
          'secondary': '#F57D1F',
        },
        wrapped3: {
          'base-100': '#1C2321',
          'base-200': '#2D3432',
          'base-300': '#3E4543',
          'neutral': '#00F5FF',
          'accent': '#FF6D28',
          'primary': '#EA047E',
          'secondary': '#FCE700',
        },
        wrapped4: {
          'base-100': '#1a0033',
          'base-200': '#28004d',
          'base-300': '#350066',
          'neutral': '#7C00FE',
          'accent': '#F5004F',
          'primary': '#FFAF00',
          'secondary': '#F9E400',
        },
        wrapped5: {
          'base-100': '#FFB84C',
          'base-200': '#e6a545',
          'base-300': '#cc933d',
          'neutral': '#BFFFBC',
          'accent': '#2CD3E1',
          'primary': '#F266AB',
          'secondary': '#A459D1'
        },
        wrapped6: {
          'base-100': '#FF85B3',
          'base-200': '#e677a2',
          'base-300': '#cc708f',
          'neutral': '#F900BF',
          'accent': '#73EEDC',
          'primary': '#4700D8',
          'secondary': '#9900F0'
        },
      }
    ]
  },
  plugins: [daisyui],
}