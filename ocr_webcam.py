import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    text = pytesseract.image_to_string(frame)

    print(text)

    cv2.imshow("OCR Camera", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()