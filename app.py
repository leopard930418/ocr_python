import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pytesseract
import cv2
from PIL import Image, ImageTk
import os

# Set tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Desktop App")
        self.root.geometry("800x600")

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.btn_select = tk.Button(root, text="Select Image", command=self.select_image)
        self.btn_select.pack(pady=5)

        self.btn_ocr = tk.Button(root, text="Run OCR", command=self.run_ocr)
        self.btn_ocr.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(root, width=90, height=15)
        self.text_area.pack(pady=10)

        self.btn_save = tk.Button(root, text="Save Text", command=self.save_text)
        self.btn_save.pack(pady=5)

        self.image_path = None

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img = img.resize((400, 300))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def preprocess_image(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
        return thresh

    def run_ocr(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first")
            return

        processed = self.preprocess_image(self.image_path)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed, config=custom_config)

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)

    def save_text(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to save")
            return

        os.makedirs("output", exist_ok=True)
        with open("output/result.txt", "w", encoding="utf-8") as f:
            f.write(text)

        messagebox.showinfo("Success", "Text saved to output/result.txt")


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()