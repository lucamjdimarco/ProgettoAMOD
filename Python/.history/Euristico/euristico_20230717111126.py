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

def sortNEH(seq):
    Cmax = 0
    seqNEH = []
    Ctemp1 = []
    Ctemp2 = []
    for m in M:
        if m == 1:
            for i in seq:
                Ctemp1.append(p[i, m])
        else:
            for i in seq:
                Ctemp1[i] = Ctemp1[i] + p[i, m]
    
    seq.reverse()
    for m in M:
        if m == 1:
            for i in seq:
                Ctemp2.append(p[i, m])
        else:
            for i in seq:
                Ctemp2[i] = Ctemp2[i] + p[i, m]
        
    if Ctemp1[num_J] <= Ctemp2[num_J]:
        return Ctemp1[num_J], seq.reverse()
    else:
        return Ctemp2[num_J], seq
    return Cmax, seqNEH
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
    Cmax, seqNEH = sortNEH(seq[:2])



if __name__ == "__main__":
  main()

