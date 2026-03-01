import pytesseract
from PIL import Image

# Set tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("images/sample.png")

text = pytesseract.image_to_string(img)

print("Extracted Text:")
print(text)