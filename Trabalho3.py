import numpy as np

#Classe que representa estados
#Cada estado é uma matriz possível que representa a sala, isto é, é uma matriz nxn onde 1 pessoa ocupa 1 coordenada e 1 alavanca ocupa outra
class Estado:
    def __init__(self, posicaoPessoa, posicaoAlavanca, estadoAnterior, dimensao):
        self.posicaoPessoa = posicaoPessoa #posicao [x,y] da pessoa na matriz
        self.posicaoAlavanca=posicaoAlavanca #posicao [x,y] da alavanca na matriz
        self.estadoAnterior = estadoAnterior #O estado a partir do qual
        self.dimensao = dimensao #Dimensao da sala

        #Construção da sala em formato de matriz
        sala = np.zeros((self.dimensao, self.dimensao), dtype=int)
        sala[alavancaPosicao[0]][alavancaPosicao[1]] = 1  #Na matriz, a alavanca é representada pelo numero 1
        sala[posicaoPessoa[0]][posicaoPessoa[1]] = 7  #Na matriz, a pessoa é representada pelo numero 7
        self.matrizSala=sala


    def __repr__(self): #O estado é representado graficamente pela matriz
        #return str(self.matrizSala)
        return str(self.posicaoPessoa)


#Criação do Estado Inicial
alavancaPosicao = [0,0] #Coordenadas da alavanca na matriz
pessoaPosicao = [3,3] #Coordenadas da pessoa na matriz
EstadoInicial = Estado(pessoaPosicao,alavancaPosicao, None, 4)


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

#Busca em largura dos estados
def buscaEmLargura(estadoInicial):
    posicaoAlavanca = estadoInicial.posicaoAlavanca
    #Caso 1 - A pessoa já está na mesma coordenada que a alavanca
    if posicaoAlavanca==estadoInicial.posicaoPessoa:
        return estadoInicial
    #Caso 2 - Busca em Largura
    else:
        estadosVisitados = [estadoInicial] #Estados que serão visitados no BFS
        estadosProxNivel = definirProxEstados(estadoInicial) #Estados no nível que será analisado no Laço a seguir
        while estadosProxNivel!=[]: #Enquanto há estados no prox nível, a busca ocorre
            estadosProxProxNivel = [] #Armazena os estados que serão computados na próxima iteração
            for estado in estadosProxNivel: #Itera pelos estados no próximo nível
                #Caso 1 - Encontrou o Estado Buscado
                if estado.posicaoPessoa==posicaoAlavanca: #Encontra o estado buscado
                    estadosVisitados.append(estado)
                    caminho = montarCaminho(estado) #Monta o caminho feito
                    return caminho
                #Caso 2 - Não encontrou o Estado Buscado
                else:
                    estadosVisitados.append(estado) #Adiciona o estado visitado à lista de estados visitados
                    for proxEstados in definirProxEstados(estado): #Armazena todos os estados seguintes ao estado analisado
                        estadosProxProxNivel.append(proxEstados)
                    estadosProxNivel = estadosProxProxNivel #Atualiza o próximo nível a ser atualizado
        return [] #Se chegar até aqui, não foi encontrado um caminho entre os dois estados buscados

def buscaEmProfundidade(estadoInicial):
    #Caso 1 - A pessoa já está na mesma coordenada que a alavanca
    if estadoInicial.posicaoPessoa==estadoInicial.posicaoAlavanca:
        return estadoInicial
    #Caso 2 - Busca em Profundidade
    else:
        pilha = [] #Pilha usada para avançar na busca
        pilha.append(estadoInicial)
        estadosVisitados = [] #Controle dos estados visitados
        while pilha!=[]:
            estadoAtual = pilha.pop() #Remove o último estado adicionado à pilha
            if estadoAtual.posicaoPessoa==estadoInicial.posicaoAlavanca:
                caminho = montarCaminho(estadoAtual) #Se encontrou o estado final, traça o caminho
                return caminho
            else:
                #Verifica se o estado atual já não foi visitado. Faz a verificação observando se a coordenada de Pessoa já foi visitada.
                if estadoAtual.posicaoPessoa not in [x.posicaoPessoa for x in estadosVisitados]:
                    estadosVisitados.append(estadoAtual)
                    for estado in definirProxEstados(estadoAtual): #Adiciona os estados seguintes à pilha
                        pilha.append(estado)
        return pilha

#Função auxiliar para determinar a profundidade de um determinado estado
def contarNivel(estadoAtual, nivel=0):
    #A função retorna do estadoAtual até o estado inicial, contando quantas etapas existem entre eles
    if estadoAtual.estadoAnterior==None:
        return nivel
    else:
        return contarNivel(estadoAtual.estadoAnterior, nivel+1)

def buscaEmProfundidadeLimitada(estadoInicial, limite):
    #Caso 1 - A pessoa já está na mesma coordenada que a alavanca
    if estadoInicial.posicaoPessoa==estadoInicial.posicaoAlavanca:
        return estadoInicial
    #Caso 2 - Busca em Profundidade com Limite
    else:
        pilha = [] #Estados que serão visitados no DLS
        pilha.append(estadoInicial)
        estadosVisitados = [] #Controla os estados visitados para evitar loops e repetições
        while True:
            while pilha!=[]:
                estadoAtual = pilha.pop()
                if estadoAtual.posicaoPessoa==estadoInicial.posicaoAlavanca:
                    b = montarCaminho(estadoAtual)
                    return b
                else:
                    nivelAtual = contarNivel(estadoAtual) #Determina o nível atual
                    if estadoAtual.posicaoPessoa not in [x.posicaoPessoa for x in estadosVisitados] and nivelAtual<=limite:
                        estadosVisitados.append(estadoAtual)
                        for estado in definirProxEstados(estadoAtual):
                            pilha.append(estado)
            return pilha

def buscaEmProfundidadeIterativa(estadoInicial):
    #Caso 1 - A pessoa já está na mesma coordenada que a alavanca
    if estadoInicial.posicaoPessoa==estadoInicial.posicaoAlavanca:
        return estadoInicial
    #Caso 2 - Busca em Profundidade com Limite
    else:
        nivel = 0 #Nivel da origem
        resultado = [] #Vetor que armazena o caminho encontrado
        while resultado==[]:
            nivel += 1 #Desce mais um nível possível
            resultado = buscaEmProfundidadeLimitada(estadoInicial, nivel) #Roda o DLS
        return (nivel, resultado)

#Teste
if __name__ == '__main__':

    a = buscaEmProfundidade(EstadoInicial)
    b = buscaEmLargura(EstadoInicial)
    c = buscaEmProfundidadeLimitada(EstadoInicial, 7)
    d = buscaEmProfundidadeIterativa(EstadoInicial)


    print(a)
    print(b)
    print(c)
    print(d)

