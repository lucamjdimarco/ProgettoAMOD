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
    Ctemp1 = {}
    Ctemp2 = {}

    for m in M:
        for j in seq:
            if m == 1:
                Ctemp1[j, m] = p[j, m]
            else:
                Ctemp1[j, m] = Ctemp1[j, m-1] + p[j, m]
    
    seq2 = seq.copy()
    seq2.reverse()

    for m in M:
        for j in seq2:
            if m == 1:
                Ctemp2[j, m] = p[j, m]
            else:
                Ctemp2[j, m] = Ctemp2[j, m-1] + p[j, m]
    
    print(Ctemp1)
    print(Ctemp2)

    #seq[-1] indica l'ultimo elemento della lista
    if Ctemp1[seq[-1], num_M] <= Ctemp2[seq2[-1], num_M]:
        return Ctemp1[seq[-1], num_M], seq
    else:
        return Ctemp2[seq2[-1], num_M], seq2
            
            
    # for m in M:
    #     if m == 1:
    #         sum = 0
    #         for i in seq:
    #             sum = p[i, m]
    #         Ctemp1.append(sum)
    #     else:
    #         sum = 0
    #         for i in seq:
    #             sum = p[i, m-1] + p[i, m]
    #         Ctemp1.append(sum)
    
    # seq.reverse()
    # for m in M:
    #     if m == 1:
    #         sum = 0
    #         for i in seq:
    #             sum = p[i, m]
    #         Ctemp2.append(sum)
    #     else:
    #         sum = 0
    #         for i in seq:
    #             sum = p[i, m-1] + p[i, m]
    #         Ctemp2.append(sum)
        
    # if Ctemp1[num_J] <= Ctemp2[num_J]:
    #     print(Ctemp1[num_J])
    #     return Ctemp1[num_J], seq.reverse()
    # else:
    #     print(Ctemp2[num_J])
    #     return Ctemp2[num_J], seq
    
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

    print(Cmax)
    print(seqNEH)



if __name__ == "__main__":
  main()


