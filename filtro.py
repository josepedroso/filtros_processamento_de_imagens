import cv2
import numpy as np
import sys
import random

#verifica argumentos de entrada
def checagem(imagemEntrada, nivelRuido, filtro):
    niveisRuido = [0.01, 0.02, 0.05, 0.07, 0.1]
    if imagemEntrada is None:
        print(f"erro na imagem de entrada")
        exit(-1)
    if nivelRuido in niveisRuido == False:
        print(f"valor de ruido invalido")
        exit(-1)
    if filtro < 0 or filtro > 2:
        print(f"valor de filtro invalido")
        exit(-1)

#implementação do metodo de empilhamento
def empilhamento(imagem_ruido, imagemEntrada, ruido):
    imagem_resultado = imagem_ruido
    sum = imagem_ruido
    for i in range(4):#faz a media acumulativa 4 vezes 
        for l in range (13):
            sum = sum + sp_noise(imagemEntrada, ruido)#somatorio de 13 imagens
        sum = sum / 13#media das 13
        imagem_resultado = (imagem_resultado + sum) / 2# media com a imagem resultante acumulativa
    return imagem_resultado

#direciona para qual filtro aplicar e retorna a imagem com filtro
def filtros(imagemRuido, filtro, imagemOriginal, ruido):
    if filtro == 0:
        print("filtro usado: média")
        return cv2.blur(imagemRuido, (5, 3))
    if filtro == 1:
        print("filtro usado: mediana")
        return cv2.medianBlur(imagemRuido, 3)
    if filtro == 2:
        print("filtro usado: empilhamento")
        emp = empilhamento(imagemRuido, imagemOriginal, ruido)
        return emp

#aplica ruidos na imagem
def sp_noise(image, prob):
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

#função principal printa o psnr e escreve a imagem de saida
def testaFiltros(nomeImagemEntrada, nivelRuido, filtro, nomeImagemSaida):
    imagemEntrada = cv2.imread(nomeImagemEntrada)
    checagem(imagemEntrada, nivelRuido, filtro)
    imagem_ruido = sp_noise(imagemEntrada, nivelRuido)
    imagemFiltro = filtros(imagem_ruido, filtro, imagemEntrada, nivelRuido)
    if filtro == 2:
        imagemEntrada = imagemEntrada.astype(float)#devido ser uma media o empilhamento volta com valores em float 
    print(f"nivel de ruido: {nivelRuido}")
    print(f"PSNR: {cv2.PSNR(imagemEntrada, imagemFiltro)}")
    cv2.imwrite(nomeImagemSaida, np.hstack([imagem_ruido, imagemFiltro]))

if __name__ == "__main__":
    if len(sys.argv) == 5:
        for i, arg in enumerate(sys.argv):
            if i == 1:
                nomeImagemEntrada = arg
            if i == 2:
                nivelRuido = float(arg)
            if i == 3:
                filtro = int(arg)
            if i == 4:
                nomeImagemSaida = arg
        testaFiltros(nomeImagemEntrada, nivelRuido, filtro, nomeImagemSaida)
    else:
        print(f"numero de argumentos errado")