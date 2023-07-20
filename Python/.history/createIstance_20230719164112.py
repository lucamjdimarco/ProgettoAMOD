import pickle
import random

J = []
M = [1, 2, 3]

# Inserire 21 così da avere 20 job
for i in range(1, 11):
    J.append(i)

num_M = 3
num_J = len(J)

p = {}

# for i in J:
#     for m in M:
#         p[i, m] = random.randint(1, 10)

lambd = 0.5
for i in J:
    for m in M:
        num = int(random.expovariate(lambd))
        if num == 0:
            num = 1
        else: p[i, m] = num

# Salvataggio delle variabili in un file
data = {
    'J': J,
    'M': M,
    'num_M': num_M,
    'num_J': num_J,
    'p': p
}
with open('dati.pickle', 'wb') as file:
    pickle.dump(data, file)
