import cv2

image1 = cv2.imread("O1-1.jpg")
image2 = cv2.imread("TabuleiroO1.jpg")

cv2.imshow("subtraida", cv2.subtract(image2, image1))
cv2.waitKey(0)