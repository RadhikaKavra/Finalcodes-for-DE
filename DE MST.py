import sys
import math
import numpy as np
from numpy import linalg as LA
import networkx as nx
from matplotlib import pyplot as plt
from collections import defaultdict
def input(): return sys.stdin.readline().rstrip('\r\n')
take_input = lambda: list(map(int, input().split()))

sys.stdin = open('input.txt', 'r') 
sys.stdout = open('output1.txt', 'w') 

Graph = defaultdict(list)
FinalGraph = defaultdict(list)
dist= defaultdict(list)
FinalGraphNodeData = defaultdict(list)
NodeIntervalG = defaultdict(list)
edges = defaultdict(list)
edgeinbetween = defaultdict(list)
edgeIntervalG = defaultdict(list)
edgeDist=defaultdict(list)
def addEdge(graph,u,v):
    graph[u].append(v)
    graph[v].append(u)

n,m = take_input()

for j in range (1,m+1):
    u,v = take_input()
    su = "v"+str(u);
    sv = "v"+str(v);
    addEdge(Graph,su,sv)
    edges[j]=(su,sv)
    edgeinbetween[(su,sv)] = j
    #edgeinbetween[(sv,su)] = j

for j in range (1,n+1):
    vj = "v"+str(j);
    l,r = take_input()
    NodeIntervalG[vj] = (l,r)

for j in range (1,m+1):
    u,v = edges[j]
    l = max(NodeIntervalG[u][0],NodeIntervalG[v][0])
    r = min(NodeIntervalG[u][1],NodeIntervalG[v][1])
    edgeIntervalG[j] = (l,r)
G=nx.Graph()
for k,v in Graph.items():
    G.add_node(k)
    for i in v:
        G.add_edge(k,i)
nx.draw(G,with_labels=1)
plt.title('Given arbitrary Interval graph')
plt.show() 
random_pos = nx.random_layout(G, seed=42)
node_positions = nx.spring_layout(G, pos=random_pos)
#print(node_positions)
pos=node_positions
for j in range(1,m+1):
    u,v=edges[j]
    dist_node=math.sqrt((pos[u][0] - pos[v][0])**2 + (pos[u][1] - pos[v][1])**2)
    edgeDist[j]=dist_node
key=node_positions.keys()
keylist=list(key)
#print(keylist)  
value=node_positions.values()
valuel=list(value) 
v=edgeDist.values()
vlist=list(v)
k=edgeDist.keys()
klist=list(k)
ke=edgeinbetween.keys()
kelist=list(ke)
ve=edgeinbetween.values()
velist=list(ve)
d=[]
def to_int(a):
    a=a[1:]
    return int(a)

C=[]
count=0
for j in range(len(klist)):
    edgejdist=vlist[j]
    #print(edgejdist)
    index=velist.index(klist[j])
    u=kelist[index]
    #print(u)
    u0=u[0]
    u1=u[1]
    in1=keylist.index(u0)
    in2=keylist.index(u1)
    v1=valuel[in1]
    v2=valuel[in2]
    for i in range(len(valuel)):
        t=valuel[i]
        ds1=math.sqrt((v1[0]-t[0])*(v1[0]-t[0]))+((v1[1]-t[1])*(v1[1]-t[1]))
        if ds1<=edgejdist:
            count=count+1        
        ds2=math.sqrt((v2[0]-t[0])*(v2[0]-t[0]))+((v2[1]-t[1])*(v2[1]-t[1]))
        if ds2<=edgejdist:
            count=count+1
    dist[j+1]=count   
    count=0         
#print(dist)
#print(edgeinbetween)    
vl=dist.values()
vll=list(vl)
de=defaultdict(list)
for i in range(len(vll)):
    C.append(vll[i]+vlist[i])
    de[i+1]=vll[i]+vlist[i]
#print('de' ,de)    
#print(C)    
ar=[[to_int(i[0])-1,to_int(i[1])-1,j] for i, j in zip(kelist,C)]
A=np.array(ar)
#print(A)
            
def createAdjMatrix(V, graph):
    adjMatrix =[]
 #create N x N matrix filled with 0 edge weights between all vertices
    for i in range(0, V):
        adjMatrix.append([])
        for j in range(0, V):
            adjMatrix[i].append(0)
      #populate adjacency matrix with correct edge weights
    for i in range(0, len(graph)):
          adjMatrix[graph[i][0]][graph[i][1]] = graph[i][2]
          adjMatrix[graph[i][1]][graph[i][0]] = graph[i][2]
    return adjMatrix
def prims(V, graph):
      # create adj matrix from graph
      adjMatrix = createAdjMatrix(V, graph)
      #arbitrarily choose initial vertex from graph
      vertex = 0
      #initialize empty edges array and empty MST
      MST = []
      edges = []
      visited = []
      minEdge = [None,None,float('inf')]
      #run prims algorithm until we create an MST
      #that contains every vertex from the graph
      while len(MST) != V-1:
          #mark this vertex as visited
          visited.append(vertex)
          #add each edge to list of potential edges
          for r in range(0, V):
              if adjMatrix[vertex][r] != 0:
                  edges.append([vertex,r,adjMatrix[vertex][r]])
          #find edge with the smallest weight to a vertex
          #that has not yet been visited
          for e in range(0, len(edges)):
              if edges[e][2] < minEdge[2] and edges[e][1] not in visited:
                  minEdge = edges[e]
          #remove min weight edge from list of edges
          edges.remove(minEdge)
          #push min edge to MST
          MST.append(minEdge)
          #start at new vertex and reset min edge
          vertex = minEdge[1]
          minEdge = [None,None,float('inf')]
      return MST
s1=0
s2=0
s3=0
graph=ar
num=n
MST=[]
MST=prims(num,graph)
#print(MST)
DE=[]
DS=[]
inf=[]
for i in range(len(MST)):
    z=MST[i]
    y=['v'+str(z[0]+1),'v'+str(z[1]+1),z[2]]
    index=C.index(z[2])
    DE.append(z[2])
    e1=vlist[index]
    DS.append(e1)
    e2=vll[index]
    inf.append(e2)
    s2=s2+e1
    s3=s3+e2
    s1=s1+z[2]
    addEdge(FinalGraph,y[0],y[1]) 
#print(DE)
#print(dict(FinalGraph))
#print('max distance', max(DS))   
print('max DE' , max(DE))
#print('max inf' , max(inf))
#print('T Interference ' , s3)
#print('T distance ' , s2) 
print('DE sum ' ,s1) 
print(dict(FinalGraph))
g=nx.Graph()
for k,v in FinalGraph.items():
    g.add_node(k)
    for i in v:
        g.add_edge(k,i)
        g.add_edge(i,k)
nx.draw(g,with_labels=1)
plt.title('MST')
plt.show()  

#power = (-1,-1)
#
#minmaxtransmission = 0;
#
#for j in FinalGraph:
#    mn = 1e9
#    mx = -1
#    for i in FinalGraph[j]:
#        mn = min(mn,edgeIntervalG[edgeinbetween[(i,j)]][0])
#        mx = max(mx,edgeIntervalG[edgeinbetween[(i,j)]][1])
#    FinalGraphNodeData[j] = (mn,mx)
#    minmaxtransmission = max(mx,minmaxtransmission)
#    if mx>power[1] or (mx==power[1] and mn<power[0]):
#        power = (mn,mx)
#print("min-max node power is :", power)
#print("min max transmission cost:", minmaxtransmission)