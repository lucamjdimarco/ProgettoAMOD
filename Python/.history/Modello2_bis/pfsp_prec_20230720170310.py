import gurobipy as gp
from gurobipy import GRB
import pickle


# Creazione del modello
model = gp.Model("pfsp_prec")

# # Dati
# J = [1, 2, 3, 4, 5]
# M = [1, 2, 3, 4]
# num_J = 5
# num_M = 4

# p = {(1, 1): 10, 
#      (1, 2): 2, 
#      (1, 3): 6, 
#      (1, 4): 4, 
#      (2, 1): 8, 
#      (2, 2): 8, 
#      (2, 3): 12,
#      (2, 4): 5, 
#      (3, 1): 4, 
#      (3, 2): 7, 
#      (3, 3): 4, 
#      (3, 4): 7,
#      (4, 1): 12, 
#      (4, 2): 10, 
#      (4, 3): 2,
#      (4, 4): 10,
#      (5, 1): 5,
#      (5, 2): 4,
#      (5, 3): 8,
#      (5, 4): 11}

with open('../dati.pickle', 'rb') as file:
    data = pickle.load(file)

J = data['J']
M = data['M']
num_M = data['num_M']
num_J = data['num_J']
p = data['p']

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
#bigM = model.addVar(vtype=GRB.CONTINUOUS, name="bigM")
bigM = 100

#y = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="y")
#c = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="c")


# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Aggiornamento del modello con le variabili definite
model.update()


# Vincoli

# constraint2_constr = {}
# for k in M:
#     for i in J:
#         for j in J:
#             if(i < j):
#                 constraint2_constr[k, i, j] = model.addConstr(C[k, j] >= p[j, k] + C[k, i] + (bigM * (1 - x[i, j])), "constraint2[%s,%s,%s]" % (k, i, j))


# constraint3_constr = {}
# for k in M:
#     for i in J:
#         for j in J:
#             if(i < j):
#                 constraint3_constr[k, i, j] = model.addConstr(C[k, i] >= p[i, k] + C[k, j] + (bigM * x[i, j]), "constraint3[%s,%s,%s]" % (1, i, j))

for k in M:
for i in J:
    for j in J:
        if(i < j):
            model.addConstr((x[i,j] == 1) >> (C[1, j] >= p[j, 1] + C[1, i]), "constraint2[%s,%s,%s]" % (1, i, j))
            model.addConstr((x[i,j] == 0) >> (C[1, i] >= p[i, 1] + C[1, j]), "constraint3[%s,%s,%s]" % (1, i, j))

# y = {}
# c = {}
# for k in range(2, num_M + 1):
#     for i in J:
#         for j in J:
#             if i < j:
#                 # Aggiornamento delle variabili y e c usando addVar
#                 y[k, i, j] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="y[%s,%s,%s]" % (k, i, j))
#                 c[k, i, j] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="c[%s,%s,%s]" % (k, i, j))

#                 #model.update()

#                 model.addGenConstrMax(y[k, i, j], [C[k - 1, j], C[k, i]], name="max_constraint[%s,%s,%s]" % (k, i, j))
#                 model.addGenConstrMax(c[k, i, j], [C[k - 1, i], C[k, j]], name="max_constraint2[%s,%s,%s]" % (k, i, j))

#                 # Vincoli condizionali usando y e c
#                 model.addConstr((x[i, j] == 1) >> (C[k, j] >= p[j, k] + y[k, i, j]), "constraint2[%s,%s,%s]" % (k, i, j))
#                 model.addConstr((x[i, j] == 0) >> (C[k, i] >= p[i, k] + c[k, i, j]), "constraint3[%s,%s,%s]" % (k, i, j))



constraint4_constr = {}
for j in J:
    for k in range(2, num_M+1):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[j, k] + s[k], "constraint4[%s,%s]" % (j, k))

constraint8_constr = {}
for k in M:
    for j in J:
        constraint8_constr[k, j] = model.addConstr(C[k, j] >= s[k] + p[j, k], "constraint8[%s,%s]" % (k, j))

constraint5_constr = model.addConstr(Cmax >= C[num_M, num_J], "constraint5")

constraint6_constr = {}
for m in M:
    for i in J:
        constraint6_constr[m, i] = model.addConstr(C[m, i] >= 0, "constraint6[%s,%s]" % (m, i))




# model.computeIIS()
# model.write("model.ilp")                
model.optimize()



# Stampa dei risultati
if model.status == GRB.OPTIMAL:
    
    print("\nC:")
    for m in M:
        for j in J:
            print("C[%s,%s] = %s" % (m, j, C[m, j].x))

    print("\nCmax: %s" % Cmax.x)

if model.status == GRB.INFEASIBLE:
    print("Modello infattibile")
