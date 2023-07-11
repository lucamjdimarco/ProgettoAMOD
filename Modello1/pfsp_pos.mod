reset;

set J; #jobs
set M; #machines

param num_M;
param num_J;

param p{j in J}; #processing time of job j
param s{m in M}; #setup time of machine m

var C{m in M, i in J};

var pi{j in J};  # Sequenza dei job (permutazione)

var x{i in J, j in J} binary; #Variabili di decisione

var Cmax; 

minimize obj: Cmax;

#init var di decisione
s.t. init:
	forall{j in J}
		forall{i in J}
			x[i,j] = if j = pi[i] then 1 else 0;

#each job is assigned to exactly one position
s.t. assignement:
	forall{i in J}
		 sum{j in J} x[i,j] = 1;

#each position is assigned to exactly one job
s.t. position:
	forall{j in J}
		sum{i in J} x[i,j] = 1;
		
#completion time of job on position 1 on machine 1
s.t. constraint1: C[1,1] >= s[1] + sum{j in J} (p[j] * x[1,j]); 

#completion time of job j on position k on machine 1
s.t. constraint2:
	forall{i in 2..num_J} #i in J
		C[1,i] >= s[1] + C[1,i-1] + sum{j in J} p[j] * x[i,j];
		

#completion time of job j on position k on machine i
s.t. constraint3:
	forall{m in 2..num_M, i in J} #m in M
		C[m,i] >= C[m-1,i] + sum{j in J} p[j] * x[i,j];


#completion time of job j on position k on machine i
s.t. constraint4:
	forall{m in M, i in 2..num_J} #i in J
		C[m,i] >= s[m] + C[m,i-1] + sum{j in J} p[j] * x[i,j];

#Cmax is the completion time of the last job on the last position on the last machine
s.t. constraint5: Cmax >= C[2,4]; 

#completion time of job j on position k on machine i
s.t. constraint6:
	forall{m in M, i in J}
		C[m,i] >= 0;
