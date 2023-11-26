import cv2
import numpy as np
from operator import itemgetter
import os
import time
import statistics

from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import numpy as np

tamanho_medio_quadrados = 13383.775

def tira_foto_quadro_vazio(cap):
    img = capture_picture(cap)
    cv2.imwrite("imagem_quadro_vazio.jpg", img)
    # img_processada = process(img,np.ones((12,12)))
    return img

def tira_foto_tabuleiro_vazio(cap):
    img = capture_picture(cap)
    cv2.imwrite("imagem_tabuleiro_vazio.jpg", img)
    # img_processada = process(img,np.ones((12,12)))
    return img

def processa_tabuleiro_vazio(cap,tabuleiro_vazio, quadro_vazio):
    # quadro = cv2.imread("imagem_quadro_vazio.jpg")
    # tabuleiro = cv2.imread("imagem_tabuleiro_vazio.jpg")
    sub = cv2.subtract(tabuleiro_vazio, quadro_vazio)
    img_processada = process(sub,np.ones((12,12)))
    cv2.imwrite("imagem_subtracao_processada.jpg", img_processada)
    return img_processada

def calcula_area(vertices):
    vertices = np.array(vertices, dtype=np.int32)
    vertices = vertices.reshape((-1, 1, 2))
    area = cv2.contourArea(vertices)
    return area

def encontra_quadrados(imagem):
    contours, _ = cv2.findContours(imagem, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #talvez usar o CHAIN_APPROX_SIMPLE, ver a diferenca em https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
    aux = sorted(map(convex_hull, contours), key=len)
    lista_quadrados = get_square_corners_v2(aux)
    if len(lista_quadrados) != 9:
        raise("Lista de Quadrados Vazia!!!")
    
    return lista_quadrados

def testa_qualidade_tabuleiro(lista_quadrados):
    list_area_size = []
    try:
        for square in lista_quadrados:
            list_area_size.append(calcula_area(square))
        list_area_size = np.array(list_area_size)

        media = np.mean(list_area_size)

        if media >= tamanho_medio_quadrados*0.8 and media <= tamanho_medio_quadrados*1.2:
            return True
        return False 
        
        return False
    except:
        return False
    

def testa_posicionamento_tabuleiro(img_processada,lista_quadrados):
    try:
        for quadrado in lista_quadrados:
            imagem = get_squares_after_play(np.array(quadrado), img_processada)                
            three_d_array = imagem[:, :, np.newaxis]
    except:
        return False
    return True


def detecta_jogada(img_processada,lista_quadrados,quadrados_preenchidos,simbolo, cap):
    print("Detectando...\n")
    contador_estabilidade = [0 for _ in range(9)]
    simbolos_detectado = [None for _ in range(9)]
    lista_imagens = [None for _ in range(9)]
    foto = 0
    while True:
        img_x = capture_picture(cap)
        img_processada_x = process(img_x)

        img_sub = cv2.subtract(img_processada_x, img_processada)

        # processando os ruidos do da subtracao feita
        img_sub_processada = process_symbols(img_sub)
        #cv2.imwrite(f"imagens_imp/erro/foto{foto}.png",img_sub_processada)
        simbolo_detectado = False
        for index,quadrado_preenchindo in enumerate(quadrados_preenchidos):
            if not quadrado_preenchindo:
                imagem = get_squares_after_play(np.array(lista_quadrados[index]), img_sub_processada)
                
                three_d_array = imagem[:, :, np.newaxis]
                imagem_3d = np.repeat(three_d_array, 3, axis=2)
                detectou_jogada = detector_jogada(imagem_3d)
                if detectou_jogada and not simbolo_detectado:
                    if simbolos_detectado[index] is None:
                        contador_estabilidade[index] += 1
                        lista_imagens[index] = imagem_3d
                        simbolos_detectado[index] = classificador_jogada(imagem_3d)
                        simbolo_detectado = True
                    else:
                        y_hat = classificador_jogada(imagem_3d)
                        if simbolos_detectado[index] == y_hat:
                            contador_estabilidade[index] += 1
                            lista_imagens[index] = imagem_3d
                            simbolos_detectado[index] = y_hat
                            simbolo_detectado = True
                        else:
                            contador_estabilidade[index] = 0
                            lista_imagens[index] = None
                            simbolos_detectado[index] = None
                elif detectou_jogada and simbolo_detectado:
                    contador_estabilidade = [0 for _ in range(9)]
                    break
                else:
                    contador_estabilidade[index] = 0
                    lista_imagens[index] = None
                    simbolos_detectado[index] = None

        for index,valor in enumerate(contador_estabilidade):
            if valor>1:
                y_hat = simbolos_detectado[index]
                if y_hat != simbolo:
                    cv2.imwrite(f"imagens_com_erro/simbolo_erro.png",lista_imagens[index])
                    return None
                return index
        #time.sleep(0.3)

detector_de_jogada = load_model(os.path.join('models','image_detector.h5'))
classificador_de_jogada = load_model(os.path.join('models','image_classifier.h5'))

def detector_jogada(imagem):
    resize = tf.image.resize(imagem, (256,256))
    aux = np.expand_dims(resize/255, 0)
    y_hat = detector_de_jogada.predict(aux,verbose = 0)
    if y_hat < 0.05:
        return True
    return False

def classificador_jogada(imagem):
    resize = tf.image.resize(imagem, (256,256))
    aux = np.expand_dims(resize/255, 0)
    y_hat = classificador_de_jogada.predict(aux,verbose = 0)
    if y_hat > 0.50:
        return 'x'
    else:
        return 'o'

# def capture_picture():
#     # Open a connection to the webcam (0 is usually the default webcam)
#     while True:
#         cap = cv2.VideoCapture(0)
    
#         if not cap.isOpened():
#             print("Error: Could not open webcam.")
#             while not cap.isOpened():
#                 cap = cv2.VideoCapture(1)
            
#         # Capture a single frame
#         ret, frame = cap.read()
    
#         if ret:
#             break
#         else:
#             print("Error: Could not read frame.")
#             time.sleep(10)
#     alpha = 3  # Increase this value to make the image brighter
#     beta = 0     # You can adjust this value if needed
#     brightened_frame = cv2.addWeighted(frame, alpha, np.zeros(frame.shape, frame.dtype), 0, beta)

#     # Release the webcam
#     cap.release()
#     return brightened_frame

#captuer_picture com a camera sempre ligada
def capture_picture(cap):
    # Open a connection to the webcam (0 is usually the default webcam)        
    # Capture a single frame
    i = 0
    while i != 10:
        _, frame = cap.read()
        i+=1
    return frame


# processando a imagem!
def process(img,dilat_kernel = np.ones((9, 9))):
     # convercao de RGB para BGR e grayscale
     try:
         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     except:
        raise("Erro")
     # aplicando o filtro gaussiano 
     img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
     # detectando as bordas
     img_canny = cv2.Canny(img_blur, 100, 200)
     # retorna um array com o tamanho (9,9 (?)) preenchido com 1
     kernel = np.ones((9, 9))
     # dilatando a imagem
     img_dilate = cv2.dilate(img_canny, dilat_kernel, iterations=1)
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
def get_square_corners_v2(contours):
    flag = 0 
    for contour in contours:
         if len(contour)<4:
              continue
         inner = contour
         ordenando_indice_x = inner[...,0].argsort()
         ordenando_x_menor = sorted(inner[ordenando_indice_x], key=itemgetter(0))
         lista_x_menor = np.array(ordenando_x_menor[0:2])
         lista_x_maior = np.array(ordenando_x_menor[2:])
         ordenando_indice_y_menor = lista_x_menor[...,1].argsort()
         aux = sorted(lista_x_menor[ordenando_indice_y_menor], key=itemgetter(1))
         
         top_lef_inner, bot_lef_inner = aux[0],aux[-1]
         ordenando_indice_y_maior = lista_x_maior[...,1].argsort()
         aux = sorted(lista_x_maior[ordenando_indice_y_maior], key=itemgetter(1))
         top_rit_inner, bot_rit_inner = aux[0],aux[-1]
         dist = np.linalg.norm(top_rit_inner - top_lef_inner)
         if dist > 50:
              flag = True
              break
    
    if not flag:
         return None
              
    p2 = 2*top_lef_inner - bot_lef_inner
    p5 = 2*top_lef_inner - top_rit_inner
    p3 = 2*top_rit_inner - bot_rit_inner
    p6 = 2*top_rit_inner - top_lef_inner
    p7 = 2*bot_lef_inner - bot_rit_inner
    p10 = 2*bot_lef_inner - top_lef_inner
    p8 = 2*bot_rit_inner - bot_lef_inner
    p11 = 2*bot_rit_inner - top_rit_inner
    p1 = 2*top_lef_inner - bot_rit_inner
    p4 = 2*top_rit_inner - bot_lef_inner
    p9 = 2*bot_lef_inner - top_rit_inner
    p12 = 2*bot_rit_inner - top_lef_inner
    return [[p7,bot_lef_inner,p10,p9],[p5,top_lef_inner,bot_lef_inner,p7],[p1,p2,top_lef_inner,p5],[bot_lef_inner,bot_rit_inner,p11,p10],[top_lef_inner,top_rit_inner,bot_rit_inner,bot_lef_inner],[p2,p3,top_rit_inner,top_lef_inner],[bot_rit_inner,p8,p12,p11],[top_rit_inner,p6,p8,bot_rit_inner],[p3,p4,p6,top_rit_inner]]  
     
def get_square_corners(inner, outer): 

     ordenando_indice_x = inner[...,0].argsort()
     ordenando_x_menor = sorted(inner[ordenando_indice_x], key=itemgetter(0))

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
