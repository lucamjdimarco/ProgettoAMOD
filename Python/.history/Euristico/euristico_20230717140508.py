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

# s = {1: 0, 
#      2: 0, 
#      3: 0,
#      4: 0}

def sortNEHFirstIteration(seq):
    Cmax = 0
    seqNEH = []
    Ctemp1 = {}
    Ctemp2 = {}

    for m in M:
        for j in range(0,len(seq)):
            if m == 1:
                if j == 0:
                    Ctemp1[seq[j], m] = p[seq[j], m]
                else: 
                    Ctemp1[seq[j], m] = Ctemp1[seq[j-1], m] + p[seq[j], m]
            else:
                if j == 0:
                    Ctemp1[seq[j], m] = Ctemp1[seq[j], m-1] + p[seq[j], m]
                else:
                    Ctemp1[seq[j], m] = max(Ctemp1[seq[j-1], m], Ctemp1[seq[j], m-1]) + p[seq[j], m]
    
    seq2 = seq.copy()
    seq2.reverse()

    for m in M:
        for j in range(0, len(seq2)):
            if m == 1:
                if j == 0:
                    Ctemp2[seq2[j], m] = p[seq2[j], m]
                else: 
                    Ctemp2[seq2[j], m] = Ctemp2[seq2[j-1], m] + p[seq2[j], m]
            else:
                if j == 0:
                    Ctemp2[seq2[j], m] = Ctemp2[seq2[j], m-1] + p[seq2[j], m]
                else:
                    Ctemp2[seq2[j], m] = max(Ctemp2[seq2[j-1], m], Ctemp2[seq2[j], m-1]) + p[seq2[j], m]


    #seq[-1] indica l'ultimo elemento della lista
    if Ctemp1[seq[-1], num_M] <= Ctemp2[seq2[-1], num_M]:
        return Ctemp1[seq[-1], num_M], seq
    else:
        return Ctemp2[seq2[-1], num_M], seq2

def sortNEHIteration(seq):
    Cmax = 1000
    seqNEH = []
    Ctemp1 = {}

    #-1
    iteration = len(seq)
    i = 0

    while i < iteration:
        for m in M:
            for j in range(0,len(seq)):
                if m == 1:
                    if j == 0:
                        Ctemp1[seq[j], m] = p[seq[j], m]
                    else: 
                        Ctemp1[seq[j], m] = Ctemp1[seq[j-1], m] + p[seq[j], m]
                else:
                    if j == 0:
                        Ctemp1[seq[j], m] = Ctemp1[seq[j], m-1] + p[seq[j], m]
                    else:
                        Ctemp1[seq[j], m] = max(Ctemp1[seq[j-1], m], Ctemp1[seq[j], m-1]) + p[seq[j], m]
        
        #seq[-1] indica l'ultimo elemento della lista
        Cmax = Ctemp1[seq[-1], num_M]
        seqNEH = seq.copy()
        #print(Cmax)
        #print(seqNEH)

        #scambio i due elementi
        temp = seq[i]
        seq[i] = seq[i+1]
        seq[i+1] = temp
        i = i + 1

    for m in M:
        for j in range(0,len(seq)):
            if m == 1:
                if j == 0:
                    Ctemp1[seq[j], m] = p[seq[j], m]
                else: 
                    Ctemp1[seq[j], m] = Ctemp1[seq[j-1], m] + p[seq[j], m]
            else:
                if j == 0:
                    Ctemp1[seq[j], m] = Ctemp1[seq[j], m-1] + p[seq[j], m]
                else:
                    Ctemp1[seq[j], m] = max(Ctemp1[seq[j-1], m], Ctemp1[seq[j], m-1]) + p[seq[j], m]

            
def main():

    Cmax = 0
    seqNEH = []

    #CALCOLO SOMMA TEMPI DI PROCESSAMENTO DEI JOB
    jobDict = {}
    for j in J:
        sum = 0
        for m in M:
            sum = sum + p[j, m]
        jobDict[j] = sum
    
    #ORDINO I JOB IN BASE AL TEMPO DI PROCESSAMENTO IN ORDINE DECRESCENTE
    sorted_dictionary = sorted(jobDict.items(), key=lambda x: x[1], reverse=True)

    #print(sorted_dictionary[0][1])

    #COSTRUISCO LA SEQUENZA INIZIALE
    seq = []
    for i in range(len(sorted_dictionary)):
        seq.append(sorted_dictionary[i][0])

    #TROVO LA MIGLIORE SEQUENZA TRA I PRIMI DUE JOB
    Cmax, seqNEH = sortNEHFirstIteration(seq[:2])

    #TROVO LA MIGLIORE SEQUENZA
    for j in range(2, len(seq)):
        #inserisco il primo job all'inizio
        seqNEH.insert(0, seq[j])
        Ctemp, seqTemp = sortNEHIteration(seqNEH)
        if Ctemp < Cmax:
            Cmax = Ctemp
            seqNEH = seqTemp

    #print(Cmax)
    #print(seqNEH)



if __name__ == "__main__":
  main()

