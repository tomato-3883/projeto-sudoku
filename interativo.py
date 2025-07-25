#ATÔNIO ÍTALO BARROS NOGUEIRA - 581571
#DAVI RABELO DE OLIVEIRA - 581052
#GUSTAVO MELO DE SOUSA - 580490

#Importa a biblioteca sys, útil para permitir a entrada e a leitura das pistas
import sys

linhas = 9
colunas = 9

#Marca quais casas são as pistas vindas do arquivo, facilitando a impedir que o jogadar mude ou as apague
pistas_tabuleiro = [[False for _ in range(colunas)] for _ in range(linhas)]

#A lista/matriz do tabuleiro em si
matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]

#Função que define a forma e design do tabuleiro, como está no exemplo do arquivo do trabalho
def tabuleiro_sudoku(matriz):

   print('     A   B   C    D   E   F    G   H   I')
   print('  ++---+---+---++---+---+---++---+---+---++')

   for li in range(9):

     if li % 3 == 0 and li != 0:
       print('  ++===+===+===++===+===+===++===+===+===++')

     elif li != 0:
        print('  ++---+---+---++---+---+---++---+---+---++')

     print(f'{li + 1} ' + ('||'), end ='')

     for co in range(9):
       if co % 3 == 0:
        if co > 2:
         print('||', end ='')

       else:
        print('|', end ='')

       num = matriz[li][co]

       if num !=0:
        
        #Dá a cor vermelhas aos números das pistas
        if pistas_tabuleiro[li][co]:
          print(f"\033[1;31m{num :^3}\033[0m" , end = '')

        else:
          print(f"{num :^3}", end = '')

       else:
         print(f"{'' :^3}" , end = '') 
         
       if co == 8:
         print('||' + f' {li + 1}', end = '')

     print()
   print('  ++---+---+---++---+---+---++---+---+---++')
   print('     A   B   C    D   E   F    G   H   I')
   print()

#Função para validar as jogadas, com base nas regras do Sudoku
def jogada_valida(matriz, linha, coluna, numero, nao_erropista = True):

  valor_original = matriz[linha][coluna]
  matriz[linha][coluna] = 0

  if numero in matriz[linha]:
    if nao_erropista:
      print(f'\033[1;31mO {numero} já existe nessa linha! Faça uma nova jogada.\033[0m')

    matriz[linha][coluna] = valor_original
    return False

  for l in range(9):
    if matriz[l][coluna] == numero:

      if nao_erropista:
        print(f'\033[1;31mO {numero} já existe nessa coluna! Faça uma nova jogada.\033[0m')

      matriz[linha][coluna] = valor_original
      return False

  quadrante_linha = (linha // 3) * 3
  quadrante_coluna = (coluna // 3) * 3

  for l in range(quadrante_linha, quadrante_linha + 3):
    for c in range(quadrante_coluna, quadrante_coluna + 3):
      if matriz[l][c] == numero:

        if nao_erropista:
          print(f'\033[1;31mO {numero} já existe nesse quadrante! Faça uma nova jogada.\033[0m')

        matriz[linha][coluna] = valor_original
        return False

  matriz[linha][coluna] = valor_original
  return True

#Função que permite a flexibilidade no formato das entradas para as jogadas
def posicao(c):
 
 if c == 'A' or c == 'a' or c == 'A ' or c == 'a ':
    co = 1

 if c == 'B' or c == 'b' or c == 'B ' or c == 'b ':
    co = 2

 if c == 'C' or c == 'c' or c == 'C ' or c == 'c ':
    co = 3

 if c == 'D' or c == 'd' or c == 'D ' or c == 'd ':
    co = 4

 if c == 'E' or c == 'e' or c == 'E ' or c == 'e ':
    co = 5

 if c == 'F' or c == 'f' or c == 'F ' or c == 'f ':
    co = 6

 if c == 'G' or c == 'g' or c == 'G ' or c == 'g ':
    co = 7

 if c == 'H' or c == 'h' or c == 'H ' or c == 'h ':
    co = 8

 if c == 'I' or c == 'i' or c == 'I ' or c == 'i ':
    co = 9

 return co

#Função que verifica se o jogador já ganhou o jogo, completando todas as casas
def vitoria(matriz):
  for li in range(9):
    for co in range(9):

      num = matriz[li][co]

      if num == 0 or not jogada_valida(matriz, li, co, num, nao_erropista = False):
        return False
      
  return True

#Trecho que recebe e lê o arquivo indicado pelo jogador, colocando as pistas no tabuleiro/grade
arq_entr = sys.argv[1]
pistas = 0

try:
  with open(arq_entr, 'r')  as txt:

    for linha in txt:
      linha = linha.strip()
      col, lin_num = linha.split(',')
      lin, num = lin_num.split(':')

      col_pst = posicao(col.strip()) - 1
      lin_pst = int(lin.strip()) - 1
      num = int(num.strip())
 
      #Garante a validade das pistas e acusa erro quando encontra uma pistas inválida
      if 0 <= lin_pst < 9 and 0 <= col_pst < 9 and 1 <= num <=9:

        #Acusa erro caso quebra as regras sobre linha, coluna e quadrante do Sudoku
        if not jogada_valida(matriz, lin_pst, col_pst, num, nao_erropista = False):

          matriz[lin_pst][col_pst] = (f'\033[1;31m{num :^3}\033[0m')
          tabuleiro_sudoku(matriz)
          print(f'\033[1;31mO arquivo {arq_entr} apresenta entradas inválidas.\033[0m')
          sys.exit(1)

        #Adiciona a pista caso ela esteja válida  
        else:
          matriz[lin_pst][col_pst] = num
          pistas_tabuleiro[lin_pst][col_pst] = True
          pistas +=1

      #Acusa erro caso as pistas estejam fora do "range" do tabuleiro [A,i] nas colunas e [1,9] nas linhas e nos números
      else:
        print(f'\033[1;31mO arquivo {arq_entr} apresenta entradas inválidas (Fora dos intervalos [A,I] ou [1,9]).\033[0m')
        sys.exit(1)

  #Verifica se as pistas estam no intervalo de [1,80]
  if pistas < 1 or pistas > 80:

    print(f'\033[1;31mO número de pistas não está no intervalo [1,80].\033[0m')
    sys.exit(1)

#Acusa erro caso o arquivo informado não tenha sido encontrado
except FileNotFoundError:
  print(f'\033[1;31mO arquivo {arq_entr} não foi encontrado.\033[0m')
  sys.exit(1)
  
#Printa o tabuleiro a primeira vez já com as pista colocadas
tabuleiro_sudoku(matriz)

#Loop para computar e verificar as jogadas feitas pelo usuário/jogador
while True:
 
 jogada = input('Faça sua jogada (coluna,linha:número): ')
 
 #Verifica que o jogador usou o comando para pedir as possibilidades de jogadas para uma casa
 if jogada.startswith('?'):
   jogada = jogada[1:] 

   co, li = jogada.split(',')
   co = posicao(co) - 1
   li = int(li) - 1

   #Impede o comando e aponta erro caso seja uma casa de pista ou já esteja ocupada
   if 0 <= li < 9 and 0 <= co < 9:
     if matriz[li][co] != 0 or pistas_tabuleiro[li][co]:
        print()
        print('\033[1;31mEssa casa já está ocupada! Esse comando só funciona para casas vazias.\033[0m')
     
     #Analisa e dá as jogadas possíveis para a casa solicitada
     else:
        print()
        print(f"\n\033[1;34mJogadas possíveis para ({jogada}):\033[0m ", end= '')
        
        for n in range(1, 10):
            if jogada_valida(matriz, li, co, n, nao_erropista = False):
                print(f'\033[1;34m{n} \033[0m', end= '')
        print('\n')

   #Apresenta o erro caso o comando seja usado para uma casa que não existe
   else:
      print()
      print('\033[1;31mPosição fora do range do tabuleiro [A,I][1,9]. Faça uma nova jogada.'
         + '\033[0m')

 #Verifica que o jogador usou o comando para apagar uma das jogadas anteriores
 elif jogada.startswith('!'):
   jogada = jogada[1:]

   co, li = jogada.split(',')
   co = posicao(co) - 1
   li = int(li) - 1

   if 0 <= li < 9 and 0 <= co <9:

    #Verfica se a casa é uma pista e impede o comando
    if pistas_tabuleiro[li][co]:
      print()
      print('\033[1;31mEssa casa é uma pista e não pode ser alterada! Faça uma nova jogada.\033[0m')
   
    #Verifica se a casa está vazia e impede o comando
    elif matriz[li][co] == 0:
      print()
      print('\033[1;31mEssa casa já está vazia!\033[0m')

    #Apaga a jogada caso não tenha nenhum dos problemas anteriores
    else:
      matriz[li][co] = 0
      print()
      print('\033[1;34mJogada apagada.\033[0m')

   #Apresenta o erro caso o comando seja usado para uma casa que não existe
   else:
      print()
      print('\033[1;31mPosição fora do range do tabuleiro [A,I][1,9]. Faça uma nova jogada.'
         + '\033[0m')
      
#Caso a entrada não seja nenhum comando específico, faz a verificação da jogada
 else:

  co, li_num = jogada.split(',')
  li, num = li_num.split(':')
  co = posicao(co)

  co = int(co) - 1
  li = int(li) - 1
  num = int(num)

  #Praticamente as mesmas verificações e mensagens de erros dos outros comandos
  if 0 <= li < 9 and 0 <= co < 9 and 1 <= num <=9:

   if pistas_tabuleiro[li][co]:
    print()
    print('\033[1;31mEssa casa é uma pista e não pode ser alterada! Faça uma nova jogada.\033[0m')

   elif matriz[li][co] != 0:
     print()
     sobrescrever = input(f'\033[1;34mEssa casa já está ocupada. Deseja sobrescrever o número? (s/n) \033[0m')

     if sobrescrever == 's':
       if jogada_valida(matriz, li, co, num):
        matriz[li][co] = num
        
   elif jogada_valida(matriz, li, co, num):
    matriz[li][co] = num

  else:
   print()
   print('\033[1;31mPosição fora do range do tabuleiro [A,I][1,9]. Faça uma nova jogada.'
         + '\033[0m')

 print()
 tabuleiro_sudoku(matriz)

 #Verifica a vitória e dá parabéns ao jogador
 if vitoria(matriz):
      print('\n\033[1;32mSudoku concluido! Parabéns!\033[0m\n')
      sys.exit(0)
