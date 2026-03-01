import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pytesseract
import cv2
from PIL import Image, ImageTk
import os

# Set tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Camera App")
        self.root.geometry("900x650")

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack()

        self.btn_select = tk.Button(frame, text="Select Image", command=self.select_image)
        self.btn_select.grid(row=0, column=0, padx=5)

        self.btn_camera = tk.Button(frame, text="Open Camera", command=self.open_camera)
        self.btn_camera.grid(row=0, column=1, padx=5)

        self.btn_capture = tk.Button(frame, text="Capture Photo", command=self.capture_image)
        self.btn_capture.grid(row=0, column=2, padx=5)

        self.btn_ocr = tk.Button(frame, text="Run OCR", command=self.run_ocr)
        self.btn_ocr.grid(row=0, column=3, padx=5)

        self.text_area = scrolledtext.ScrolledText(root, width=100, height=15)
        self.text_area.pack(pady=10)

        self.btn_save = tk.Button(root, text="Save Text", command=self.save_text)
        self.btn_save.pack(pady=5)

        self.image_path = None
        self.cap = None
        self.current_frame = None

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.show_image(Image.open(file_path))

    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def update_camera(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img).resize((500, 350))
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            self.root.after(20, self.update_camera)

    def capture_image(self):
        if self.current_frame is not None:
            os.makedirs("output", exist_ok=True)
            path = "output/captured.png"
            cv2.imwrite(path, self.current_frame)
            self.image_path = path
            messagebox.showinfo("Captured", "Image captured successfully!")

    def preprocess_image(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
        return thresh

    def run_ocr(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected or captured")
            return

        processed = self.preprocess_image(self.image_path)
        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed, config=config)

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

        messagebox.showinfo("Saved", "Text saved to output/result.txt")

    def show_image(self, img):
        img = img.resize((500, 350))
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRCameraApp(root)
    root.mainloop()