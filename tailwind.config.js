/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        'primary-green': '#16a34a',
        'dark-green': '#14532d',
        'light-green': '#d1fae5',
        'hover-green': '#15803d',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
      animation: {
        'fadeInUp': 'fadeInUp 0.3s ease-out',
        'slideInUp': 'slideInUp 0.6s ease-out',
        'pulse-green': 'pulse-green 2s infinite',
        'typing': 'typing 1.4s infinite ease-in-out',
        'float': 'float 15s infinite linear',
        'gradientShift': 'gradientShift 3s ease infinite',
      },
      keyframes: {
        fadeInUp: {
          'from': {
            opacity: '0',
            transform: 'translateY(20px)'
          },
          'to': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        slideInUp: {
          'from': {
            opacity: '0',
            transform: 'translateY(30px)'
          },
          'to': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        'pulse-green': {
          '0%': { boxShadow: '0 0 0 0 rgba(16, 185, 129, 0.7)' },
          '70%': { boxShadow: '0 0 0 10px rgba(16, 185, 129, 0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(16, 185, 129, 0)' }
        },
        typing: {
          '0%, 80%, 100%': { 
            transform: 'scale(0.8)', 
            opacity: '0.5' 
          },
          '40%': { 
            transform: 'scale(1)', 
            opacity: '1' 
          }
        },
        float: {
          '0%': {
            transform: 'translateY(100vh) rotate(0deg)',
            opacity: '0'
          },
          '10%': {
            opacity: '1'
          },
          '90%': {
            opacity: '1'
          },
          '100%': {
            transform: 'translateY(-100px) rotate(360deg)',
            opacity: '0'
          }
        },
        gradientShift: {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' }
        }
      },
      backgroundSize: {
        '200': '200% 200%'
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}