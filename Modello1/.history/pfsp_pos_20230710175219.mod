reset;

set J; #jobs
set M; #machines
set K; #positions

param p{j in J}; #processing time of job j
param s{m in M}; #setup time of machine m
param pi{j in J} symbolic; #permutation index

var Cmax; 
var C{m in M, k in K}; #completion time of job on position k on machine m

var x{k in K, j in J} binary; #x[k,j] = 1 if job j is assigned to position k

minimize obj: Cmax; 

s.t. assignement{k in K}: sum{j in J} x[k,j] = 1; #each job is assigned to exactly one position
s.t. position{j in J}: sum{k in K} x[k,j] = 1; #each position is assigned to exactly one job
s.t. constraint1{j in J}: C[1,1] >= s[1] + sum{j in J}(ord(pi[j]) = k) * p[j]



