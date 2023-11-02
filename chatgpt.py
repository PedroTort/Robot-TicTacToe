import cv2
import pytesseract

img = cv2.imread("jogodavelha.png")

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

resultado = pytesseract.image_to_string(img)

print(resultado)