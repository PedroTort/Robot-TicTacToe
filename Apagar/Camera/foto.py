import cv2

image = cv2.imread('3.jpeg')

# corrigindo a iluminacao do fundo da imagem

# convert between RGB/BGR and grayscale
# convercao de RGB para BGR e grayscale
# --Parametros: imagem, gradiente escolhido
image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# converte os graos para a forma que foi passada, nesse caso eh um rectangulo (?) - pode ser rectangulo, cross ou ellipse
# passa a estrutura e o tamanho que quer o grao
# --Parametros: formato, tamanho, "posicao ancora"
se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))

# dilatando a imagem (aumentando a quantidade de pixel em branco que tem vizinhos com pixels brancos tbm)
# --Parametros: imagem, transformacao escolhida, quantidade de iteracoes
bg=cv2.morphologyEx(image, cv2.MORPH_DILATE, se)

# divisao por elemento de vetor com vetor ou de escalar por vetor
# --Parametros: um vetor, outro vetor do msm tamanho, o escalar, ...?
out_gray=cv2.divide(image, bg, scale=255)

# se o pixel for maior que o valor, vira 1, caso contrario vira 0
# a imagem como parametro deve ser uma imagem em escala de cinza
# --Parametros: imagem, valor do treshold, valor que o pixel vira caso seja maior que o treshold, tipo de treshold
out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 


# o binary ficou bom pro teste da imagem 3
cv2.imshow('binary', out_binary)  
cv2.imwrite('binary.png',out_binary)
# o gray nao ficou mt legal
cv2.imshow('gray', out_gray)  
cv2.imwrite('gray.png',out_gray)