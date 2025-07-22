#ANTÔNIO ÍTALO BARROS NOGUEIRA - 581571
#DAVI RABELO DE OLIVEIRA - 581052
#GUSTAVO MELO DE SOUSA - 580490

import sys

def montar_grade_do_arquivo(caminho_arquivo): #lê o arquivo de pistas e monta a grade do arquivo
    grade = [[0 for _ in range(9)] for _ in range(9)]
    pistas_marcadas = [[False for _ in range(9)] for _ in range(9)]
    
    try:
        with open(caminho_arquivo, 'r') as f:
            for linha_str in f:
                linha_limpa = linha_str.strip()
                if linha_limpa and not linha_limpa.startswith('#'):
                    try:
                        partes = linha_limpa.split(':')
                        coordenada = partes[0].split(',')
                        valor = int(partes[1].strip())
                        
                        letra_col = coordenada[0].strip().upper()
                        num_lin = int(coordenada[1].strip())

                        col = ord(letra_col) - ord('A')
                        lin = num_lin - 1
                        
                        #acusa erro caso leia pistas inválidas dos arquivos
                        if grade[lin][col] !=0 or not verificar_movimento_valido(grade, valor, lin, col):
                            print('\033[1;31mO arquivo de pistas apresenta pistas inválidas.\033[0m')
                            sys.exit(1)
                        
                        grade[lin][col] = valor
                        pistas_marcadas[lin][col] = True

                    except (ValueError, IndexError):
                        print(f"Ignorando linha com formato inválido '{linha_limpa}'")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return None, None
    
    return grade, pistas_marcadas

def imprimir_tabuleiro(matriz, pistas_marcadas):
    print('     A   B   C    D   E   F    G   H   I')
    print('  ++---+---+---++---+---+---++---+---+---++')
    for li in range(9):
        if li % 3 == 0 and li != 0:
            print('  ++===+===+===++===+===+===++===+===+===++')
        elif li != 0:
            print('  ++---+---+---++---+---+---++---+---+---++')
        
        print(f'{li + 1} ||', end='')

        for co in range(9):
            if co != 0:
                if co % 3 == 0:
                    print('||', end='')
                else:
                    print('|', end='')

            num = matriz[li][co]
            if num != 0:
                if pistas_marcadas[li][co]:
                    print(f"\033[1;31m{num:^3}\033[0m", end='')
                else:
                    print(f"{num:^3}", end='')
            else:
                print(f"{'':^3}", end='')

        print(f'|| {li + 1}')
    print('  ++---+---+---++---+---+---++---+---+---++')
    print('     A   B   C    D   E   F    G   H   I')


def verificar_movimento_valido(matriz, numero, linha, coluna):
    for i in range(9):
        if matriz[linha][i] == numero or matriz[i][coluna] == numero:
            return False
    quadrante_linha = (linha // 3) * 3
    quadrante_coluna = (coluna // 3) * 3
    for l in range(3):
        for c in range(3):
            if matriz[quadrante_linha + l][quadrante_coluna + c] == numero:
                return False
    return True

def opcoes_possiveis(matriz, linha, coluna): #vê quais números podem ser usados e guarda numa lista
    if matriz[linha][coluna] != 0:
        return []

    opcoes = []
    for numero in range(1, 10):
        if verificar_movimento_valido(matriz, numero, linha, coluna):
            opcoes.append(numero)
    return opcoes

#função que tenta resolver a matriz com base nas dicas
def resolver_sudoku(matriz, pistas_marcadas):
    matriz_ant = [[-1 for _ in range(9)] for _ in range(9)]

    while matriz != matriz_ant: #faz uma cópia da matriz atual para comparar depois

        #cria uma cópia de cada linha da matriz real, pra não deixar que as mudanças em uma matriz alterem a outra
        matriz_ant = [linha[:] for linha in matriz] 

        for linha in range(9):
            for coluna in range(9):
                if matriz[linha][coluna] == 0:
                    opcoes = opcoes_possiveis(matriz, linha, coluna)
                    if len(opcoes) == 1:
                        matriz[linha][coluna] = opcoes[0]
                        pistas_marcadas[linha][coluna] = False

    #vê se todo o tabuleiro foi completado
    for linha in range(9):
        for coluna in range(9):
            if matriz[linha][coluna] == 0:
                return False
    return True

caminho_do_arquivo = sys.argv[1]
         
matriz_jogo, pistas_marcadas = montar_grade_do_arquivo(caminho_do_arquivo) #carrega a matriz do jogo e a marcação das pistas

if matriz_jogo:
            print("--- Módulo Solucionador ---")
            print(f"\nTabuleiro inicial do arquivo {caminho_do_arquivo}")
            imprimir_tabuleiro(matriz_jogo, pistas_marcadas)

            confirmacao = input("\nPressione ENTER para resolver ou 'N' para cancelar: ").upper() #essa parte é a responsável por perguntar se a resposta do sudoku deve ser mostrada ou não
            
            if confirmacao != 'N':
                print("\nIniciando a solução")
                sucesso = resolver_sudoku(matriz_jogo, pistas_marcadas)
                print('Grade preenchida com base nas pistas:')
                imprimir_tabuleiro(matriz_jogo, pistas_marcadas)

                if not sucesso:
                    print()
                    print('\033[1;31mNão foi possível continuar, quantidade de pistas insuficiente.\033[0m')

                    sys.exit(1)
                else:
                    print()
                    print('\033[1;32mSudoku solucionado com sucesso!\033[0m')
                    sys.exit(0)
            else:
                print("Operação cancelada.")
                sys.exit(0)
