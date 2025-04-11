import psutil  
import time
from collections import deque

estado_objetivo = (1, 2, 3, 
                   4, 5, 6, 
                   7, 8, 0)  # Estado final esperado

def gerar_sucessores(estado): # Gera os estados sucessores a partir do estado atual
    indice_0 = estado.index(0)  # Encontra a posição do zero
    sucessores = []  # Lista para armazenar os estados sucessores

    movimentos= {
        'Cima': -3,  
        'Baixo': 3,  
        'Esquerda': -1,  
        'Direita': 1  
    }

    for movimento, deslocamento in movimentos.items():
        novo_indice = indice_0 + deslocamento

        if (movimento == 'Cima' and indice_0 > 2) or \
           (movimento == 'Baixo' and indice_0 < 6) or \
           (movimento == 'Esquerda' and indice_0 % 3 != 0) or \
           (movimento == 'Direita' and indice_0 % 3 != 2):
            
            novo_estado = list(estado)
            novo_estado[indice_0], novo_estado[novo_indice] = novo_estado[novo_indice], novo_estado[indice_0]
            sucessores.append((tuple(novo_estado), movimento))  # Adiciona o novo estado e movimento à lista de sucessores
    
    return sucessores

def resolver(estado_inical, algoritmo):
    inicio= time.time() # Marca o tempo de início
    processo= psutil.Process()  # Cria um objeto para monitorar o uso de RAM

    # Define estrutura de dados com base no algoritmo escolhido
    if algoritmo == 'BFS':
        fronteira= deque([(estado_inical, [], 0)]) # Fila
    elif algoritmo == 'DFS':
        fronteira= [(estado_inical, [], 0)]	 # Pilha
    elif algoritmo == "IDFS":
        return idfs(estado_inical)  
    
    visitados= set() #Conjunto que evita ciclos
    max_fringe_size= 0 # Variável para armazenar o tamanho máximo da fronteira
    max_search_depth= 0 # Variável para armazenar a profundidade máxima da busca

    while fronteira:
        max_fringe_size= max(max_fringe_size, len(fronteira)) 

        if algoritmo == 'BFS':
            estado_atual, caminho, profundidade= fronteira.popleft()
        else: # algoritmo == 'DFS'
            estado_atual, caminho, profundidade= fronteira.pop()
        
        if estado_atual in visitados:
            continue
        visitados.add(estado_atual)

        if estado_atual == estado_objetivo:
            fim= time.time()
            return {
                "path_to_goal": caminho, # Caminho para o objetivo
                "cost_of_path": len(caminho), # Custo do caminho
                "searcjh_depth": profundidade, # Profundidade da busca
                "nodes_expanded": len(visitados), # Nós expandidos
                "fringe_size": len(fronteira), # Tamanho da fronteira
                "max_fringe_size": max_fringe_size, # Tamanho máximo da fronteir
                "max_search_depth": max_search_depth, # Profundidade máxima da busca
                "runnung_time": round(fim - inicio, 8), # Tempo de execução
                "max_ram_usage": round(processo.memory_info().rss / (1024 * 1024), 8) # Uso máximo de RAM em MB
            }
        for novo_estado, movimeno in gerar_sucessores(estado_atual):
            fronteira.append((novo_estado, caminho + [movimeno], profundidade + 1))
            max_search_depth= max(max_search_depth, profundidade + 1)
        
    return None  # Retorna None se não encontrar solução

def bfs(estado_inicial):
    return resolver(estado_inicial, "BFS")  

def dfs(estado_inicial):
    return resolver(estado_inicial, "DFS")

def idfs(estado_inicial):
    limite = 0
    max_fringe_size = 0
    nodes_expanded_total = 0
    max_search_depth = 0
    inicio = time.time()
    processo = psutil.Process()

    while True:
        visitados = set()
        resultado, fringe_size, max_fringe_size_iter, profundidade = dls(
            estado_inicial, [], limite, visitados, 0, 0
        )
        max_fringe_size = max(max_fringe_size, max_fringe_size_iter)
        nodes_expanded_total += len(visitados)
        max_search_depth = max(max_search_depth, profundidade)

        if resultado:
            fim = time.time()
            resultado["nodes_expanded"] = nodes_expanded_total 
            resultado["fringe_size"] = fringe_size
            resultado["max_fringe_size"] = max_fringe_size
            resultado["max_search_depth"] = max_search_depth
            resultado["running_time"] = round(fim - inicio, 8)
            resultado["max_ram_usage"] = round(processo.memory_info().rss / (1024 * 1024), 8)
            return resultado

        limite += 1


def dls(estado_atual, caminho, limite, visitados, fringe_size, max_fringe_size):
    if estado_atual == estado_objetivo:
        profundidade = len(caminho)
        return {
            "path_to_goal": caminho,
            "cost_of_path": profundidade,
            "search_depth": profundidade,
        }, fringe_size, max_fringe_size, profundidade

    if limite == 0:
        return None, fringe_size, max_fringe_size, len(caminho)

    visitados.add(estado_atual)
    sucessores = gerar_sucessores(estado_atual)
    fringe_size += len(sucessores)
    max_fringe_size = max(max_fringe_size, fringe_size)
    profundidade_atual = len(caminho)

    for novo_estado, movimento in sucessores:
        if novo_estado not in visitados:
            resultado, fringe_size, max_fringe_size, profundidade = dls(
                novo_estado, caminho + [movimento], limite - 1, visitados, fringe_size, max_fringe_size
            )
            if resultado:
                return resultado, fringe_size, max_fringe_size, profundidade

puzzle = (1, 7, 3, 4, 6, 0, 8, 5, 2)

print("Executando BFS...")
resultado_bfs = bfs(puzzle)
for chave, valor in resultado_bfs.items():
    print(f"{chave}: {valor}")

print("\nExecutando DFS...")
resultado_dfs = dfs(puzzle)
for chave, valor in resultado_dfs.items():
    print(f"{chave}: {valor}")

print("\nExecutando IDFS...")
resultado_idfs = idfs(puzzle)
for chave, valor in resultado_idfs.items():
    print(f"{chave}: {valor}")
