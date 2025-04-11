# IA 8-Puzzle Game
## 🧑‍🏫 Colaborador
  <table>
    <tr>
      <td align="center">
        <a>
          <img src="https://arquivos.ufrrj.br/arquivos/2023114195c004360761553a8ff546c1c/IMG-20221020-WA0089.jpeg" width="200px;" alt="Foto de Pedro Henrique Guedes"/><br>
          <sub>
            <span style="font-size: 25px;"><b>Pedro H. Guedes</b></span><br>
          </sub>
        </a>
        <a href="https://github.com/PecMont"><b>GitHub</b></a>
      </td>
    </tr>
  </table>

### 1. Introdução

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdN6Edz9MtnsgZ2Y9nH311jY20uhUalFau-g&s">
 
O `8-Puzzle` é um jogo de tabuleiro onde um tabuleiro 3x3 contém oito peças numeradas de 1 a 8 e um espaço vazio (representado por 0). O objetivo é reorganizar as peças para atingir o estado final: (1,2,3,4,5,6,7,8,0).

#### Para resolver esse problema, utilizaremos três algoritmos de busca:
 - Busca em Largura **(BFS):** Explora todos os estados em uma determinada profundidade antes de ir para a próxima.
 - Busca em Profundidade **(DFS):** Explora o caminho até a profundidade máxima antes de voltar e explorar outras opções.
 - Busca por Aprofundamento Iterativo **(IDFS):** Combina os benefícios de DFS e BFS, realizando buscas de profundidade limitada e expandindo iterativamente o limite.

 O objetivo deste relatório é implementar e comparar esses algoritmos para determinar qual deles é mais eficiente.
 
### 2. Implementação
#### 📦 Bibliotecas importadas:
 - `psutil`: Usada para monitorar o uso de memória RAM do processo durante a execução.
 - `time`: Permite medir o tempo de execução dos algoritmos.
 - `deque(de collections)`: Uma fila de duas pontas pontas eficiete.
 - `estado_objetivo`: Representa a configuração final correta do 8-Puzzle.
 
#### 🎯 Estado objetivo:

Define como deve estar o tabuleiro no final da resolução. O número 0 representa o espaço vazio.
 ```py
    estado_objetivo = (1, 2, 3, 4, 5, 6,  7, 8, 0)
```
#### 🔄 Função gerar_sucessores(estado)

Esta função é responsável por gerar todos os possíveis movimentos válidos a partir de um estado atual do tabuleiro do 8-puzzle. É usada por todos os algoritmos de busca (BFS, DFS e IDFS) para explorar os próximos passos possíveis a partir do estado atual. É graças a ela que o agente consegue "navegar" pelo quebra-cabeça.
##### 🧠 Como funciona?
1. Encontra a posição do 0 (o espaço vazio), pois é ele que se move trocando de lugar com os números adjacentes 


2. Define os movimentos possíveis:
    ```py
    movimentos= {
            'Cima': -3,  
            'Baixo': 3,  
            'Esquerda': -1,  
            'Direita': 1  
        }
    ```
     Esses valores indicam a mudança no índice da lista que representa o tabuleiro (3x3, ou seja, 9 posições).

3. Verifica quais movimentos são válidos com base na posição atual do `0`.
    ```py
    if (movimento == 'Cima' and indice_0 > 2) or \
            (movimento == 'Baixo' and indice_0 < 6) or \
            (movimento == 'Esquerda' and indice_0 % 3 != 0) or \
            (movimento == 'Direita' and indice_0 % 3 != 2):
    ```

4. Para cada movimento válido: <br>
<space> - Gera um novo estado trocando o `0` de lugar <br>
<space> - Armazena o novo estado junto com o nome do movimento<br>

#### 🧠 Função `resolver(estado_inicial, algoritmo)`:
 Essa função executa a busca para encontrar o caminho até o estado objetivo, usando o algoritmo escolhido: BFS, DFS ou IDFS. A função `resolver()` é o centro da execução das buscas. Todas as chamadas como `bfs(puzzle)` ou `dfs(puzzle)` usam essa função para resolver o problema.
Se o algoritmo for *IDFS*, a função apenas redireciona para a função `idfs()`, que lida com a lógica separadamente, mas ainda faz parte da estrutura principal de resolução.
##### ⚙️ O que ela faz?
1. Marca o tempo inicial e cria um objeto para medir o uso de memória RAM.

2. Prepara a estrutura de dados da fronteira:

    - deque `(fila)` para BFS
    - lista `(pilha)` para DFS
    - Encaminha para a função `idfs()` se for IDFS

3. Usa um laço while para explorar os nós da fronteira até encontrar a solução.

4. Mantém um conjunto de visitados para evitar ciclos.

5. Para cada estado:

    - Verifica se é o objetivo
    - Gera os sucessores e os adiciona à fronteira
    - Atualiza os dados de profundidade e fronteira máxima

6. Se encontrar a solução, retorna um dicionário com:

    `path_to_goal", "cost_of_path", "nodes_expanded", "fringe_size", "max_fringe_size", "searcjh_depth", "max_search_depth", "runnung_time", "max_ram_usage"`

#### 📌 O que essa célula faz no contexto do projeto
Essa célula define como os três algoritmos centrais `(BFS, DFS, IDFS)` são executados no projeto.
Eles são responsáveis por resolver o problema do `8-puzzle` e também por coletar as estatísticas de desempenho que serão usadas no relatório comparativo entre os algoritmos.
##### 🧠 Funções
- ```py
    def bfs(estado_inicial): e def dfs(estado_inicial):
    ```
    Essas duas funções servem como atalhos simples que apenas chamam a função resolver, informando o tipo de busca desejada `("BFS" ou "DFS")`. Elas deixam o código mais limpo, organizado e fácil de reutilizar em próximos trabalhos.


- ```py
    def idfs(estado_inicial):
    ```

    Implementa o algoritmo de Busca em Profundidade Iterativa `(IDFS)`, que funciona como várias execuções de uma Busca em Profundidade Limitada `(DLS)`, com o limite de profundidade aumentando a cada ciclo `(limite += 1)`.


- ```py
    def dls(estado_atual, caminho, limite, visitados, fringe_size, max_fringe_size):
    ```
    Executa a busca em profundidade com um limite máximo de profundidade:
    - 🚫 Para de explorar quando o limite atinge zero.

    - 🔄 Gera os sucessores do estado atual e continua a busca recursivamente.

    - 📦 Retorna os dados da solução se ela for encontrada (como o caminho e profundidade), ou None caso contrário.

#### 📌"Inicio"
 Esta célula executa os algoritmos de busca `(BFS, DFS e IDFS)` com base no estado inicial definido e exibe os resultados diretamente no console com o comando `print().`
```py
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
```
