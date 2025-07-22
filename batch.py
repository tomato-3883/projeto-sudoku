from sys import argv

def traducao(entrada):
    coord,valor = entrada.split(':')
    valor = int(valor)
    c,linha = coord.split(',')
    linha = int(linha)
    if linha < 1 or linha > 9:
        return False
    linha = linha - 1
    if valor < 1 or valor > 9:
        return False
    else:
        if c == 'a' or c == 'A':
            coluna = 0
        elif c == 'b' or c == 'B':
            coluna = 1
        elif c == 'c' or c == 'C':
            coluna = 2
        elif c == 'd' or c == 'D':
            coluna = 3
        elif c == 'e' or c == 'E':
            coluna = 4
        elif c == 'f' or c == 'F':
            coluna = 5
        elif c == 'g' or c == 'G':
            coluna = 6
        elif c == 'h' or c == 'H':
            coluna = 7
        elif c == 'i' or c == 'I':
            coluna = 8
        else:
            return False
    return coluna,linha,valor

def eh_valido(M,coluna,linha,valor):
    for j in range(9): #Verificando se há valores iguais na linha
        if M[linha][j] == valor:
            return False
    for i in range(9): #Verificando se há valores iguais na coluna
        if M[i][coluna] == valor:
            return False
    #Verificar no bloco se há valores iguais
    x = linha // 3
    y = coluna // 3
    for i in range(x*3 , x*3+3):
        for j in range(y*3,y*3+3):
            if M[i][j] == valor:
                return False
    return True

def resolvido(M): #Para sabermos se um determinado jogo está completo, precisamos verificar se um elemento da matriz ainda é 0
    for i in range(9):
        for j in range(9):
            if M[i][j] == 0:
                return False
    return True

def preencher_de_dicas(arquivo,M):
    with open(arquivo,'r') as lista_dicas: #Abrir o arquivo de dicas
        for dica in lista_dicas: #Pega cada dica da lista inteira de dicas
            coluna,linha,valor = traducao(dica) #Traduz a dica para algo usavel
            if eh_valido(M,coluna,linha,valor): #Determina se essa dica é válida
                M[linha][coluna] = valor
            else:
                return False #Se a dica for inválida, vai ser o gatilho para o arquivo de dicas ser inválido
    return M

def preencher_de_respostas(arquivo,M):
    with open(arquivo,'r') as lista_respostas:
        invalido = []
        for resposta in lista_respostas:
            coluna_str,tanto_faz = resposta.split(',')
            coluna,linha,valor = traducao(resposta)
            if eh_valido(M,coluna,linha,valor):
                M[linha][coluna] = valor
            else:
                invalido.append(f'A jogada ({coluna_str},{linha+1}) = {valor} é inválida!')
    return invalido, resolvido(M)

M = [[0]*9 for _ in range(9)] #Matriz que será usada para armazenar os dados

arquivo_dicas = argv[1]
arquivo_respostas = argv[2]

M = preencher_de_dicas(arquivo_dicas,M) #Preenchendo a grade com as dicas

if not M: #Se a matriz não for preenchida corretamente, ela adquire o valor False, que é o gatilho caso para negar essas dicas
    print('Configuração de dicas inválida!')
else:
    invalido, resultado = preencher_de_respostas(arquivo_respostas,M)

    if len(invalido) > 0:
        print('\n'.join(invalido)) #Como os casos inválidos já são armazenados na formatação correta, basta joinar eles com a quebra de linha
    if resultado:
        print('A grade foi preenchida com sucesso!')
    else:
        print('A grade foi não foi preenchida!')


