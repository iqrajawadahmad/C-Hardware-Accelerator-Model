from PIL import Image

# Open JPEG/PNG
img = Image.open("image.jpg")  # change filename
img = img.convert("RGB")        # ensure RGB

# Save as PPM P6 binary
img.save("input.ppm", format="PPM")

print("Converted input.jpg → input.ppm successfully!")