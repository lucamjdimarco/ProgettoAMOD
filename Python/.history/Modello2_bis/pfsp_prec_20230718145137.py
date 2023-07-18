import gurobipy as gp
from gurobipy import GRB
import pickle


# Creazione del modello
model = gp.Model("pfsp_prec")

# Dati
J = [1, 2, 3, 4, 5]
M = [1, 2, 3, 4]
num_J = 5
num_M = 4

p = {(1, 1): 10, 
     (1, 2): 2, 
     (1, 3): 6, 
     (1, 4): 4, 
     (2, 1): 8, 
     (2, 2): 8, 
     (2, 3): 12,
     (2, 4): 5, 
     (3, 1): 4, 
     (3, 2): 7, 
     (3, 3): 4, 
     (3, 4): 7,
     (4, 1): 12, 
     (4, 2): 10, 
     (4, 3): 2,
     (4, 4): 10,
     (5, 1): 5,
     (5, 2): 4,
     (5, 3): 8,
     (5, 4): 11}

# with open('../dati.pickle', 'rb') as file:
#     data = pickle.load(file)

# J = data['J']
# M = data['M']
# num_M = data['num_M']
# num_J = data['num_J']
# p = data['p']

s = {1: 0, 
     2: 0, 
     3: 0,
     4: 0}

pi = {1: 1, 
      2: 2, 
      3: 3, 
      4: 4,
      5: 5}

# Variabili di decisione
C = {}
for m in M:
    for j in J:
        C[m, j] = model.addVar(vtype=GRB.CONTINUOUS, name="C[%s,%s]" % (m, j))

x = {}
for i in J:
    for j in J:
        if(i < j):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name="x[%s,%s]" % (i, j))
        
Cmax = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Cmax")
bigM = model.addVar(vtype=GRB.CONTINUOUS, name="bigM")


# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Aggiornamento del modello con le variabili definite
model.update()


# Vincoli


constraint2_constr = {}
for k in M:
    for i in J:
        for j in J:
            if(i < j):
                constraint2_constr[k, i, j] = model.addConstr(C[k, j] >= p[j, k] + C[k, i] + (bigM * (1 - x[i, j])), "constraint2[%s,%s,%s]" % (1, i, j))


constraint3_constr = {}
for k in M:
    for i in J:
        #for j in range(i + 1, num_J):
        for j in J:
            if(i < j):
                constraint3_constr[k, i, j] = model.addConstr(C[k, i] >= p[i, k] + C[k, j] + (bigM * x[i, j]), "constraint3[%s,%s,%s]" % (1, i, j))

constraint4_constr = {}
for j in J:
    for k in range(2, num_M):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[j, k] + s[k], "constraint4[%s,%s]" % (j, k))

constraint7_constr = {}
for k in M:
    for j in J:
        constraint7_constr[k, j] = model.addConstr(C[k, j] >= s[k] + p[j, k], "constraint7[%s,%s]" % (k, j))

constraint5_constr = model.addConstr(Cmax >= C[num_M, num_J], "constraint5")

constraint6_constr = {}
for m in M:
    for i in J:
        constraint6_constr[m, i] = model.addConstr(C[m, i] >= 0, "constraint6[%s,%s]" % (m, i))

constraint9_constr = {}
for k in M:
    for i in J:
        constraint9_constr[k, i] = model.addConstr(C[k, i] >= 0, "constraint9[%s,%s]" % (k, i))

                


# model.computeIIS()
# Risoluzione del modello
model.optimize()

# Stampa dei risultati
if model.status == GRB.OPTIMAL:
    print(x)

    print("\nC:")
    for m in M:
        for j in J:
            print("C[%s,%s] = %s" % (m, j, C[m, j].x))

    print("\nCmax: %s" % Cmax.x)

if model.status == GRB.INFEASIBLE:
    print("Modello infattibile")
