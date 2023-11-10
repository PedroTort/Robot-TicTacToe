import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob 
# img = cv2.imread('3.jpeg', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('3.jpeg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# aplicando o filtro gaussiano 
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv2.Canny(img_blur,100,200)



# cv2.imshow("Resutado", edges) 
# cv2.imwrite("Resutado.png", edges) 

kernel = np.ones((9,9))
inchado = cv2.dilate(edges, kernel, iterations=1)

# cv2.imshow("dilatado", inchado) 
# cv2.imwrite("dilatado.png", inchado) 

kernel = np.ones((5,5))
erodido = cv2.erode(inchado, kernel, iterations=1)

# cv2.imshow("erodido", erodido) 
# cv2.imwrite("erodido.png", erodido) 

# cv2.waitKey(0) 
# cv2.destroyWindow("Imagem") 
# glob.os.remove("Imagem.png")

plt.subplot(121),plt.imshow(inchado,cmap = 'gray')
plt.title('Inchado'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(erodido,cmap = 'gray')
plt.title('Erodido'), plt.xticks([]), plt.yticks([])
plt.show()