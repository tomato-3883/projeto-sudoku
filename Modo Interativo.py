linhas = 9
colunas = 9
cont = 1

#Monta a lista/matriz q vai receber os números de fato
matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]

#Função q define a formatação da grade/tabuleior do Sudoku
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

       if co == 8:
        print('   ||' + f' {li + 1}', end ='')

       num = matriz[li][co]

       print(f"{num if num !=0 else'':^3}", end ='')
     print()
   print('  ++---+---+---++---+---+---++---+---+---++')
   print('     A   B   C    D   E   F    G   H   I')
   print()

#Função q define a validade de uma jogada (Incomplta ainda)
def jogada_valida(matriz, linha, coluna, numero):

  #if matriz[co][li] != 0:
    #print('Espaço já ocupado! Faça uma nova jogada.')
    #return False

  if numero in matriz[linha]:
    print()
    print(f'\033[1;31mO {num} já existe nessa linha! Faça uma nova jogada.' 
          + '\033[0m')
    return False

  for c in range(9):
    if matriz[c][coluna] == numero:
      print()
      print(f'\033[1;31mO {num} já existe nessa coluna! Faça uma nova jogada.'
      + '\033[0m')
      return False

  bloco_linha = (linha // 3) * 3
  bloco_coluna = (coluna // 3) * 3
  for l in range(bloco_linha, bloco_linha + 3):
    for c in range(bloco_coluna, bloco_coluna + 3):
      if matriz[l][c] == numero:
        print()
        print(f'\033[1;31mO {num} já existe nesse quadrante! Faça uma nova jogada.'
        + '\033[0m')
        return False


  return True

#Função q converte as letras da entrada nos números das colunas
def posicao(c):
 if c == 'A' or c == 'a':
    co = 1

 if c == 'B' or c == 'b':
    co = 2

 if c == 'C' or c == 'c':
    co = 3

 if c == 'D' or c == 'd':
    co = 4

 if c == 'E' or c == 'e':
    co = 5

 if c == 'F' or c == 'f':
    co = 6

 if c == 'G' or c == 'g':
    co = 7

 if c == 'H' or c == 'h':
    co = 8

 if c == 'I' or c == 'i':
    co = 9

 return co   

tabuleiro_sudoku(matriz)

#Parte q pega a entrada (Imcompleta, o cont serve pra parar o programa)
while cont <=5:
 jogada = input('Faça sua jogada (coluna,linha:número): ')
 co, li, num = jogada.split(' ')

 co = posicao(co)

 co = int(co) - 1
 li = int(li) - 1
 num = int(num)
 
 #Parte q verifica se linha e coluna jogada estam no intervalo [1,9]
 if 0 <= li < 9 and 0 <= co < 9 and 1 <= num <=9:
  if jogada_valida(matriz, li, co, num):
   matriz[li][co] = num
   cont += 1

 else:
  print()
  print('\033[1;31mPosição fora do range do tabuleiro! Faça uma nova jogada' 
        + '\033[0m')

 print()
 tabuleiro_sudoku(matriz)