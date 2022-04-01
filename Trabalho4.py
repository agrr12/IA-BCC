import numpy as np
#Classe que representa estados
#Cada estado é uma matriz possível que representa a sala, isto é, é uma matriz nxn onde 1 pessoa ocupa 1 coordenada e 1 alavanca ocupa outra
class Estado:
    def __init__(self, posicaoPessoa, posicaoAlavanca, estadoAnterior, dimensao, acao):
        self.posicaoPessoa = posicaoPessoa #posicao [x,y] da pessoa na matriz
        self.posicaoAlavanca=posicaoAlavanca #posicao [x,y] da alavanca na matriz
        self.estadoAnterior = estadoAnterior #O estado a partir do qual o estado atual foi gerado
        self.dimensao = dimensao #Dimensao da sala
        self.acao = acao #Ação que originou o estado atual
        self.distanciaEstadoFinal = abs(posicaoPessoa[0] - posicaoAlavanca[0]) + abs(
            posicaoPessoa[1] - posicaoAlavanca[1]) #Para Busca heurística

        #Construção da sala em formato de matriz
        sala = np.zeros((self.dimensao, self.dimensao), dtype=int)
        sala[alavancaPosicao[0]][alavancaPosicao[1]] = 1  #Na matriz, a alavanca é representada pelo numero 1
        sala[posicaoPessoa[0]][posicaoPessoa[1]] = 7  #Na matriz, a pessoa é representada pelo numero 7
        self.matrizSala=sala

    #Dois estados são iguais se as coordenadas da pessoa e da alavanca são idênticas nos dois casos
    def __eq__(self, other):
        if (isinstance(other, Estado)):
            return (self.posicaoPessoa == other.posicaoPessoa) and self.posicaoAlavanca == other.posicaoAlavanca

    # O estado é representado por ação de origem|coordenada da pessoa
    def __repr__(self):
        return (str(self.acao) +"|"+str(self.posicaoPessoa))

################## FUNÇÕES AUXILIARES #####################################################
###########################################################################################

#Função auxiliar para determinar a profundidade de um determinado estado
def contarNivel(estadoAtual, nivel=0):
    #A função retorna do estadoAtual até o estado inicial, contando quantas etapas existem entre eles
    if estadoAtual.estadoAnterior==None:
        return nivel
    else:
        return contarNivel(estadoAtual.estadoAnterior, nivel+1)

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
        acao = ""
        novaPosicao = estado.posicaoPessoa.copy()
        if movimento == "N":
            novaPosicao[0] -= 1
            acao="Norte"
        elif movimento == "S":
            novaPosicao[0] += 1
            acao = "Sul"
        elif movimento == "L":
            novaPosicao[1] += 1
            acao = "Leste"
        elif movimento == "O":
            novaPosicao[1] -= 1
            acao = "Oeste"
        proxEstados.append(Estado(novaPosicao, estado.posicaoAlavanca, estado, estado.dimensao, acao))
    return proxEstados

#Recebe o estado final encontrado após uma busca e determina o caminho feito até o estado inicial
def montarCaminho(estadoFinal):
    etapa = estadoFinal
    caminho = [estadoFinal]
    while (etapa.estadoAnterior != None): #O caminho de partida SEMPRE tem o atributo .estadoAnterior como None
        etapa = etapa.estadoAnterior
        caminho.append(etapa)
    return caminho[::-1] #Reverte a ordem e retorna o caminho
###########################################################################################

#algoritmo de Busca Gulosa utilizando Fila de Prioridade (Priority Queue)
def BG (estadoInicial):
    filaPrioridade = [estadoInicial]
    visitados = []
    while filaPrioridade != []:  # Laço até percorrer todos os estados possíveis
        estadoAtual = filaPrioridade.pop(0)
        visitados.append(estadoAtual)
        proxEstados = definirProxEstados(estadoAtual)  # Define os próximos estados a partir do estado atual
        # Seleciona a menor distância até a alavanca dentre os estados seguintes
        for proxEstado in proxEstados:  # Itera pelos próximos estados
            if proxEstado.posicaoAlavanca == proxEstado.posicaoPessoa:
                return montarCaminho(proxEstado)
            else:
                if proxEstado not in visitados:
                    filaPrioridade.append(proxEstado)
        #Organiza a fila de prioridade colocando os mais próximos do objetivo na primeira posição
        filaPrioridade = sorted(filaPrioridade, key=lambda x: x.distanciaEstadoFinal)[::-1]


#Busca A*
def buscaAEstrela(estadoInicial):
    filaPrioridade = [estadoInicial]
    visitados = []
    while filaPrioridade != []:  # Laço até percorrer todos os estados possíveis
        estadoAtual = filaPrioridade.pop(0)
        visitados.append(estadoAtual)
        custoAcumulado = len(montarCaminho(estadoAtual)) - 1  # Calcula o custo acumulado até o estado atual
        proxEstados = definirProxEstados(estadoAtual)  # Define os próximos estados a partir do estado atual
        # Seleciona a menor distância até a alavanca dentre os estados seguintes
        for proxEstado in proxEstados:  # Itera pelos próximos estados
            if proxEstado.posicaoAlavanca == proxEstado.posicaoPessoa:
                return montarCaminho(proxEstado)
            else:
                if proxEstado not in visitados:
                    filaPrioridade.append(proxEstado)
        #Organiza a fila de prioridade colocando os mais próximos do objetivo na primeira posição (considerando o custo acumulado)
        filaPrioridade = sorted(filaPrioridade, key=lambda x: x.distanciaEstadoFinal+custoAcumulado+1)[::-1]

def buscaAEstrelaAprofundamentoIterativo(estadoInicial,nivelMaximo):
    filaPrioridade = [estadoInicial]
    visitados = []
    while filaPrioridade != []:  # Laço até percorrer todos os estados possíveis
        estadoAtual = filaPrioridade.pop(0)
        visitados.append(estadoAtual)
        custoAcumulado = len(montarCaminho(estadoAtual)) - 1  # Calcula o custo acumulado até o estado atual
        #Verifica se o nivel máximo foi estourado
        #Se estoura, aumenta o nível máximo e reinicia o processo
        if custoAcumulado > nivelMaximo:
            nivelMaximo += 1
            filaPrioridade = [estadoInicial]
            continue
        proxEstados = definirProxEstados(estadoAtual)  # Define os próximos estados a partir do estado atual
        # Seleciona a menor distância até a alavanca dentre os estados seguintes
        for proxEstado in proxEstados:  # Itera pelos próximos estados
            if proxEstado.posicaoAlavanca == proxEstado.posicaoPessoa:
                return montarCaminho(proxEstado)
            else:
                if proxEstado not in visitados:
                    filaPrioridade.append(proxEstado)
        #Organiza a fila de prioridade colocando os mais próximos do objetivo na primeira posição (considerando o custo acumulado)
        filaPrioridade = sorted(filaPrioridade, key=lambda x: x.distanciaEstadoFinal+custoAcumulado+1)[::-1]




if __name__ == '__main__':
    # Criação do Estado Inicial
    alavancaPosicao = [0, 0]  # Coordenadas da alavanca na matriz
    pessoaPosicao = [3, 3]  # Coordenadas da pessoa na matriz
    EstadoInicial = Estado(pessoaPosicao, alavancaPosicao, None, 4, "Inicio")
    print(BG(EstadoInicial))
    print(buscaAEstrela(EstadoInicial))
    print(buscaAEstrelaAprofundamentoIterativo(EstadoInicial,10))