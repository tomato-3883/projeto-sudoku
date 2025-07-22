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
                        
                        grade[lin][col] = valor
                        pistas_marcadas[lin][col] = True
                    except (ValueError, IndexError):
                        print(f"Ignorando linha com formato inválido '{linha_limpa}'")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return None, None
    
    return grade, pistas_marcadas

def imprimir_tabuleiro(matriz, pistas_marcadas): #função que imprime a grade e colore de vermelho, conforme requisitado no trabalho
    print('     A   B   C    D   E   F    G   H   I')
    print('  ++---+---+---++---+---+---++---+---+---++')
    for li in range(9):
        if li % 3 == 0 and li != 0:
            print('  ++===+===+===++===+===+===++===+===+===++')
        elif li != 0:
            print('  ++---+---+---++---+---+---++---+---+---++')
        
        print(f'{li + 1} ||', end='')
        for co in range(9):
            if co % 3 == 0:
                print('|', end='')
            
            num = matriz[li][co]
            if num != 0:
                if pistas_marcadas[li][co]:
                    print(f"\033[1;31m{num:^3}\033[0m", end='')
                else:
                    print(f"{num:^3}", end='')
            else:
                print(f"{'.':^3}", end='')
        
        print('|' + f'|| {li + 1}')
    print('  ++---+---+---++---+---+---++---+---+---++')

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

def encontrar_casa_vazia(matriz): #encontra a próxima célula vazia
    for linha in range(9):
        for coluna in range(9):
            if matriz[linha][coluna] == 0:
                return (linha, coluna)
    return None

def solucionar_matriz(matriz): #função principal para responder o sudoku com backtracing
    casa_vazia = encontrar_casa_vazia(matriz)
    if not casa_vazia:
        return True

    linha, coluna = casa_vazia
    for numero_tentativa in range(1, 10):
        if verificar_movimento_valido(matriz, numero_tentativa, linha, coluna):
            matriz[linha][coluna] = numero_tentativa
            if solucionar_matriz(matriz):
                return True
            matriz[linha][coluna] = 0
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Forneça o nome do arquivo de pistas")
        print("python3 solucionador.py arq_01_cfg.txt")
    else:
        caminho_do_arquivo = sys.argv[1]
        
        matriz_jogo, pistas_marcadas = montar_grade_do_arquivo(caminho_do_arquivo) #carrega a matriz do jogo e a marcação das pistas

        if matriz_jogo:
            print("--- Módulo Solucionador ---")
            print(f"\nTabuleiro inicial do arquivo {caminho_do_arquivo}")
            imprimir_tabuleiro(matriz_jogo, pistas_marcadas)

            confirmacao = input("\nPressione ENTER para resolver ou 'N' para cancelar: ").upper() #essa parte é a responsável por perguntar se a resposta do sudoku deve ser mostrada ou não
            
            if confirmacao != 'N':
                print("\nIniciando a solução")
                if solucionar_matriz(matriz_jogo):
                    print("\nSolução possível e encontrada")
                    print("\nTabuleiro Resolvido:")
                    imprimir_tabuleiro(matriz_jogo, pistas_marcadas)
                else:
                    print("\nNão foi possível encontrar uma solução")
            else:
                print("Operação cancelada.")