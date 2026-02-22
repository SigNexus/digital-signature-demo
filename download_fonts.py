import os
import re
import requests

CSS_URLS = [
    "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap",
    "https://fonts.googleapis.com/icon?family=Material+Icons"
]

STATIC_DIR = "static"
FONTS_DIR = os.path.join(STATIC_DIR, "fonts")

if not os.path.exists(FONTS_DIR):
    os.makedirs(FONTS_DIR)

headers = {
    # Send a modern user agent to get woff2
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

all_css = []

for url in CSS_URLS:
    print(f"Fetching {url}...")
    res = requests.get(url, headers=headers)
    css_text = res.text
    
    # Find all url(https://...)
    urls = re.findall(r'url\((https://[^)]+)\)', css_text)
    
    for font_url in urls:
        filename = font_url.split("/")[-1]
        local_path = os.path.join(FONTS_DIR, filename)
        
        if not os.path.exists(local_path):
            print(f"Downloading {filename}...")
            font_res = requests.get(font_url)
            with open(local_path, "wb") as f:
                f.write(font_res.content)
        
        # Replace remote URL in CSS with local font path
        css_text = css_text.replace(font_url, f"/static/fonts/{filename}")
        
    all_css.append(css_text)

with open(os.path.join(STATIC_DIR, "fonts.css"), "w") as f:
    f.write("\n".join(all_css))

print("Fonts downloaded and CSS generated successfully!")
