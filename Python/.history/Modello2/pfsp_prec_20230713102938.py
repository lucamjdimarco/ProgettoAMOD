import gurobipy as gp
from gurobipy import GRB

# Creazione del modello
model = gp.Model("pfsp_prec")

# Dati
J = [1, 2, 3, 4, 5]
M = [1, 2, 3, 4]
num_J = 5
num_M = 3

p = {(1, 1): 5, 
     (2, 1): 4, 
     (3, 1): 4, 
     (4, 1): 3, 
     (1, 2): 5, 
     (2, 2): 4, 
     (3, 2): 4,
     (4, 2): 3, 
     (1, 3): 3, 
     (2, 3): 2, 
     (3, 3): 3, 
     (4, 3): 3,
     (1, 4): 6, 
     (2, 4): 4, 
     (3, 4): 4,
     (4, 4): 2,
     (1, 5): 3,
     (2, 5): 4,
     (3, 5): 1,
     (4, 5): 5}

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
        x[i, j] = model.addVar(vtype=GRB.BINARY, name="x[%s,%s]" % (i, j))

Cmax = model.addVar(vtype=GRB.CONTINUOUS, name="Cmax")
bigM = model.addVar(vtype=GRB.CONTINUOUS, name="bigM")

# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Vincoli
# init_constr = {}
# for i in range(1, num_J):
#     for j in range(i + 1, num_J):
#         init_constr[i, j] = model.addConstr(x[i, j] == gp.LinExpr([1 if (i == pi[j] and i + 1 == pi[j + 1]) else 0], [1]), "init[%s,%s]" % (i, j))

# init2_constr = {}
# for j in range(num_J):
#     init2_constr[j] = model.addConstr(x[num_J, j] == gp.LinExpr([1 if (i == pi[j] and i + 1 == pi[j + 1]) else 0], [1]), "init2[%s]" % j)

assignment_constr = {}
for j in range(1, num_J + 1):
    assignment_constr[j] = model.addConstr(gp.quicksum(x[i, j] for i in J if i != j) == 1, "assignment[%s]" % j)

assignment2_constr = {}
for i in range(1, num_J + 1):
    assignment2_constr[i] = model.addConstr(gp.quicksum(x[i, j] for j in J if j != i) == 1, "assignment2[%s]" % i)

constraint1_constr = {}
for k in M:
    for i in J:
        for j in range(i + 1, num_J + 1):
            constraint1_constr[k, i, j] = model.addConstr(C[k, j] >= p[j, k] + C[k, i] - bigM * (1 - x[i, j]), "constraint1[%s,%s,%s]" % (k, i, j))

constraint2_constr = {}
for k in M:
    for i in J:
        for j in J:
            constraint2_constr[k, i, j] = model.addConstr(C[k, i] >= p[k, i] + C[k, j] - bigM * x[i, j], "constraint2[%s,%s,%s]" % (k, i, j))

constraint3_constr = {}
for k in M:
    for j in J:
        constraint3_constr[k, j] = model.addConstr(C[k, j] >= s[k] + p[k, j], "constraint3[%s,%s]" % (k, j))

constraint4_constr = {}
for j in J:
    for k in range(2, num_M + 1):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[k, j], "constraint4[%s,%s]" % (j, k))

constraint5_constr = {}
for j in J:
    constraint5_constr[j] = model.addConstr(C[1, j] >= p[j, 1], "constraint5[%s]" % j)

# Risoluzione del modello
model.optimize()

# Stampa dei risultati
if model.status == GRB.OPTIMAL:
    print("Pi:")
    for j in J:
        print("pi[%s] = %s" % (j, pi[j]))

    print("\nC:")
    for m in M:
        for j in J:
            print("C[%s,%s] = %s" % (m, j, C[m, j].x))

    print("\nCmax: %s" % Cmax.x)
