import cv2
import pytesseract
import numpy as np

def get_circles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    cv2.imshow("gray", gray)
    gray_blurred = cv2.blur(gray, (3, 3)) 
    cv2.imshow("blur", gray_blurred)
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 1, maxRadius = 40) 
    
    # desenhando os circulos detectados (precisamos desenhar msm, n eh soh pegar se tem ou n?)
    if detected_circles is not None: 
    # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            # cv2.imshow("Detected Circle", img)
            # # cv2.imwrite("circulo1.png", img) 
            # cv2.waitKey(0) 
            return img
    return None
            
    
    # fazer retornar uma flag, caso ele tenha detectado um circulo no quadrado da matriz, pra fazer a jogada e remover quadrado da leitura

# for i in range(0,9):
#      k=i+1
#      if(k%3==0):
#           j=3
#      else:
#           j=k%3
#      k=int(i/3)+1
#      imagem_cortada_com_x_tratada = cv2.imread(f"imagem_cortada_com_x_final{k}{j}.png")
#      cv2.imwrite(f"{k}{j}.png",get_circles(imagem_cortada_com_x_tratada))


image1 = cv2.imread("print1.png")
img1 = get_circles(image1)
if img1 is not None:
    cv2.imwrite(f"aa.png",img1)
else:
    print("ola")