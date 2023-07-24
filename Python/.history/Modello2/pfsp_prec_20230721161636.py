import gurobipy as gp
from gurobipy import GRB
import pickle

# Creazione del modello
model = gp.Model("pfsp_prec")

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

max_completion_time = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="max_completion_time")


# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Aggiornamento del modello con le variabili definite
model.update()

# Vincoli

# for i in J:
#     for j in J:
#         if(i < j):
#             #Vincoli NON LINEARI
#             model.addConstr((x[i,j] == 1) >> (C[1, j] >= p[j, 1] + C[1, i]), "constraint2[%s,%s,%s]" % (1, i, j))
#             model.addConstr((x[i,j] == 0) >> (C[1, i] >= p[i, 1] + C[1, j]), "constraint3[%s,%s,%s]" % (1, i, j))

for i in J:
    for j in J:
        if i < j:
            model.addConstr(C[1, j] >= p[j, 1] + C[1, i] - bigM * (1 - x[i, j]), "constraint2[%s,%s,%s]" % (1, i, j))
            model.addConstr(C[1, i] >= p[i, 1] + C[1, j] - bigM * x[i, j], "constraint3[%s,%s,%s]" % (1, i, j))

y = {}
c = {}
for k in range(2, num_M + 1):
    for i in J:
        for j in J:
            if i < j:
                # Aggiornamento delle variabili y e c usando addVar
                y[k, i, j] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="y[%s,%s,%s]" % (k, i, j))
                c[k, i, j] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="c[%s,%s,%s]" % (k, i, j))

                #model.update()

                model.addGenConstrMax(y[k, i, j], [C[k - 1, j], C[k, i]], name="max_constraint[%s,%s,%s]" % (k, i, j))
                model.addGenConstrMax(c[k, i, j], [C[k - 1, i], C[k, j]], name="max_constraint2[%s,%s,%s]" % (k, i, j))

                # Vincoli NON LINEARI
                # model.addConstr((x[i, j] == 1) >> (C[k, j] >= p[j, k] + y[k, i, j]), "constraint2[%s,%s,%s]" % (k, i, j))
                # model.addConstr((x[i, j] == 0) >> (C[k, i] >= p[i, k] + c[k, i, j]), "constraint3[%s,%s,%s]" % (k, i, j))
                model.addConstr(C[k, j] - p[j, k] - y[k, i, j] >= - bigM * (1 - x[i, j]))
                model.addConstr(C[k, i] - p[i, k] - c[k, i, j] >= - bigM * x[i, j])



constraint4_constr = {}
for j in J:
    for k in range(2, num_M+1):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[j, k] + s[k], "constraint4[%s,%s]" % (j, k))

constraint8_constr = {}
for k in M:
    for j in J:
        constraint8_constr[k, j] = model.addConstr(C[k, j] >= s[k] + p[j, k], "constraint8[%s,%s]" % (k, j))

# Vincolo per trovare il tempo di completamento massimo sull'ultima macchina
model.addGenConstrMax(max_completion_time, [C[num_M, j] for j in J], name="max_completion_constraint")
constraint5_constr = model.addConstr(Cmax >= max_completion_time, "constraint5")

constraint6_constr = {}
for m in M:
    for i in J:
        constraint6_constr[m, i] = model.addConstr(C[m, i] >= 0, "constraint6[%s,%s]" % (m, i))

#MAX TEMPO DI ESECUZIONE = 600 SECONDI
model.setParam('TimeLimit', 600)
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
