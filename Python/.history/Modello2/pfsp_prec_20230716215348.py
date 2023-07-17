import gurobipy as gp
from gurobipy import GRB

# Creazione del modello
model = gp.Model("pfsp_prec")

# Dati
J = [1, 2, 3, 4, 5]
M = [1, 2, 3, 4]
num_J = 5
num_M = 4

p = {(1, 1): 6, 
     (1, 2): 4, 
     (1, 3): 9, 
     (1, 4): 3, 
     (2, 1): 5, 
     (2, 2): 7, 
     (2, 3): 4,
     (2, 4): 3, 
     (3, 1): 3, 
     (3, 2): 2, 
     (3, 3): 4, 
     (3, 4): 3,
     (4, 1): 6, 
     (4, 2): 5, 
     (4, 3): 4,
     (4, 4): 2,
     (5, 1): 3,
     (5, 2): 4,
     (5, 3): 4,
     (5, 4): 5}

s = {1: 2, 
     2: 3, 
     3: 1,
     4: 4}

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
#bigM = model.addVar(vtype=GRB.CONTINUOUS, name="bigM")
bigM = 10

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

# constraint1_constr = {}
# for k in M:
#     for i in J:
#         for j in range(i + 1, num_J):
#             constraint1_constr[k, i, j] = model.addConstr(C[k, j] >= p[j, k] + C[k, i] + bigM * (1 - x[i, j]), "constraint1[%s,%s,%s]" % (k, i, j))

# ------- AGGIUNTIVE -------

constraint1_constr = {}
for i in range(1, num_J):
    for j in range(1, num_J):
        if(i != j):
            constraint1_constr[i, j] = model.addConstr(x[i, j] + x[j, i] == 1, "constraint1[%s,%s]" % (i, j))

assignment_constr = {}
for j in range(1, num_J):
    assignment_constr[j] = model.addConstr(gp.quicksum(x[i, j] for i in range(1, num_J) if i != j) == 1, "assignment[%s]" % j)

assignment2_constr = {}
for i in range(num_J):
    assignment2_constr[i] = model.addConstr(gp.quicksum(x[i, j] for j in range(1, num_J) if j != i) == 1, "assignment2[%s]" % i)

# ------- FINE AGGIUNTIVE -------

constraint2_constr = {}
for k in M:
    for i in range(1, num_J):
        #for j in range(i + 1, num_J):
        for j in range(1, num_J):
            if(i != j):
                constraint2_constr[k, i, j] = model.addConstr(C[k, i] >= p[i, k] + C[k, j] + bigM * x[i, j], "constraint2[%s,%s,%s]" % (k, i, j))

constraint3_constr = {}
for k in M:
    for j in J:
        constraint3_constr[k, j] = model.addConstr(C[k, j] >= s[k] + p[j, k], "constraint3[%s,%s]" % (k, j))

constraint4_constr = {}
for j in J:
    for k in range(2, num_M + 1):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[j, k], "constraint4[%s,%s]" % (j, k))

constraint5_constr = {}
for j in J:
    constraint5_constr[j] = model.addConstr(C[1, j] >= p[j, 1] + s[1], "constraint5[%s]" % j)

constraint6_constr = model.addConstr(Cmax >= C[num_M, num_J], "constraint6")

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
        for j in J:
            print("C[%s,%s] = %s" % (m, j, C[m, j].x))

    print("\nCmax: %s" % Cmax.x)
