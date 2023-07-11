reset;

set J; #jobs
set M; #machines
set K; #positions (sequence of jobs)

param p{j in J}; #processing time of job j
param s{m in M}; #setup time of machine m

var Cmax; 

var C{m in M, k in K}; #completion time of job on position k on machine m

var x{k in K, j in J} binary; #x[k,j] = 1 if job j is assigned to position k

minimize obj: Cmax; 

s.t. assignement{k in K}: sum{j in J} x[k,j] = 1; #each job is assigned to exactly one position

s.t. position{j in J}: sum{k in K} x[k,j] = 1; #each position is assigned to exactly one job

s.t. constraint1: C[1,1] >= s[1] + sum{j in J} p[j] * x[1,j]; #completion time of job 1 on position 1 on machine 1

s.t. constraint2{k in 2..K}: C[1,k] >= s[1] + C[1,k-1] + sum{j in J} p[j] * x[k,j]; #completion time of job j on position k on machine 1

s.t. constraint3{k in K, i in 2..M}: C[i,k] >= C[i-1,k] + sum{j in J} p[j] * x[k,j]; #completion time of job j on position k on machine i

s.t. constraint4{k in K, i in M}: C[i,k] >= s[i] + C[i,k-1] + sum{j in J} p[j] * x[k,j]; #completion time of job j on position k on machine i

s.t. constraint5: Cmax >= C[M,K]; #Cmax is the completion time of the last job on the last position on the last machine

s.t. constraint6{i in M, k in K}: C[i,k] >= 0; #completion time of job j on position k on machine i

s.t. constraint7{j in J, k in K}: x[k,j] >= 0; #x[k,j] = 1 if job j is assigned to position k
