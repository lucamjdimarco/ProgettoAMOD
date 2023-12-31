import pickle
import random

J = []
M = [1, 2, 3]

for i in range(1, 36):
    J.append(i)

num_M = 3
num_J = len(J)

p = {}

for i in J:
    for m in M:
        p[i, m] = random.randint(10, 30)


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
