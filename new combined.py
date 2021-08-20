import re
import sys
import math
import networkx as nx
from matplotlib import pyplot as plt
from collections import defaultdict
def input(): return sys.stdin.readline().rstrip('\r\n')
take_input = lambda: list(map(int, input().split()))

sys.stdin = open('input.txt', 'r') 
sys.stdout = open('out.txt', 'w') 

Graph = defaultdict(list)
FinalGraph = defaultdict(list)
FinalGraphNodeData = defaultdict(list)
NodeIntervalG = defaultdict(list)
edges = defaultdict(list)
edgeinbetween = defaultdict(list)
edgeIntervalG = defaultdict(list)
dist=defaultdict(list)
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
        

def optimalpathcover(n,Graph):
    opc=[]                                #set of distinct path components covering all vertices of graph.
    vertices=["v"+str(i) for i in range(1,n+1)]   
    uncoverV=["v"+str(i) for i in range(1,n+1)]  #list of unvisited vertices
    vi=min(uncoverV)
    vi=uncoverV[n-1]
    num=1                    #num is the number of disjoint path components           
    pnum=vi                 #first path is started with the rightmostvertex of an interval graph
    uncoverV.remove(uncoverV[n-1])
    def s(vi):
            index=vertices.index(vi)
            s=[]
            for j in range(0,len(Graph[vi])):   
                if Graph[vi][j] in uncoverV:
                    idx=vertices.index(Graph[vi][j])
                    if idx>index:
                        s.append(Graph[vi][j])
            return s
    def t(vi):
             index=vertices.index(vi)
             t=[]
             for j in range(len(Graph[vi])):
                if(Graph[vi][j] in uncoverV):
                    idx=vertices.index(Graph[vi][j])
                    if idx<index:
                        t.append(Graph[vi][j])
             return t   
    def rightmostvertex(S):
        ss=''.join(S)
        number=[int(i) for i in re.findall(r'\d+', ss)]
        numlist=sorted(number)
        SList=["v"+str(numlist[i]) for i in range(len(number))]  
        rmv=SList[len(SList)-1]
        return rmv
     
    def leftmostvertex(T):
        tt=''.join(T)
        number=[int(i) for i in re.findall(r'\d+', tt)]
        numlist=sorted(number)
        TList=["v"+str(numlist[i]) for i in range(len(number))]  
        lmv=TList[0]
        return lmv
    
    while uncoverV!=[]:
            S=s(vi)
            T=t(vi)
            if (s(vi)==[] and t(vi)==[]):
                opc.append(pnum)
                u=rightmostvertex(uncoverV)
                num=num+1
                pnum=u  
            elif s(vi)!=[]:
                    u=rightmostvertex(S)
                    v=""
                    for i in reversed(range(len(pnum)-1)):
                        if pnum[i] == 'v':
                            v=pnum[i:]
                            break
                    addEdge(FinalGraph,v,u)
                    # print(u,v)
                    pnum=pnum+u
            else:
                u=leftmostvertex(T)
                v=""
                for i in reversed(range(len(pnum)-1)):
                    if pnum[i] == 'v':
                        v=pnum[i:]
                        break
                # print(u,v,pnum)
                addEdge(FinalGraph,v,u)
                pnum=pnum+u
            vi=u        
            index=uncoverV.index(vi)
            uncoverV.remove(uncoverV[index])  
    opc.append(pnum)
    return opc
opc=optimalpathcover(n,Graph)
print(opc)
G=nx.Graph()
for k,v in Graph.items():
    G.add_node(k)
    for i in v:
        G.add_edge(k,i)
nx.draw(G,with_labels=1)
plt.title('Given arbitrary Interval graph')
plt.show()
#print("optimal path cover :",opc)
random_pos = nx.random_layout(G, seed=42)
node_positions = nx.spring_layout(G, pos=random_pos)
#print(node_positions)
pos=node_positions
#print(edgeDist)
for j in range(1,m+1):
    u,v=edges[j]
    dist_node=math.sqrt((pos[u][0] - pos[v][0])**2 + (pos[u][1] - pos[v][1])**2)
    edgeDist[j]=dist_node
#print('edgeDist' , edgeDist)    
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
vl=dist.values()
vll=list(vl)
for i in range(len(vll)):
    C.append(vll[i]+vlist[i])
#print('C',C)  


def get_List(T):
    number=[int(s) for s in re.findall(r'\d+', T)]
    numlist=sorted(number)
    List=["v"+str(numlist[i]) for i in range(len(number))]  
    return List
def get_Dict(T):
    number=[int(s) for s in re.findall(r'\d+', T)]
    l=["v"+str(number[i]) for i in range(len(number))]
    Dict=dict([ x for x in enumerate(l)])
    return Dict

if len(opc)==1:
    T=opc[0]
    Tlist=get_List(T)
    T_lmv=Tlist[0]
    tdict=get_Dict(T)
    T=nx.path_graph(len(Tlist))
    T.add_nodes_from(tdict)
    T=nx.relabel_nodes(T,tdict)
    nx.draw(T,with_labels=1)
    plt.title("connected routing structure")
    plt.show()


if len(opc)>1:
    T=opc[0]
    opc.remove(T)
    Tlist=get_List(T)
    T_lmv=Tlist[0]
    tdict=get_Dict(T)
    T=nx.path_graph(len(Tlist))
    T.add_nodes_from(tdict)
    T=nx.relabel_nodes(T,tdict)
    
    def minimumrightend(nghT):
        ngh=''.join(nghT)
        number=[int(i) for i in re.findall(r'\d+', ngh)]
        numlist=sorted(number)
        nghList=["v"+str(numlist[i]) for i in range(len(number))]  
        minvalue=nghList[0]
        return minvalue

    def to_int(a):
        a=a[1:]
        return int(a);
    
    while opc!=[]:
        q=opc[0]
        nghq=[]
        nghT=[]
        qlist=get_List(q)
        qdict=get_Dict(q)
        q=nx.path_graph(len(qlist))
        q.add_nodes_from(qdict)
        q=nx.relabel_nodes(q,qdict)
        q_lmv=qlist[0]
        if to_int(q_lmv)<to_int(T_lmv):
            for j in range(len(qlist)):
                z=qlist[j]
                for i in range(len(Tlist)):
                    z1=Tlist[i]
                    #y=edgeinbetween[(z1,z)]
                    if qlist[j] in Graph[z1]:
                        nghT.append(z1)
                #print('nghT',nghT)        
                if nghT!=[]:
                    to=minimumrightend(nghT)
                    #if(to==T_lmv): continue
                    T.add_edge(z,to)
                    addEdge(FinalGraph,z,to)
                    T_lmv=q_lmv
                    T=nx.compose(T,q)
                    Tlist.extend(qlist)
                    S=''.join(Tlist)
                    Tlist=get_List(S)
                    opc.remove(opc[0])
                    break
        else:
            for j in range(len(qlist)):
                z=qlist[j]
                for i in range(len(Tlist)):
                    z1=Tlist[i]
                    #y=edgeinbetween[(z,z1)]
                    if z in Graph[z1]:
                        nghT.append(z1)
                #print('nghT',nghT)        
                if nghT!=[]:
                    to=minimumrightend(nghT)
                    #if(to==T_lmv): continue
                    T.add_edge(z,to)
                    addEdge(FinalGraph,z,to)
                    T=nx.compose(T,q)
                    Tlist.extend(qlist)
                    S=''.join(Tlist)
                    Tlist=get_List(S)
                    opc.remove(opc[0])
                    #T_lmv=q_lmv
                    break 
        if nghT==[]:
            f=opc[0]
            opc.remove(opc[0])
            opc.append(f)
        #print(opc)
        
    nx.draw(T,with_labels=1)
    plt.title("connected routing structure")
    plt.show()        
q=[]
#print(FinalGraph)
for j in FinalGraph:
    for i in FinalGraph[j]:
        q.append(edgeinbetween[(j,i)])
#print('q',q)
newl=[]   
for x in q:
    if x not in newl:
        newl.append(x)  
#print(newl)
d=[] 
for x in range(len(newl)):
    index=klist.index(newl[x])
    d.append(C[index])   
#print(d)        

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

a=0
for i in d:
    a=a+i
print('sum' , a)    
print("min-max node power is :", power)


print("min max transmission cost:", minmaxtransmission)



