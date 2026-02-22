import subprocess
import os
import shutil

# directory config
build_dir = ".tailwind_build"
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

# package.json
pkg = '''{
  "name": "tailwind-builder",
  "version": "1.0.0",
  "main": "index.js",
  "license": "MIT"
}'''
with open(f"{build_dir}/package.json", "w") as f:
    f.write(pkg)

# tailwind.config.js
tw_config = '''module.exports = {
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
}'''
with open(f"{build_dir}/tailwind.config.js", "w") as f:
    f.write(tw_config)

# input.css
with open(f"{build_dir}/input.css", "w") as f:
    f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")

# Install plugins
print("Installing tailwind dependencies...")
subprocess.run("npm install -D tailwindcss@3 @tailwindcss/forms @tailwindcss/container-queries", shell=True, cwd=build_dir)

# Build
print("Building tailwind CSS...")
subprocess.run("npx tailwindcss -i input.css -o output.css", shell=True, cwd=build_dir)

print("Done.")
