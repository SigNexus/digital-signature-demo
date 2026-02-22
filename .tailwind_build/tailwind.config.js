module.exports = {
  content: ["../index.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#f20d33",
        "background-light": "#f8f5f6",
        "background-dark": "#1a0a0c",
      },
      fontFamily: {
        "display": ["Space Grotesk"]
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}