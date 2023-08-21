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
bigM = 800

max_completion_time = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="max_completion_time")


# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Aggiornamento del modello con le variabili definite
model.update()

# Vincoli

#VINCOLI DI PRECEDENZA

for k in M:
    for i in J:
        for j in J:
            if(i < j):
                model.addConstr(C[k, j] >= p[j, k] + C[k, i] - bigM * (1 - x[i, j]), "constraint2[%s,%s,%s]" % (1, i, j))
                model.addConstr(C[k, i] >= p[i, k] + C[k, j] - bigM * x[i,j], "constraint2[%s,%s,%s]" % (1, i, j))


constraint4_constr = {}
for j in J:
    for k in range(2, num_M+1):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[j,k], "constraint4[%s,%s]" % (j, k))

constraint8_constr = {}
for k in M:
    for j in J:
        constraint8_constr[k, j] = model.addConstr(C[k, j] >= p[j, k], "constraint8[%s,%s]" % (k, j))

constraint6_constr = {}
for m in M:
    for j in J:
        constraint6_constr[m, i] = model.addConstr(C[m, j] >= 0, "constraint6[%s,%s]" % (m, i))



# Vincolo per trovare il tempo di completamento massimo sull'ultima macchina
model.addGenConstrMax(max_completion_time, [C[num_M, j] for j in J], name="max_completion_constraint")
constraint5_constr = model.addConstr(Cmax >= max_completion_time, "constraint5")

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
