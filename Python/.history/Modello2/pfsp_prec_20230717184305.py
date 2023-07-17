import gurobipy as gp
from gurobipy import GRB


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
        if(i != j):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name="x[%s,%s]" % (i, j))
        
Cmax = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Cmax")
bigM = model.addVar(vtype=GRB.CONTINUOUS, name="bigM")
#bigM = 10

# Funzione obiettivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Aggiornamento del modello con le variabili definite
model.update()


# Vincoli

constraint1_constr = {}
for i in J:
    for j in J:
        if(i != j):
            constraint1_constr[i, j] = model.addConstr(x[i, j] + x[j, i] == 1, "constraint1[%s,%s]" % (i, j))

assignment_constr = {}
for j in J:
    # assignment_constr[j] = model.addConstr(gp.quicksum(x[i, j] for i in range(1, num_J) if(i != j)) <= 1, "assignment[%s]" % j)
    # oppure
    assignment_constr[j] = model.addConstr(gp.quicksum(x[i, j] for i in range(1, j) if(i != j)) <= (num_J-1), "assignment[%s]" % j)

assignment2_constr = {}
for i in J:
    # assignment2_constr[i] = model.addConstr(gp.quicksum(x[i, j] for j in range(1, num_J) if(i != j)) <= 1, "assignment2[%s]" % i)
    # oppure
    assignment2_constr[i] = model.addConstr(gp.quicksum(x[i, j] for j in range(1, num_J) if(i != j)) <= (num_J-1), "assignment2[%s]" % i)



constraint2_constr = {}
for i in J:
    for j in J:
        if(i != j):
            constraint2_constr[1, i, j] = model.addConstr(C[1, j] >= p[j, 1] + C[1, i] + bigM * (1 - x[i, j]), "constraint2[%s,%s,%s]" % (1, i, j))


constraint3_constr = {}
for i in J:
    #for j in range(i + 1, num_J):
    for j in J:
            if(i != j):
                constraint3_constr[1, i, j] = model.addConstr(C[1, i] >= p[i, 1] + C[1, j] + bigM * x[i, j], "constraint3[%s,%s,%s]" % (1, i, j))

constraint4_constr = {}
for j in J:
    for k in range(2, num_M):
        constraint4_constr[j, k] = model.addConstr(C[k, j] >= C[k - 1, j] + p[j, k] + s[k], "constraint4[%s,%s]" % (j, k))

# constraint3_constr = {}
# for k in M:
#     for j in J:
#         constraint3_constr[k, j] = model.addConstr(C[k, j] >= s[k] + p[j, k], "constraint3[%s,%s]" % (k, j))

constraint5_constr = model.addConstr(Cmax >= C[num_M, num_J], "constraint5")

constraint6_constr = {}
for m in M:
    for i in J:
        constraint6_constr[m, i] = model.addConstr(C[m, i] >= 0, "constraint6[%s,%s]" % (m, i))

constraint7_constr = {}
for k in range(2, num_M):
    for i in J:
        for j in J:
            if i != j:
                y = model.addVar(vtype=GRB.BINARY, name="y[%s,%s,%s]" % (k, i, j))
                model.addConstr(C[k, j] >= C[k, i] + p[j, k] + bigM * (1 - x[i, j]) - bigM * y, name="constraint7_aux1[%s,%s,%s]" % (k, i, j))
                model.addConstr(C[k, j] >= C[k-1, j] + p[j, k] + bigM * (1 - x[i, j]) - bigM * (1 - y), name="constraint7_aux2[%s,%s,%s]" % (k, i, j))
                constraint7_constr[k, i, j] = model.addConstr(y == 1, name="constraint7[%s,%s,%s]" % (k, i, j))

constraint8_constr = {}
for k in range(2, num_M):
    for i in J:
        for j in J:
            if i != j:
                z = model.addVar(vtype=GRB.BINARY, name="z[%s,%s,%s]" % (k, i, j))
                model.addConstr(C[k, i] >= C[k, j] + p[i, k] + bigM * (1 - x[i, j]) - bigM * z, name="constraint8_aux1[%s,%s,%s]" % (k, i, j))
                model.addConstr(C[k, i] >= C[k-1, i] + p[i, k] + C[k, j] + bigM * x[i, j] - bigM * (1 - z), name="constraint8_aux2[%s,%s,%s]" % (k, i, j))
                constraint8_constr[k, i, j] = model.addConstr(z == 1, name="constraint8[%s,%s,%s]" % (k, i, j))

                


model.computeIIS()
model.write("model.ilp")
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

#Print the constraints
# for c in model.getConstrs():
#     print(c)
