import cv2

import numpy as np

def Init():
    cap = cv2.VideoCapture('pedra-papel-tesoura.mp4') #Captura do Frame

    if not cap.isOpened():
        raise Exception("Não foi possível abrir o vídeo")  # Expection

    return cap

def BuildImageFilter(frame):
    filter_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Filtro de Cinza

    blur = cv2.blur(filter_hsv, (15, 15), 0)  # Blur

    array_filter1 = np.array([0, 20, 10])  # Filtro HSV
    array_filter11 = np.array([18, 200, 200])  # Filtro HSV

    array_filter2 = np.array([0, 1, 1])  # Filtro HSV
    array_filter21 = np.array([255, 150, 250])  # Filtro HSV

    mask_1 = cv2.inRange(blur, array_filter1, array_filter11)  # Máscara 1

    mask_2 = cv2.inRange(blur, array_filter2, array_filter21)  # Máscara 2

    return cv2.bitwise_or(mask_1, mask_2)  # Imagem filtrada

def BuildArea(imagem_filtro):
    contours, _ =cv2.findContours(imagem_filtro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #contornos

    imagem_filtro = cv2.cvtColor(imagem_filtro, cv2.COLOR_GRAY2RGB) #imagem para RGB

    cv2.drawContours(imagem_filtro, contours, -1, [191, 64, 191], 4) #pintando os contornos

    contorno = contours[1] #jogador 1

    contorno2 = contours[0] #jogador 2

    dicio_1 = cv2.moments(contorno) # dicionário dos contornos do jogador 1
    dicio_2 = cv2.moments(contorno2) # dicionário dos contornos do jogador 2

    area_c1 = int(dicio_1['m00']) #mão do jogador 1
    area_c2 = int(dicio_2['m00']) #mão do jogador 2

    return area_c1, area_c2, imagem_filtro

def GetMatchResults(area_c1, area_c2, pontos_p1, pontos_p2):
    
    result_h1 = ''
    result_h2 = ''
    resultado = ''

    if area_c1 < 58163:       #Definindo áreas de tesoura, papel e pedra
        result_h1 = "Tesoura"
    elif area_c1 > 58163 and area_c1 < 70045:
        result_h1 = "Pedra"
    elif area_c1 > 70045:
        result_h1 = "Papel"

    if area_c2 < 58163:
        result_h2 = "Tesoura"
    elif area_c2 > 58163 and area_c2 < 70045:
        result_h2 = "Pedra"
    elif area_c2 > 70045:
        result_h2 = "Papel"


    #guetto fix
    if result_h1 == "Pedra" and result_h2 == "Tesoura":
        result_h1 = "Tesoura"
        result_h2 = "Pedra"

    #PONTUAÇÕES

    if (result_h1 == "Tesoura" and result_h2 == "Papel"):
        pontos_p1 = pontos_p1+1
        resultado = "Vencedor: jogador 1!"

    elif (result_h1 == "Papel" and result_h2 == "Tesoura"):
        pontos_p2 = pontos_p2+1
        resultado = "Vencedor: jogador 2!"

    elif (result_h1 == "Pedra" and result_h2 == "Tesoura"):
        pontos_p1 =pontos_p1+1
        resultado = "Vencedor: jogador 1!"

    elif (result_h1 == "Tesoura" and result_h2 == "Pedra"):
        pontos_p2 =pontos_p2+1
        resultado = "Vencedor: jogador 2!"

    elif (result_h1 == "Papel" and result_h2 == "Pedra"):
        pontos_p1 =pontos_p1+1
        resultado = "Vencedor: jogador 1!"

    elif (result_h1 == "Pedra" and result_h2 == "Papel"):
       pontos_p2 = pontos_p2+1
       resultado = "Vencedor: jogador 2!"

    if result_h1 == result_h2:
        resultado = "Empate"

    return result_h1, result_h2, resultado, pontos_p1, pontos_p2

capture = Init()

pontos_p1 = 0
pontos_p2 = 0

while True:

    ret, frame = capture.read() #Frame do Vídeo

    # print(ret, frame)
    if not ret or frame is None:
        print("Video finalizado!")
        break

    imagem_filtro = BuildImageFilter(frame) #call pra construir os filtros do frame

    area_c1, area_c2, imagem_filtro = BuildArea(imagem_filtro)

    # print("areas ", area_c1, area_c2)

    result_h1, result_h2, resultado, pontos_p1, pontos_p2= GetMatchResults(area_c1, area_c2, pontos_p1, pontos_p2)
    
    #Texto Jogador 1
    (cv2.putText(imagem_filtro,("jogador 1 = " + str(result_h1)),(250, 250),cv2.FONT_HERSHEY_SIMPLEX,2, (191, 64, 191), 2, cv2.LINE_AA))

    #Texto Jogador 2

    (cv2.putText(imagem_filtro,("jogador 2 = " + str(result_h2)),(1050, 250),cv2.FONT_HERSHEY_SIMPLEX,2, (191, 64, 191), 2, cv2.LINE_AA))

    #Texto do Resultado

    (cv2.putText(imagem_filtro, (resultado), (530, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (191, 64, 191), 2, cv2.LINE_AA))
    # (cv2.putText(imagem_filtro, str(pontos_p1) + "     x     " + str(pontos_p2), (700, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (191, 64, 191), 2, cv2.LINE_AA))

    img_final = cv2.resize(imagem_filtro, (800, 600)) #Reduzindo tamanho do Video

    cv2.imshow("Game", img_final) #Mostrando Video

    if cv2.waitKey(1) & 0xFF == ord('f'): #Comandos para Sair
        break

capture.release()

cv2.destroyAllWindows()
