reset;

set J; #jobs
set M; #machines

param num_M;
param num_J;

param p{m in M, j in J}; #processing time of job j on machine m
param s{m in M}; #setup time of machine m

var C{m in M, i in J};

var pi{j in J};  # Sequenza dei job (permutazione)

var x{i in J, j in J} binary; #Variabili di decisione

var Cmax; 

var bigM;

minimize obj: Cmax;

#init var di decisione
s.t. init:
	forall{i in 1..num_J-1, j in i+1..num_J-1}
		x[i,j] = if (i = pi[j] and i+1 = pi[j+1]) then 1 else 0;
		
#init var di decisione
s.t. init2:
	forall{j in num_J}
		x[num_J,j] = if (i = pi[j] and i+1 = pi[j+1]) then 1 else 0;

s.t. assignement:
	forall{j in 1..num_J}
		 sum{i in J: i <> j} x[i,j] = 1;

s.t. assignement2:
	forall{i in 1..num_J}
		 sum{j in J: j <> i} x[i,j] = 1;
		 
s.t. constraint1:
	forall{k in M, i in J, j in i+1..num_J}
		C[k,j] >= p[k,j] + C[k,i] - bigM * (1-x[i,j]);

s.t. constraint2:
	forall{k in M, i in J, j in J}
		C[k,i] >= p[k,i] + C[k,j] - bigM * x[i,j];

s.t. constraint3:
	forall{k in M, j in J}
		C[k,j] >= s[k] + p[k,j];

s.t. constraint4:
	forall{j in J, k in 2..num_M}
		C[k,j] >= C[k-1,j] + p[k,j];

s.t. constraint5:
	forall{j in J}
		C[1,j] >= p[1,j];