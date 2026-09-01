/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        ink: '#0f172a',
        treaty: '#2563eb',
        inst: '#ea580c',
        right: '#16a34a',
        exam: '#dc2626',
        mat: '#64748b',
      },
    },
  },
  plugins: [],
}
