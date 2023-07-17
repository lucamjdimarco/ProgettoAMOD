import gurobipy as gp
from gurobipy import GRB

# Creazione del modello
model = gp.Model("pfsp_pos")

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
     (2, 2): 22, 
     (2, 3): 12,
     (2, 4): 5, 
     (3, 1): 4, 
     (3, 2): 7, 
     (3, 3): 1, 
     (3, 4): 7,
     (4, 1): 12, 
     (4, 2): 10, 
     (4, 3): 2,
     (4, 4): 10,
     (5, 1): 3,
     (5, 2): 4,
     (5, 3): 8,
     (5, 4): 11}

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
    for i in J:
        C[m, i] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="C[%s,%s]" % (m, i))

x = {}
for i in J:
    for j in J:
        x[i, j] = model.addVar(vtype=GRB.BINARY, name="x[%s,%s]" % (i, j))

#x = model.addVars(J, J, vtype=GRB.BINARY, name="x")

Cmax = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Cmax")

# Aggiornamento del modello con le variabili definite
model.update()

# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Vincoli


# init_constr = {}
# for i in J:
#     for j in J:
#         init_constr[i, j] = model.addConstr(x[i, j] == 1 if j == pi[i] else x[i, j] == 0, "init[%s,%s]" % (i, j))


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

# Risoluzione del modello
model.optimize()

# Stampa dei risultati
if model.status == GRB.OPTIMAL:
    print(x)
    print("Pi:")
    for j in J:
        print("pi[%s] = %s" % (j, pi[j]))

    print("\nC:")
    for m in M:
        for i in J:
            print("C[%s,%s] = %s" % (m, i, C[m, i].x))

    print("\nCmax: %s" % Cmax.x)
