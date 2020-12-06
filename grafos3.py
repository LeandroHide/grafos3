from queue import Queue 

class Grafos:
    def __init__(self):
        self.numeroVertices = []
        self.adjacentes = []
        self.matrizCapacidade = []
        self.matrizCapacidadeResidual = []
        self.s = 0
        self.t = 0



    def ler(self, arquivo):
        f = open(arquivo, "r")

        fluxo_maximo = 0
        emparelhamento = 0
        contadorLinha = 0

        for x in f:
            linha = x.split()
            if (fluxo_maximo == 0 and emparelhamento == 0):
                if (linha[1] == "Line"):
                    fluxo_maximo = 1
                else:
                    emparelhamento = 1

            if (fluxo_maximo == 1):
                if (contadorLinha == 1):
                    self.numeroVertices = int(linha[1])
                    for i in range(self.numeroVertices+1):
                        self.adjacentes.append([])
                    self.matrizCapacidade = [[0 for x in range(self.numeroVertices+1)] for y in range(self.numeroVertices+1)]
                    self.matrizCapacidadeResidual = [[0 for x in range(self.numeroVertices+1)] for y in range(self.numeroVertices+1)]
                
                if (contadorLinha == 3):
                    self.s = int(linha[1])

                if (contadorLinha == 4):
                    self.t = int(linha[1])

                if (contadorLinha >= 5):
                    self.adjacentes[int(linha[1])].append(int(linha[2]))
                    self.matrizCapacidade[int(linha[1])][int(linha[2])] = int(linha[3])
                    self.matrizCapacidadeResidual[int(linha[1])][int(linha[2])] = int(linha[3])

            if (emparelhamento == 1):
                if (contadorLinha == 3):
                    self.numeroVertices = int(linha[2])
                    for i in range(self.numeroVertices+1):
                        self.adjacentes.append([])

                if (contadorLinha >= 4):
                    self.adjacentes[int(linha[1])].append(int(linha[2]))
                    self.adjacentes[int(linha[2])].append(int(linha[1]))

            contadorLinha += 1
        


    def ford_fulkerson(self):
        f = [[float('inf') for x in range(self.numeroVertices+1)] for y in range(self.numeroVertices+1)]
        for u in range(1, self.numeroVertices+1):
            for v in self.adjacentes[u]:
                f[u][v] = 0

        fluxoMaximo = 0
        fluxoP = float('inf')


        while True:
            p = self.edmonds_karps(f)
            if (p == None):
                break

            for vertice in range(len(p)-1):
                if (self.matrizCapacidadeResidual[p[vertice]][p[vertice+1]] < fluxoP):
                    fluxoP = self.matrizCapacidadeResidual[p[vertice]][p[vertice+1]]

            for vertice in range(len(p)-1):
                if self.matrizCapacidade[p[vertice]][p[vertice+1]] > 0:
                    f[p[vertice]][p[vertice+1]] += fluxoP
                else:
                    f[p[vertice]][p[vertice+1]] -= fluxoP
    
            fluxoMaximo += fluxoP

        print(fluxoMaximo)



    def edmonds_karps(self, f):
        c = []
        a = []
        for i in range(self.numeroVertices+1):
            c.append(False)
            a.append(None)

        c[self.s] = True

        q = Queue()
        q.put(self.s)

        while (q.empty() == False):
            u = q.get()
            for v in self.adjacentes[u]:

                if (c[v] == False and (self.matrizCapacidade[u][v] - f[u][v]) > 0):
                    c[v] = True
                    a[v] = u
                    if (v == self.t):
                        p = [self.t]
                        w = self.t
                        while w != self.s:
                            w = a[w]
                            p = [w] + p
                        return p
                    q.put(v)
        
        return None


    def hopcroft_karp(self):
        d = []
        mate = []
        for _ in range(self.numeroVertices+1):
            d.append(float('inf'))
            mate.append(0)

        m = 0

        while True:
            [diferente, mate, d] = self.bfs(mate, d)
            if diferente == False:
                break
            
            for x in range(1, int(self.numeroVertices/2)+1):
                if (mate[x] == 0):
                    [dfsBoolean, mate, d] = self.dfs(mate, x, d)
                    if (dfsBoolean == True):
                        m += 1

        print("Valor do emparelhamento maximo:", m)

        mate = mate[1:]
        print("Pares: ", end = "")

        for i in range(int(len(mate)/2)):
            print("(" + str(i+1) + ", " + str(mate[i]) + ")", end = " ")

        



    def bfs(self, mate, d):
        q = Queue()
        for x in range(1, int(self.numeroVertices/2)+1):
            if (mate[x] == 0):
                d[x] = 0
                q.put(x)
            else:
                d[x] = float('inf')

        d[0] = float('inf')

        while (q.empty() == False):
            x = q.get()
            if (d[x] < d[0]):
                for y in self.adjacentes[x]:
                    if (d[mate[y]] == float('inf')):
                        d[mate[y]] = d[x] + 1
                        q.put(mate[y])
        
        
        return [d[0] != float('inf'), mate, d]


    def dfs(self, mate, x, d):
        if (x != 0):
            for y in self.adjacentes[x]:
                if (d[mate[y]] == d[x] + 1):
                    [dfsBoolean, mate, d] = self.dfs(mate, mate[y], d)
                    if (dfsBoolean == True):
                        mate[y] = x
                        mate[x] = y
                        return [True, mate, d]

            d[x] = float('inf')
            return [False, mate, d]
        return [True, mate, d]



grafo2 = Grafos()
grafo2.ler("C:\Programmer\Python\Grafos\emparelhamento_maximo\gr128_50.gr")
grafo2.hopcroft_karp()

