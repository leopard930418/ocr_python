import cv2
import pytesseract
from PIL import Image
import os

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMAGE_PATH = "images/sample.png"
OUTPUT_PATH = "output/result.txt"

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh

def extract_text(image):
    text = pytesseract.image_to_string(image, lang="rus")
    return text

def save_text(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    if not os.path.exists(IMAGE_PATH):
        print("Image not found!")
        return

    processed_image = preprocess_image(IMAGE_PATH)
    text = extract_text(processed_image)

    print("Extracted Text:")
    print(text)

    save_text(text, OUTPUT_PATH)
    print(f"Text saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
    