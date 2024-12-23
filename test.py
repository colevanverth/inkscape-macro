from PIL import Image 
 
# Open the image file 
image = Image.open("temp/22.png") 
 
# Convert the image to a format that can be copied to the clipboard 
image_data = Image.tobytes("jpeg") 
 
# Copy the image data to the clipboard 
pyperclip.copy(image_data) 
