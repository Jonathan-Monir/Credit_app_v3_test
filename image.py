from PIL import Image

# Open the image
img = Image.open("images/RD.png")

# Resize the image to 5x5 pixels
resized_img = img.resize((5, 5))

# Save the resized image
resized_img.save("resized_RD.png")
