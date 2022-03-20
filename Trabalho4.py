import numpy as np
#Classe que representa estados
#Cada estado é uma matriz possível que representa a sala, isto é, é uma matriz nxn onde 1 pessoa ocupa 1 coordenada e 1 alavanca ocupa outra
class Estado:
    def __init__(self, posicaoPessoa, posicaoAlavanca, estadoAnterior, dimensao):
        self.posicaoPessoa = posicaoPessoa #posicao [x,y] da pessoa na matriz
        self.posicaoAlavanca=posicaoAlavanca #posicao [x,y] da alavanca na matriz
        self.estadoAnterior = estadoAnterior #O estado a partir do qual
        self.dimensao = dimensao #Dimensao da sala
        self.distanciaEstadoFinal = abs(posicaoPessoa[0]-posicaoAlavanca[0])+abs(posicaoPessoa[1]-posicaoAlavanca[1])

        #Construção da sala em formato de matriz
        sala = np.zeros((self.dimensao, self.dimensao), dtype=int)
        sala[alavancaPosicao[0]][alavancaPosicao[1]] = 1  #Na matriz, a alavanca é representada pelo numero 1
        sala[posicaoPessoa[0]][posicaoPessoa[1]] = 7  #Na matriz, a pessoa é representada pelo numero 7
        self.matrizSala=sala


    def __repr__(self): #O estado é representado graficamente pela matriz
       # return str(self.matrizSala)
        return str(self.posicaoPessoa)


#Criação do Estado Inicial
alavancaPosicao = [2,2] #Coordenadas da alavanca na matriz
pessoaPosicao = [8,8] #Coordenadas da pessoa na matriz
EstadoInicial = Estado(pessoaPosicao,alavancaPosicao, None, 10)


#Recebe um Estado e retorna uma lista com os movimentos possíveis a partir do estado parâmetro
def movimentosPossiveis(estado):
    movimentosPossiveis = ["N", "S", "L", "O"]
    if estado.posicaoPessoa[0]==0: #Pessoa está no topo da sala
        movimentosPossiveis.remove("N")
    if estado.posicaoPessoa[0] == 3: #Pessoa está na base da sala
        movimentosPossiveis.remove("S")
    if estado.posicaoPessoa[1] == 0: #Pessoa está na face oeste da sala
        movimentosPossiveis.remove("O")
    if estado.posicaoPessoa[1] == 3: #Pessoa está na face leste da sala
        movimentosPossiveis.remove("L")
    return movimentosPossiveis

#Recebe um estado e define os estados possíveis a partir do estado parâmetro
def definirProxEstados(estado):
    mov = movimentosPossiveis(estado) #Estabelece os movimentos possíveis a partir do estado parâmetro
    proxEstados = [] #Vetor para armazenar os estados possíveis
    for movimento in mov: #A partir dos movimentos possíveis, determina todos os estados possíveis
        novaPosicao = estado.posicaoPessoa.copy()
        if movimento == "N":
            novaPosicao[0] -= 1
        elif movimento == "S":
            novaPosicao[0] += 1
        elif movimento == "L":
            novaPosicao[1] += 1
        elif movimento == "O":
            novaPosicao[1] -= 1
        proxEstados.append(Estado(novaPosicao, estado.posicaoAlavanca, estado, estado.dimensao))
    return proxEstados

#Recebe o estado final encontrado após uma busca e determina o caminho feito até o estado inicial
def montarCaminho(estadoFinal):
    etapa = estadoFinal
    caminho = [estadoFinal]
    while (etapa.estadoAnterior != None): #O caminho de partida SEMPRE tem o atributo .estadoAnterior como None
        etapa = etapa.estadoAnterior
        caminho.append(etapa)
    return caminho[::-1] #Reverte a ordem e retorna o caminho

#algoritmo de Busca Gulosa
def buscaGulosa(estado, caminho=[]):
    #Condição de Parada: Posição da pessoa é igual à da Alavanca
    if estado.posicaoAlavanca == estado.posicaoPessoa:
        return caminho
    else:
        proxEstados = definirProxEstados(estado) #Define os possíveis estados seguintes
        proxEstado = min(proxEstados, key=lambda x: x.distanciaEstadoFinal) #Seleciona o estado seguinte mais próximo da alavanca
        caminho.append(estado) #Adiciona o estado atual ao caminho
        return buscaGulosa(proxEstado,caminho) #Elo recursivo para processar o próximo estado

def buscaAEstreoa(estado, caminho=[], custoAcumulado=0):
    #Condição de Parada: Posição da pessoa é igual à da Alavanca
    if estado.posicaoAlavanca == estado.posicaoPessoa:
        return caminho
    else:
        proxEstados = definirProxEstados(estado) #Define os possíveis estados seguintes
        # Seleciona o estado seguinte mais próximo da alavanca (considerando o custo acumulado)
        proxEstado = min(proxEstados, key=lambda x: x.distanciaEstadoFinal+custoAcumulado)
        caminho.append(estado) #Adiciona o estado atual ao caminho
        return buscaAEstreoa(proxEstado,caminho, custoAcumulado+1) #Elo recursivo para processar o próximo estado

print(buscaGulosa(EstadoInicial))
print(buscaAEstreoa(EstadoInicial))