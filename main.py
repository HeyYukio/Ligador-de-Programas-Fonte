# TODO: Interface para pedir nomes dos módulos 
# TODO: Lógica para obter módulos

from random import randint

resultado = open ("resultado.txt", "w")
class Entry: 
    """
    Classe para definição dos entry points.
    """
    def __init__(self, label, addr, modulo, numeroModulo):
        self.label = label
        self.addr = addr
        self.modulo = modulo
        self.numeroModulo = numeroModulo
        self.qntd = 1

    def PrintEntry(self):
        print ("Label: " + self.label + "; Endereco: " + self.addr )

class External: 
    """
    Classe para definição dos externals.
    """
    def __init__(self, label, modulo):
        self.label = label
        self.modulo = modulo

    def PrintExternal(self):
        print ("Label: " + self.label + "; Modulo: " + self.modulo )

class Modulo:
    """
    Classe para definição dos modulos.
    """ 
    def __init__(self, label):
        self.label = label

    def enderecoInicio(self, endInic):
        self.endInic = endInic
    
    def enderecoFim(self, endFim):
        self.endFim = endFim
    
    def numeroModulo(self, numero):
        self.numero = numero
        
class VarLocal:
    """
    Classe para definição das variáveis locais.
    """ 
    def __init__(self, label, addr, modulo, numeroModulo):
        self.label = label
        self.addr = addr
        self.modulo = modulo
        self.numeroModulo = numeroModulo
        self.qntd = 1

    def PrintVar(self):
        print ("Label: " + self.label + "; Endereco: " + self.addr )

def classificarInst(modulo, linhas, enderecoAtual, primeiroModulo, modulos):
    """
    Motor de eventos do programa. Tem a finalidade de classificar as instruções e pseudos, sendo as mais
    importantes as ENT, EXT e K, que são o ponto principal do programa. Caso haja declarações de ENTs, elas
    são adicionadas numa tabela de entry points, caso sejam EXTs, adiciona-se numa tabela de externals, e caso
    sejam variáveis locais, adiciona-se numa tabela de variáveis locais.
    
    Entradas:
    modulo: Módulo atual que está sendo lido, com referência.
    linhas: Linhas decompostas em uma lista do arquivo/módulo atual.
    enderecoAtual: Endereço atual dentro do arquivo fonte que irá unificar todos. Varia conforme são lidas as instruções 
        Esse parâmetro é útil para relocar os operandos de endereço nos próximos módulos.
    primeiroModulo: Variável que indica se o módulo é o primeiro, apenas para utilizar 
        a instrução "@" (ORG) como parâmetro de endereço inicial (considerado também relocável).
    modulos: Lista com todos os modulos lidos até o momento, possui as instruções de cada um.

    Retornos:
    enderecoAtual: Endereço atual depois de ler todas as instruções. Será o endereço base para o próximo módulo.
    primeiroModulo: Indicação de que o primeiro módulo já passou.
    modulos: Lista atualizada com os módulos, incluindo o lido.
    """

    modulos.append([])                              # Adiciona um novo elemento na lista de módulos
    entriesModulo = []                              # Cria a lista de entries para aquele módulo
    enderecoBase = enderecoAtual                    # Define a base para deslocamento dos operandos de endereço
    
    for i in linhas:
        instrucao = i.split()                       # "instrucao" será a linha decomposta em elementos, ou seja, um JP /023 vira ["JP", "/023"]

        if (len(instrucao) == 1):                   # Caso tenha tamanho de 1 é uma label de endereços
            modulos[len(modulos)-1].append(i)

        if (len(instrucao) == 2):                   # Caso tenho tamanho de 2 é uma instrução com um operando
            if (instrucao[0] == "@"):               # Se for uma instrução de "@", indica início do módulo.
                modulo.enderecoInicio(instrucao[1])
                modulo.numeroModulo(len(modulos)-1)
                if (primeiroModulo):                # Para o primeiro módulo, será denominada o endereço inicial.
                    enderecoAtual = int(instrucao[1], 16)
                    salvaResultado(instrucao, enderecoBase, 2, modulos)
                    
                    
            elif (instrucao[0] == "ENT"):           # Instrução de entry. Adiciona o nome numa lista que guarda as entries desse módulo. 
                                                    # Quando chegar na definição de valor destas, isso será conferido e elas serão adicionadas
                # nomesEntry.append(instrucao[1])   # a uma lista de entry points global.
                entriesModulo.append(instrucao[1])

            elif (instrucao[0] == "EXT"):
                TabelaExternal.append(External(instrucao[1], modulo.label))  # Adiciona a uma lista de Externals
                
                
            elif (instrucao[0] == "JP"):           # Instrução de JP, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
            
            elif (instrucao[0] == "JZ"):           # Instrução de JZ, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
            
            elif (instrucao[0] == "JN"):           # Instrução de JN, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
            
            elif (instrucao[0] == "CN"):            # Instrução de CN, soma 1 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 1
                salvaResultado(instrucao, enderecoBase, 1, modulos)
            
            elif (instrucao[0] == "+"):            # Instrução de +, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2 
                salvaResultado(instrucao, enderecoBase, 2, modulos)
                
            elif (instrucao[0] == "-"):            # Instrução de -, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
            
            elif (instrucao[0] == "*"):            # Instrução de *, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
                
            elif (instrucao[0] == "/"):            # Instrução de /, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
            
            elif (instrucao[0] == "LD"):            # Instrução de LD, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)

            elif (instrucao[0] == "MM"):            # Instrução de MM, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)
            
            elif (instrucao[0] == "SC"):            # Instrução de SC, soma 2 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 2
                salvaResultado(instrucao, enderecoBase, 2, modulos)

            elif (instrucao[0] == "OS"):            # Instrução de OS, soma 1 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 1
                salvaResultado(instrucao, enderecoBase, 1, modulos)
                
            elif (instrucao[0] == "IO"):            # Instrução de IO, soma 1 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 1
                salvaResultado(instrucao, enderecoBase, 1, modulos)
                
            elif (instrucao[0] == "$"):            # Pseudoinstrução de $, soma a quantidade de bytes para reservar no endereço atual e guarda para posterior impressão.
                enderecoAtual += int(instrucao[1], 16)  # Soma a quantidade de enderecos determinados pelo array
                salvaResultado(instrucao, enderecoBase, 2, modulos)
                
            elif (instrucao[0] == "K"):            # Pseudoinstrução de K, soma 1 no endereço atual e guarda para posterior impressão.
                enderecoAtual += 1
                salvaResultado(instrucao, enderecoBase, 1, modulos)
                

        if (len(instrucao) == 3):                   # Caso tenha tamanho 3, é uma declaração de variável ou de espaço
            if(instrucao[0] in entriesModulo):      #instrucao[0] in nomesEntry and instrucao[0] in entriesModulo):
                TabelaEntry.append(Entry(instrucao[0],  hex(enderecoAtual).split('x')[-1], modulo.label, len(modulos)-1)) # Adiciona na tabela de entries
                                                        # A conversão de hex do Python é diferente da que iremos usar, portanto precisa-se converter. Isso é apenas notação, portanto
                                                        # tomou-se da liberdade de converter facilmente (a do Python é 0xaaa, enquanto a nossa é só AAA)
                
            if (instrucao[1] == 'K' or instrucao[1] == '$'):        # Tratando tanto entries quanto vars locais
                if (instrucao[0] not in entriesModulo):
                    TabelaVarsLocais.append(VarLocal(instrucao[0],  hex(enderecoAtual).split('x')[-1], modulo.label, len(modulos)-1)) # Se for var local, adiciona aqui
                modulos[len(modulos)-1].append(i)                   # Coloca a linha na lista para posteriormente imprimir
                if instrucao[1] == "$":
                    enderecoAtual += (int(instrucao[2],16) - 1)     # Caso seja uma pseudo de array, soma a quantidade de endereços no contador de endereços
                enderecoAtual += 1                                  # Soma 1 no endereço atual

    primeiroModulo = False                                          # Atualiza o primeiroModulo

    return enderecoAtual, primeiroModulo, modulos

def adicionaModulo(nomeModulo, enderecoAtual, primeiroModulo, modulos):
    """
    Função que adiciona um módulo do arquivo .txt ao arquivo final, lendo linha por linha e separando tudo.

    Entradas:
    nomeModulo: Nome do módulo atual.
    enderecoAtual: Endereco inicial do arquivo final, que servirá de base para deslocar os operandos deste módulo.
    modulos: Lista com todos os módulos lidos até o momento, cada elemento possui todas as instruções de um módulo.

    Retornos:
    modulo: Módulo atual lido.
    retorno: Os retornos obtidos de classificarInst. 
    """
    modulo = Modulo(nomeModulo)
    f = open (nomeModulo, "r")
    lines = f.readlines()
    retorno = classificarInst(modulo, lines, enderecoAtual, primeiroModulo, modulos)
        
    return modulo, retorno

def salvaResultado (instrucao, enderecoBase, qtdBytes, modulos):
    """
    Salva as instruções numa lista, separando por módulo.

    Entradas:
    instrucao: Instrução atual a ser armazenada na lista
    enderecoBase: Endereço a ser somado nos operandos que são endereços também, relocando estes.
    qtdBytes: Tamanho da instrução, se é de 1 ou 2 bytes.
    modulos: Lista com os módulos até agora, que será atualizada adicionando a instrução passada.
    """
    if (qtdBytes == 2):                     # Caso seja uma operação de 2 bytes, então deve deslocar o operando (caso seja endereço de memória)
        if (instrucao[1].startswith('/')):  # Iniciando com '/'
            instrucao[1] = instrucao[1].split('/')[1]     # Tira a barra para poder somar o valor
            instrucao[1] = (hex(int(instrucao[1], 16) + int(enderecoBase)).split('x')[-1]).upper()    # Soma o deslocamento e converte para a nossa notação.
            modulos[len(modulos)-1].append('\t' + instrucao[0] + ' /' + instrucao[1].zfill(3) + '\n')   # Coloca na lista para posterior impressão
        else:
            modulos[len(modulos)-1].append('\t' + instrucao[0] + ' ' + instrucao[1] + '\n')    # Caso seja um operando não numérico (i.e. label), então ele só coloca na lista
    else:
        modulos[len(modulos)-1].append('\t' + instrucao[0] + ' ' + instrucao[1] + '\n') # Para operações de 1 byte, ele apenas coloca na lista.

def alterarNomeVar(modulo, nomeAtual, qntd, numeroModulo):
    """
    Função para alterar o nome da variável quando houver conflito. Será usada em dois tipos de conflito:
    variável local com ENT, e variável local com variável local.

    Entradas:
    modulo: Módulo atual que está sendo manipulado.
    nomeAtual: Nome atual da variável que está sendo manipulada.
    qntd: Quantas variáveis com este nome já houve.
    numeroModulo: Número do módulo o qual está sendo manipulado.
    """
    nomeNovo = nomeAtual + str(qntd)    # Muda o nome de acordo com a variável, por exemplo AAA pode virar AAA1, AAA2, etc, dependendo se já houve outras vars iguais.
    for linha in modulo:                # Vai varrer todas as linhas desse módulo procurando pela referência, e alterará pelo nome novo.
        instrucao = linha.split()
        if (len(instrucao) == 2):           # Para instruções do tipo "operação operando", ele vai alterar o operando caso seja igual a var que deve ser mudada
            if (instrucao[1] == nomeAtual):         
                instrucao[1] = nomeNovo
                modulo[modulo.index(linha)] = ('\t' + instrucao[0] + ' ' + instrucao[1] + '\n')    # Atualiza a lista
        if (len(instrucao) == 3):
            if (instrucao[0] == nomeAtual):     # Para a declaração da var, ele altera o nome.
                instrucao[0] = nomeNovo
                modulo[modulo.index(linha)] = (instrucao[0] + ' ' + instrucao[1] + ' ' + instrucao[2] + '\n')    # Atualiza a lista.
    
    for i in TabelaVarsLocais:
        if (i.label == nomeAtual and i.numeroModulo == numeroModulo):
            i.label = nomeNovo
    
escolha = 1
modulos = []
nomesEntry = []
TabelaEntry = []
TabelaExternal = []
TabelaModulos = []
TabelaVarsLocais = []
enderecoAtual = 0
primeiroModulo = True

while escolha != "2":                       # Interface de usuário
    print("Digite a opção desejada:")
    print ("1 - Inserir modulo")
    print ("2 - Finalizar a insercao de modulo")
    escolha = input()
    if escolha == "1":
        nomeModulo = input("Digite o nome do módulo com a extensão: ")
        retorno = adicionaModulo(nomeModulo, enderecoAtual, primeiroModulo, modulos)      # Pega todos os retornos do "adicionaModulo" e monta uma lista
        TabelaModulos.append(retorno[0])                                                  # Coloca na tabela de modulos o módulo adicionado
        modulos = retorno[1][2]                                                           # Atualiza a lista de módulos para ter todas as instrucoes até agora
        enderecoAtual = retorno[1][0]                                                     # Atualiza o endereço atual para ser a base do próximo
        primeiroModulo = retorno[1][1]                                                    # Atualiza a variável de "primeiroModulo"
        # i += 1
    elif escolha != "2": 
        print('Opção inválida!')

for i in TabelaEntry:                               # Varre a tabela de Entries procurando variáveis locais que tem o mesmo nome
    for j in modulos:                               
        if (i.numeroModulo != modulos.index(j)):    # Varre cada módulo diferente do módulo da declaração inicial
            for k in j:
                if (k.split()[0] == i.label):       # Varre cada instrução deste módulo. Caso haja uma declaração (o primeiro elemento da linha é igual a label do entry)
                    qntd = i.qntd                   # então ativa uma rotina para poder lidar com essa duplicidade, alterando o nome da variável local.
                    i.qntd = i.qntd + 1
                    alterarNomeVar(j, i.label, qntd, modulos.index(j))

for i in TabelaVarsLocais:                         # Mesma lógica para a parte de conflito com entries, porém aqui faz procurando variáveis locais apenas
    for j in modulos:
        if (i.numeroModulo != modulos.index(j)):
            for k in j:
                if (k.split()[0] == i.label):
                    qntd = i.qntd 
                    i.qntd = i.qntd + 1
                    alterarNomeVar(j, i.label, qntd, modulos.index(j))

for i in modulos:           # Imprime todas as linhas de todos os módulos, já com alteração, para o arquivo de resultados.
    for j in i:
        resultado.write(j)
resultado.write('\t# ' + modulos[0][0].split()[1])          # Coloca a pseudo de "#"/FIM com o endereço inicial.