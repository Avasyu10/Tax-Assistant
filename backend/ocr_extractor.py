import cv2
import pytesseract

def extract_expenses(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    expenses = [line for line in text.split("\n") if "$" in line]
    return expenses
