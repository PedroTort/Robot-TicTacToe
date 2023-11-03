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
def quadraders(inner, outer): 

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
def corta_corta(pontos_quadrado):

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
     
    
img = cv2.imread("webcam_dia_1.jpg")
cv2.imshow("imagem_normal", img)
img_processada = process(img)
cv2.imshow("imagem_processada", img_processada)
# cv2.waitKey(0)

contours, _ = cv2.findContours(img_processada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #talvez usar o CHAIN_APPROX_SIMPLE, ver a diferenca em https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html

# contornos_desenhados = cv2.drawContours(img, contours, -1, (0,255,0), 3)
# cv2.imshow("contornos desenhados", contornos_desenhados)
# cv2.waitKey(0)

# o inner sao os pontos do quadrado do meio
# o outter sao os pontos do octagno externo

inner, outer = sorted(map(convex_hull, contours), key=len)

lista_quadrados = quadraders(inner,outer)

for i in range(0,9):
     k=i+1
     if(k%3==0):
          j=3
     else:
          j=k%3
     k=int(i/3)+1
     lista_imagens_cortadas = corta_corta(np.array(lista_quadrados[i]))
     cv2.imwrite(f"imagem_cortada_{k}{j}.png",lista_imagens_cortadas)

# for x, y in quadraders(inner, outer):
# #     print(f"X: {x}; X: {y}")
#     cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
# cv2.imshow("result", img)
# cv2.waitKey(0)