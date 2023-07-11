reset;

set J; #jobs
set M; #machines
set K; #positions

param p{j in J}; #processing time of job j
param s{m in M}; #setup time of machine m

var makespan; #makespan

var x{k in K, j in J} binary; #x[k,j] = 1 if job j is assigned to position k

minimize obj: makespan; #makespane = Cmax

