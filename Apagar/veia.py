import cv2
import numpy as np
from operator import itemgetter

# processando a imagem!
def process(img):
     # convercao de RGB para BGR e grayscale
     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     # aplicando o filtro gaussiano 
     img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
     # detectando as bordas
     img_canny = cv2.Canny(img_blur, 100, 200)
     # retorna um array com o tamanho (9,9 (?)) preenchido com 1
     kernel = np.ones((9, 9))
     # dilatando a imagem
     img_dilate = cv2.dilate(img_canny, kernel, iterations=1)
     # kernel = np.ones((5,5))
     # erodindo a imagem
     return cv2.erode(img_dilate, kernel, iterations=1)

def process_symbols(img):
     kernel = np.ones((3, 3))
     img_erode =  cv2.erode(img, kernel, iterations=1)
     img_dilate = cv2.dilate(img_erode, kernel, iterations=1)
     return img_dilate

# achando os contornos!
def convex_hull(cnt):
     # distancia maxima do contorno pra um contorno aproximado, eh o que garante um bom contorno (eh um parametro de precisao)
     # calcula o perimetor do contorno!
     epsilon = cv2.arcLength(cnt, True)
     # aproximacao dos poligonos com a precisao do epsilon
     approx = cv2.approxPolyDP(cnt, epsilon * 0.02, True)
     # corrige uma "curva" defeituosa do contorno
     return cv2.convexHull(approx).squeeze()

# recebe
def get_square_corners(inner, outer): 

     ordenando_indice_x = inner[...,0].argsort()
     ordenando_x_menor = sorted(inner[ordenando_indice_x], key=itemgetter(0))
     print(type(inner))

     lista_x_menor = np.array(ordenando_x_menor[0:2])
     lista_x_maior = np.array(ordenando_x_menor[2:])

     ordenando_indice_y_menor = lista_x_menor[...,1].argsort()
     top_lef_inner, bot_lef_inner = sorted(lista_x_menor[ordenando_indice_y_menor], key=itemgetter(1))
     
     ordenando_indice_y_maior = lista_x_maior[...,1].argsort()
     top_rit_inner, bot_rit_inner = sorted(lista_x_maior[ordenando_indice_y_maior], key=itemgetter(1))

     # pegando todas as linhas e coluna 0, e fazendo um sort com os indices (da coluna do eixo X)! (ordem crescente)
     sort_outer_index_x0 = outer[..., 0].argsort()
     # pegando todas as linhas e coluna 1, e fazendo um sort com os indices (da coluna do eixo Y)! (ordem crescente)
     sort_outer_index_y1 = outer[..., 1].argsort()

     # definindo os pontos laterais
     ordenando_x_menor = sorted(outer[sort_outer_index_x0], key=itemgetter(0))
     ordenando_y_menor = sorted(outer[sort_outer_index_y1], key=itemgetter(1))

     lista_x_menor = np.array(ordenando_x_menor[0:2])
     lista_x_maior = np.array(ordenando_x_menor[6:])

     ordenando_indice_y_menor = lista_x_menor[...,1].argsort()

     left_top_outer, left_bot_outer = sorted(lista_x_menor[ordenando_indice_y_menor], key=itemgetter(1))
     
     ordenando_indice_y_maior = lista_x_maior[...,1].argsort()
     rig_top_outer, rig_bot_outer = sorted(lista_x_maior[ordenando_indice_y_maior], key=itemgetter(1))

     # definindo
     lista_y_menor = np.array(ordenando_y_menor[0:2])
     lista_y_maior = np.array(ordenando_y_menor[6:])

     ordenando_indice_x_menor = lista_y_menor[...,1].argsort()
     top_left_outer, top_rit_outer = sorted(lista_y_menor[ordenando_indice_x_menor], key=itemgetter(0))
     
     ordenando_indice_x_maior = lista_y_maior[...,1].argsort()
     bot_left_outer, bot_rit_outer = sorted(lista_y_maior[ordenando_indice_x_maior], key=itemgetter(0))


     # calculando os pontos que nao temos
     top_left_zero = top_left_outer + left_top_outer - top_lef_inner 
     bot_left_zero = bot_left_outer + left_bot_outer - bot_lef_inner
     top_rit_zero = top_rit_outer + rig_top_outer - top_rit_inner
     bot_rit_zero = bot_rit_outer + rig_bot_outer - bot_rit_inner
     # yield np.mean ([bot_rit_outer],0)

     # yield np.mean ([top_left_zero],0)
     # yield np.mean ([top_lef_inner],0)
     # yield np.mean ([left_top_outer],0)

     quadrado_11 = [top_left_zero, top_left_outer, top_lef_inner, left_top_outer]
     quadrado_12 = [top_left_outer, top_rit_outer, top_rit_inner, top_lef_inner]
     quadrado_13 = [top_rit_outer, top_rit_zero, rig_top_outer, top_rit_inner]
     quadrado_21 = [left_top_outer, top_lef_inner, bot_lef_inner, left_bot_outer]
     quadrado_22 = [top_lef_inner, top_rit_inner, bot_rit_inner, bot_lef_inner]
     quadrado_23 = [top_rit_inner, rig_top_outer, rig_bot_outer, bot_rit_inner]
     quadrado_31 = [left_bot_outer, bot_lef_inner, bot_left_outer, bot_left_zero]
     quadrado_32 = [bot_lef_inner, bot_rit_inner, bot_rit_outer, bot_left_outer]
     quadrado_33 = [bot_rit_inner, rig_bot_outer, bot_rit_zero, bot_rit_outer]

     # yield np.mean(quadrado_11,0)
     # yield np.mean(quadrado_12,0)
     # yield np.mean(quadrado_13,0)
     # yield np.mean(quadrado_21,0)
     # yield np.mean(quadrado_22,0)
     # yield np.mean(quadrado_23,0)
     # yield np.mean(quadrado_31,0)
     # yield np.mean(quadrado_32,0)
     # yield np.mean(quadrado_33,0)

     quadrados = [quadrado_11, quadrado_12, quadrado_13, quadrado_21, quadrado_22, quadrado_23, quadrado_31, quadrado_32, quadrado_33]

     return quadrados

# recebe os 4 vertices para cortar na imagem      
def get_squares_init(pontos_quadrado):

     # https://stackoverflow.com/questions/48301186/cropping-concave-polygon-from-image-using-opencv-python

     # criando um retangulo com os vertices
     rect_corte = cv2.boundingRect(pontos_quadrado)
     # passando as coordenadas para as variaveis
     x,y,w,h = rect_corte
     # cortando a imagem com as variaveis
     croped = img_processada[y:y+h, x:x+w].copy()

     # fazendo mascara para o corte da imagem
     pontos_quadrado = pontos_quadrado - pontos_quadrado.min(axis=0)
     mask = np.zeros(croped.shape[:2], np.uint8)
     # desenhando os contornos usando a mascara
     cv2.drawContours(mask, [pontos_quadrado], -1, (255, 255, 255), -1, cv2.LINE_AA)

     # fazendo comparacao da imagem cortada com a mascara
     croped_image_final = cv2.bitwise_and(croped, croped, mask=mask)
     return croped_image_final
     # cv2.imshow("final",croped_image_final)
     # cv2.waitKey(0)
     
def get_squares_after_play(pontos_quadrado, img):

     # https://stackoverflow.com/questions/48301186/cropping-concave-polygon-from-image-using-opencv-python

     # criando um retangulo com os vertices
     rect_corte = cv2.boundingRect(pontos_quadrado)
     # passando as coordenadas para as variaveis
     x,y,w,h = rect_corte
     # cortando a imagem com as variaveis
     croped = img[y:y+h, x:x+w].copy()

     # fazendo mascara para o corte da imagem
     pontos_quadrado = pontos_quadrado - pontos_quadrado.min(axis=0)
     mask = np.zeros(croped.shape[:2], np.uint8)
     # desenhando os contornos usando a mascara
     cv2.drawContours(mask, [pontos_quadrado], -1, (255, 255, 255), -1, cv2.LINE_AA)

     # fazendo comparacao da imagem cortada com a mascara
     croped_image_final = cv2.bitwise_and(croped, croped, mask=mask)
     return croped_image_final
     # cv2.imshow("final",croped_image_final)
     # cv2.waitKey(0)
        
# recebe a imagem sem filtrar (imagem original dos quadrados com os simbolos)
def get_circles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    gray_blurred = cv2.blur(gray, (3, 3)) 
    
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
            cv2.imshow("Detected Circle", img) 
            
            cv2.waitKey(0) 
    
    # fazer retornar uma flag, caso ele tenha detectado um circulo no quadrado da matriz, pra fazer a jogada e remover quadrado da leitura


# testar fazer a subtracao do quadro VAZIO com o tabuleiro vazio, para tentar tirar os filtros e dai prosseguir!


# imagem do tabuleiro
img = cv2.imread("Webcam/O/TabuleiroO1.jpg")
img_processada = process(img)
cv2.imwrite("primeira_t_processada.jpg", img_processada)

# imagem do tabuleiro, com os simbolos temos que fazer os proximos passos em um loop (ateh a a parte da subtracao do tabuleiro com os simbolos ?)
img_x = cv2.imread("Webcam\O\O1-1.jpg")
img_processada_x = process(img_x)
cv2.imwrite("primeira_x_processada.jpg", img_processada_x)

# subtracao do tabuleiro com os simbolos 
img_sub = cv2.subtract(img_processada_x, img_processada)
cv2.imwrite("primeira_subtraida.jpg", img_sub)

# processando os ruidos do da subtracao feita
img_sub_processada = process_symbols(img_sub)
cv2.imwrite("primeira_subtraida_processada.jpg", img_sub_processada)

# contornando o tabuleiro
contours, _ = cv2.findContours(img_processada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #talvez usar o CHAIN_APPROX_SIMPLE, ver a diferenca em https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html

# pegando os contornos internos (quadrado do meio) e externos
inner, outer = sorted(map(convex_hull, contours), key=len)

# usando os contornos para calcular as coordenadas dos quadrados da matriz
lista_quadrados = get_square_corners(inner,outer)


for i in range(0,9):
     k=i+1
     if(k%3==0):
          j=3
     else:
          j=k%3
     k=int(i/3)+1
     lista_imagens_cortadas = get_squares_init(np.array(lista_quadrados[i]))
     cv2.imwrite(f"imagem_cortada_{k}{j}.png",lista_imagens_cortadas)
     imagem_cortada_com_x_tratada = get_squares_after_play(np.array(lista_quadrados[i]), img_sub_processada)
     cv2.imwrite(f"imagem_cortada_com_x_final{k}{j}.png",imagem_cortada_com_x_tratada)

# for i in range (0,9):
#      k=i+1
#      if(k%3==0):
#           j=3
#      else:
#           j=k%3
#      k=int(i/3)+1
#      lista_imagens_cortadas = corta_corta(np.array(lista_quadrados[i]))
#      quadrados_com_x = corta_corta_pronto(np.array(lista_quadrados[i]))
#      subtracted = cv2.subtract(quadrados_com_x, lista_imagens_cortadas)
#      cv2.imwrite(f"imagem_subtraida{k}{j}.png",subtracted)

# for x, y in quadraders(inner, outer):
# #     print(f"X: {x}; X: {y}")
#     cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
# cv2.imshow("result", img)
# cv2.waitKey(0)