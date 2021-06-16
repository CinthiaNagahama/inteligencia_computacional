from collections import defaultdict

class Graph:
  def __init__(self, adjacents, directional = False, weighted = False):
    if(weighted):
      self.adjacents = defaultdict(list)
    else:
      self.adjacents = defaultdict(set)

    self.weighted = weighted
    self.directional = directional
    self.insert_adjacents(adjacents)

  def insert_adjacents(self, adjacents):
    for k, v in adjacents:
      self.insert_relation(k, v)

  def insert_relation(self, k, v):
    self.adjacents[k].append(v)

    if(not self.directional):
      self.adjacents[v[0]].append([k, v[1]])

  def get_vertices(self):
    return list(self.adjacents.keys())

  def get_vertices_relation(self):
    return [(k, v) for k in self.adjacents.keys() for v in self.adjacents[k]]

  def get_adjacents(self, nodeName):
    if (nodeName not in list(self.adjacents.keys())):
      return "{} não cadastrado".format(nodeName)
    else:
      return [v for v in self.adjacents[nodeName]]

  # Busca em Largura (Breadth-First Search) 
  def bf_search(self, originNode, destinyNode):
    return self.bf_search_weighted_graph(originNode, destinyNode) if(self.weighted) else self.bf_search_non_weighted_graph(originNode, destinyNode)
  
  def bf_search_weighted_graph(self, originNode, destinyNode):
    # Inicializa o caminho e um nó auxiliar
    path = [originNode]
    aux = [originNode]

    while(len(aux) > 0):
      currentName = aux[0]
      # Define em aux_0 uma tupla (aresta atual, vizinhos da aresta atual)
      aux_0 = (currentName, self.get_adjacents(aux[0]))

      # Checa para cada vizinho da aresta atual
      for v, _ in aux_0[1]:
        # Se o vizinho foi testado
        if(v not in path):
          path.append(v)
          aux.append(v)
        # Se o vizinho é o destino
        if(v == destinyNode):
          return path
      _ = aux.pop(0)
    return "{} não encontrado".format(destinyNode)

  def bf_search_non_weighted_graph(self, originNode, destinyNode):
    # Inicializa o caminho e um nó auxiliar
    path = [originNode]
    aux = [originNode]

    while(len(aux) > 0):
      currentName = aux[0]
      # Define em aux_0 uma tupla (aresta atual, vizinhos da aresta atual)
      aux_0 = (currentName, self.get_adjacents(aux[0]))

      # Checa para cada vizinho da aresta atual
      for v in aux_0[1]:
        # Se o vizinho foi testado
        if(v not in path):
          path.append(v)
          aux.append(v)
        # Se o vizinho é o destino
        if(v == destinyNode):
          return path
      _ = aux.pop(0)
    return "{} não encontrado".format(destinyNode)

  # Busca A*
  # f(n) = g(n) + h(n)
    #   g(n) -> distância entre nó atual (n) e próximo nó vizinho
    #   h(n) -> Distância em linha reta até nó destino
  def a_star_search(self, originNode, destinyNode, h):
    notCheckedNodes = [originNode] # Nós que ainda não foram averiguados
    checkedNodes = defaultdict(set) # Nós que foram averiguados {sucessor: antecessor}

    g = {}
    f = {}
    # Inicializa g(n) e f(n) para que todas as chaves existam
    for node in self.get_vertices():
      g[node] = float("inf")
      f[node] = float("inf")

    g[originNode] = 0
    f[originNode] = self.find_h(originNode, h)
    current = originNode

    while(len(notCheckedNodes) != 0):
      # print("current: ", current, "\nnotCheckedNodes: ", notCheckedNodes, "\ncheckedNodes: ", checkedNodes)

      # Atualiza o nó atual com o nó de menor valor f(n) na lista de nós não checados 
      adjF = []
      for node in notCheckedNodes:
        _g = self.find_g(current, node)
        _h = self.find_h(node, h)
        if(type(_g) == int and type(_h) == int):
          adjF.append((node, _g + _h))
      current = min(adjF)[0]
      notCheckedNodes.remove(current)

      # Se o nó atual é o nó destino, retorna o caminho
      if(current == destinyNode):
        return self.a_star_path(checkedNodes, current)

      # Testa o g dos vizinhos do nó atual
      for neighbor, _ in self.get_adjacents(current):
        # Soma o g do nó atual com o peso da aresta entre o nó atual e o nó vizinho
        gResult = g[current] + self.find_g(current, neighbor)

        # Se o resultado da soma for menor que o g ataul do vizinho, então este é o menor caminho já feito até esse nó
        if(gResult < g[neighbor]):
          checkedNodes[neighbor] = current
          g[neighbor] = gResult
          f[neighbor] = gResult + self.find_h(neighbor, h)
          # Adiciona o vizinho na lista de nós não checados
          if(neighbor not in notCheckedNodes):
            notCheckedNodes.append(neighbor)
    return "{} não encontrado".format(destinyNode)

  def find_g(self, node, neighbor):
    if(node == neighbor): 
      return 0
    else:
      g = [v[1] for v in self.get_adjacents(node) if(v[0] == neighbor)]
      return "{} não tem relação direta com {}".format(neighbor, node) if(len(g) == 0) else g.pop(0)

  def find_h(self, node, h):
    h = [v[1] for v in h if(v[0] == node)]
    return "{} não está presente em h".format(node) if(len(h) == 0) else h[0]

  def a_star_path(self, checkedNodes, current):
    path = [current]
    while current in checkedNodes:
      current = checkedNodes[current]
      path.insert(0, current)
    return path

  def __len__(self):
    return len(self.adjacents)

  def __str__(self):
    return "{}({})".format(self.__class__.__name__, dict(self.adjacents))

  def __getitem__(self, v):
    return self.adjacents[v]

citiesRelations = [
  ("Arad", ("Zerind", 75)), 
  ("Arad", ("Timisoara", 118)), 
  ("Arad", ("Sibiu", 140)), 
  ("Zerind", ("Oradea", 71)),
  ("Sibiu", ("Oradea", 151)), 
  ("Sibiu", ("Fagaras", 99)),
  ("Sibiu", ("Rimnicu Vilcea", 80)),
  ("Timisoara", ("Lugoj", 111)), 
  ("Fagaras", ("Bucharest", 211)), 
  ("Rimnicu Vilcea", ("Craiova", 146)),
  ("Rimnicu Vilcea", ("Pitesti", 97)), 
  ("Lugoj", ("Mehadia", 70)), 
  ("Mehadia", ("Dobreta", 75)),
  ("Dobreta", ("Craiova", 120)), 
  ("Craiova", ("Pitesti", 138)),
  ("Pitesti", ("Bucharest", 80)),
  ("Bucharest", ("Giurgiu", 90)),
  ("Bucharest", ("Urziceni", 85)), 
  ("Urziceni", ("Vaslui", 142)),
  ("Urziceni", ("Hirsova", 98)), 
  ("Hirsova", ("Eforie", 86)),
  ("Vaslui", ("Iasi", 92)),
  ("Iasi", ("Neamt", 87))
]

citiesMap = Graph(citiesRelations, False, True)

# print(citiesMap.get_vertices())
# print(citiesMap.get_vertices_relation())
# print(citiesMap.get_adjacents("Arad"))
print(citiesMap.bf_search("Arad", "Bucharest"))

# Distância em linha reta até Bucharest
h = [
  ("Arad", 366),
  ("Bucharest", 0),
  ("Craiova", 160),
  ("Dobreta", 242),
  ("Eforie", 161),
  ("Fagaras", 178),
  ("Giurgiu", 77),
  ("Hirsova", 151),
  ("Iasi", 226),
  ("Logoj", 244),
  ("Mehadia", 241),
  ("Neamt", 234),
  ("Oradea", 380),
  ("Pitesti", 98),
  ("Rimnicu Vilcea", 193),
  ("Sibiu", 253),
  ("Timisoara", 329),
  ("Urziceni", 80),
  ("Vaslui", 199),
  ("Zerind", 374)
]

print(citiesMap.a_star_search("Arad", "Bucharest", h))