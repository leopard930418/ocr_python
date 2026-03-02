import tkinter as tk
from tkinter import messagebox, scrolledtext
import pytesseract
import cv2
from PIL import Image, ImageTk
import os

# Set tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRBoundingBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Camera with Bounding Boxes")
        self.root.geometry("900x650")

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Open Camera", command=self.open_camera).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Capture Image", command=self.capture_image).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Run OCR + Boxes", command=self.run_ocr).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Save Text", command=self.save_text).grid(row=0, column=3, padx=5)

        self.text_area = scrolledtext.ScrolledText(root, width=100, height=12)
        self.text_area.pack(pady=10)

        self.cap = None
        self.current_frame = None
        self.image_path = None

    def open_camera(self):
        # self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.update_camera()

    def update_camera(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()  # IMPORTANT: use copy()

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img).resize((500, 350))
                photo = ImageTk.PhotoImage(img)

                self.image_label.config(image=photo)
                self.image_label.image = photo

        self.root.after(20, self.update_camera)
        print("Frame received:", self.current_frame is not None)
    def capture_image(self):
        if self.current_frame is None:
            messagebox.showerror("Error", "No frame captured from camera")
            return

        os.makedirs("output", exist_ok=True)
        path = "output/captured.png"
        cv2.imwrite(path, self.current_frame)
        self.image_path = path

        messagebox.showinfo("Success", "Image captured!")
    def preprocess_image(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
        return img, thresh

    def run_ocr(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image captured")
            return

        original_img, processed = self.preprocess_image(self.image_path)

        data = pytesseract.image_to_data(processed, config="--psm 6", output_type=pytesseract.Output.DICT)

        extracted_text = ""

        for i in range(len(data["text"])):
            if int(data["conf"][i]) > 60:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]
                text = data["text"][i]

                extracted_text += text + " "

                cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(original_img, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb).resize((500, 350))
        photo = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, extracted_text)

    def save_text(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to save")
            return

        os.makedirs("output", exist_ok=True)
        with open("output/result.txt", "w", encoding="utf-8") as f:
            f.write(text)

        messagebox.showinfo("Saved", "Text saved to output/result.txt")


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRBoundingBoxApp(root)
    root.mainloop()