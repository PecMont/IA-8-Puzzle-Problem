## 1. Introdução

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdN6Edz9MtnsgZ2Y9nH311jY20uhUalFau-g&s">
 
 O problema do 8-Puzzle
 O 8-Puzzle é um jogo de tabuleiro onde um tabuleiro 3x3 contém oito peças numeradas de 1 a 8 e um espaço vazio (representado por 0). O objetivo é reorganizar as peças para atingir o estado final: (1,2,3,4,5,6,7,8,0).

# Para resolver esse problema, utilizaremos três algoritmos de busca:
 - **Busca em Largura (BFS):** explora todos os estados em uma determinada profundidade antes de ir para a próxima.
 - **Busca em Profundidade (DFS):** explora o caminho até a profundidade máxima antes de voltar e explorar outras opções.
 - **Busca por Aprofundamento Iterativo (IDFS):** combina os benefícios de DFS e BFS, realizando buscas de profundidade limitada e expandindo iterativamente o limite.

 O objetivo deste relatório é implementar e comparar esses algoritmos para determinar qual deles é mais eficiente.

 ### 2. Implementação
 - `psutil`: Monitora o uso de memória RAM para análise de desempenho.
 - `time`: Mede o tempo de execução dos algoritmos.
 - `deque`: Estrutura de fila eficiente usada no BFS.
 - `estado_objetivo`: Representa a configuração final correta do 8-Puzzle.
 - Definição do 8-Puzzle e geração de sucessores
 
 O tabuleiro é representado como uma tupla de 9 elementos, onde 0 representa o espaço vazio.
 Criamos a função `gerar_sucessores()` para obter todos os estados possíveis a partir do estado atual.

## Implementação do BFS, DFS e IDFS
 Criamos uma função `resolver()` que pode executar BFS ou DFS, dependendo do parâmetro passado.
```py
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
                "nodes_expanded": len(visitados), # Nós expandidos
                "fringe_size": len(fronteira), # Tamanho da fronteira
                "max_fringe_size": max_fringe_size, # Tamanho máximo da fronteira
                "searcjh_depth": profundidade, # Profundidade da busca
                "max_search_depth": max_search_depth, # Profundidade máxima da busca
                "runnung_time": round(fim - inicio, 8), # Tempo de execução
                "max_ram_usage": round(processo.memory_info().rss / (1024 * 1024), 8) # Uso máximo de RAM em MB
            }
        for novo_estado, movimeno in gerar_sucessores(estado_atual):
            fronteira.append((novo_estado, caminho + [movimeno], profundidade + 1))
            max_search_depth= max(max_search_depth, profundidade + 1)
        
    return None  # Retorna None se não encontrar solução
```
