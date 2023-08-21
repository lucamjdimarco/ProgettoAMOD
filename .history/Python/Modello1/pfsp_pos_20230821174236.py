import gurobipy as gp
from gurobipy import GRB
import random
import pickle

# Creazione del modello
model = gp.Model("pfsp_pos")

#Caricamento delle variabili da un file
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
    for i in J:
        C[m, i] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="C[%s,%s]" % (m, i))

x = {}
for i in J:
    for j in J:
        x[i, j] = model.addVar(vtype=GRB.BINARY, name="x[%s,%s]" % (i, j))

Cmax = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Cmax")

# Aggiornamento del modello con le variabili definite
model.update()

# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Vincoli


assignment_constr = {}
for i in J:
    assignment_constr[i] = model.addConstr(gp.quicksum(x[i, j] for j in J) == 1, "assignment[%s]" % i)

position_constr = {}
for j in J:
    position_constr[j] = model.addConstr(gp.quicksum(x[i, j] for i in J) == 1, "position[%s]" % j)

constraint1_constr = model.addConstr(C[1, 1] >= s[1] + gp.quicksum(p[j, 1] * x[1, j] for j in J), "constraint1")

constraint2_constr = {}
for i in range(2, num_J + 1):
    constraint2_constr[i] = model.addConstr(C[1, i] >= s[1] + C[1, i - 1] + gp.quicksum(p[j, 1] * x[i, j] for j in J), "constraint2[%s]" % i)

constraint3_constr = {}
for m in range(2, num_M + 1):
    for i in J:
        constraint3_constr[m, i] = model.addConstr(C[m, i] >= C[m - 1, i] + gp.quicksum(p[j, m] * x[i, j] for j in J), "constraint3[%s,%s]" % (m, i))

constraint4_constr = {}
for m in M:
    for i in range(2, num_J + 1):
        constraint4_constr[m, i] = model.addConstr(C[m, i] >= s[m] + C[m, i - 1] + gp.quicksum(p[j, m] * x[i, j] for j in J), "constraint4[%s,%s]" % (m, i))

constraint5_constr = model.addConstr(Cmax >= C[num_M, num_J], "constraint5")

constraint6_constr = {}
for m in M:
    for i in J:
        constraint6_constr[m, i] = model.addConstr(C[m, i] >= 0, "constraint6[%s,%s]" % (m, i))


#MAX TEMPO DI ESECUZIONE = 600 SECONDI
model.setParam('TimeLimit', 600)
# Risoluzione del modello
model.optimize()

# Stampa dei risultati
if model.status == GRB.OPTIMAL:
    # Get the variables
    x = model.getVars()
    #lista delle variabili di posizione = 1
    xlist = []

    print("\nC:")
    for m in M:
        for i in J:
            print("C[%s,%s] = %s" % (m, i, C[m, i].x))

    # Iterate over the variables
    for i in range(len(x)):
        # Check if the variable has value 1
        if x[i].x == 1:
            # Add the variable to the list
            xlist.append(x[i])

    # Print the list
    print(xlist)

    print("\nCmax: %s" % Cmax.x)
