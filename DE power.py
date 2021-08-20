# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 13:56:08 2021

@author: AAA
"""
import ast
import math
import numpy as np
import sys
import fileinput
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from itertools import chain
from collections import defaultdict
def input(): return sys.stdin.readline().rstrip('\r\n')
take_input = lambda: list(map(int, input().split()))

sys.stdin = open('input.txt', 'r') 
#sys.stdin=open('output.txt','r')
sys.stdout = open('output1.txt', 'w') 
#fg=open("output.txt")
Graph=defaultdict(list)
FinalGraph=defaultdict(list)
FinalGraphNodeData=defaultdict(list)
NodeIntervalG=defaultdict(list)
edges=defaultdict(list)
edgeinbetween=defaultdict(list)
edgeIntervalG=defaultdict(list)
edgeDist=defaultdict(list)
MST=list()
L=[]

def addEdge(graph,u,v):
    graph[u].append(v)
    graph[v].append(u)

n,m = take_input()

for j in range (1,m+1):
    u,v = take_input()
    su = "v"+str(u);
    sv = "v"+str(v);
    addEdge(Graph,su,sv)
    addEdge(FinalGraph,su,sv)
    edges[j]=(su,sv)
    edgeinbetween[(su,sv)] = j
    edgeinbetween[(sv,su)] = j

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
FinalGraph={'v1': ['v2'], 'v2': ['v1', 'v7', 'v3'], 'v7': ['v2', 'v6'], 'v6': ['v7'], 'v3': ['v2', 'v5'], 'v5': ['v3', 'v8'], 'v8': ['v5', 'v4'], 'v4': ['v8']}
#sum 40.7925690408789

#g=nx.Graph()
#for k,v in FinalGraph.items():
#    g.add_node(k)
#    for i in v:
#        g.add_edge(k,i)
#nx.draw(g,with_labels=1)
#plt.title('MST')
#plt.show()  
power = (-1,-1)

minmaxtransmission = 0;

for j in FinalGraph:
    mn = 1e9
    mx = -1
    for i in FinalGraph[j]:
        mn = min(mn,edgeIntervalG[edgeinbetween[(i,j)]][0])
        mx = max(mx,edgeIntervalG[edgeinbetween[(i,j)]][1])
    FinalGraphNodeData[j] = (mn,mx)
    minmaxtransmission = max(mx,minmaxtransmission)
    if mx>power[1] or (mx==power[1] and mn<power[0]):
        power = (mn,mx)
print("min-max node power is :", power)
print("min max transmission cost:", minmaxtransmission)