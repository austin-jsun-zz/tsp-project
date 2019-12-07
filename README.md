# tsp-project

This project is a solver that finds the optimal paths to solve the Drop the TA's home problem: Given a set of TA's 
and their homes, a set of locations, and a source vertex, what is the optimal path and dropoff combination to minimize 
energy expenditure? Driving costs 2/3 * the weight of an edge in the graph, and if a TA is dropped off at location l and 
must walk home to h, the cost is 1 * the sum of the weight of edges in the path they took. 

A bit of information to run our solver: 
- The inputs folder contains all input problems.
- The outputs folder is where all of the output solutions are written to. 
- Download Gurobi (use an academic license or otherwise) 
- Cd into the tsp-project directory after cloning. 
- Run the following command: python3 solver.py --all inputs outputs 
- If an output file for a given input does not yet exist in the outputs folder, the above command will produce a solution
for the relevant input and put it in the outputs folder, and do this for all files in the inputs folder. 
