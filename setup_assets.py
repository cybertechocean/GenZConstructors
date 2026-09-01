import os
import shutil
from PIL import Image

WORKSPACE = r"c:\Users\ADMIN\Documents\GitHub\GenZConstructors"
SRC_LOGO = r"C:\Users\ADMIN\.gemini\antigravity-ide\brain\ce75d2c5-f19f-476f-973a-e1f4d50b3736\.user_uploaded\media_1788256711211.jpg"

static_img_dir = os.path.join(WORKSPACE, "static", "images")
media_dir = os.path.join(WORKSPACE, "media", "branding")
os.makedirs(static_img_dir, exist_ok=True)
os.makedirs(media_dir, exist_ok=True)

# Copy original logo
dest_logo = os.path.join(static_img_dir, "logo.jpg")
shutil.copyfile(SRC_LOGO, dest_logo)
shutil.copyfile(SRC_LOGO, os.path.join(media_dir, "logo.jpg"))

print(f"Copied logo to {dest_logo}")

# Load with PIL and create favicons
img = Image.open(SRC_LOGO)
# Favicon .ico containing multiple sizes
img.save(os.path.join(static_img_dir, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# PNG favicons and app icons
img.resize((16, 16), Image.Resampling.LANCZOS).save(os.path.join(static_img_dir, "favicon-16x16.png"), format="PNG")
img.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(static_img_dir, "favicon-32x32.png"), format="PNG")
img.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(static_img_dir, "apple-touch-icon.png"), format="PNG")
img.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(static_img_dir, "android-chrome-192x192.png"), format="PNG")
img.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(static_img_dir, "android-chrome-512x512.png"), format="PNG")

# Open Graph social preview image (1200x630 on navy canvas)
og_img = Image.new("RGB", (1200, 630), color="#010B20")
logo_resized = img.resize((500, 500), Image.Resampling.LANCZOS)
# Paste in center
og_img.paste(logo_resized, (350, 65))
og_img.save(os.path.join(static_img_dir, "og-image.jpg"), format="JPEG", quality=95)

print("Generated all favicon and brand assets successfully!")
