reset;

set J; #jobs
set M; #machines
set K; #sequence

param p{j in J}; #processing time of job j
param s{m in M}; #setup time of machine m

var x{k in K, j in J} binary; #x[k,j] = 1 if job j is assigned to position k

