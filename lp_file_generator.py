from utils import * 
from student_utils import *


"""
This function generates the final lp file that reduces the problem to 
linear programming. This file is used as an input to Gurobi.
"""
def generate_lp_file(input_file):
    input_data = read_file(input_file)
    number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix = data_parser(input_data)

"""
This function generates the list of edge variables xij for edges in the graph.
This list contains only xij, xji for which there exist an edge between i and j
"""
def generate_edge_list(number_of_locations, adjacency_matrix):
    edge_list = []
    for i in range(0, number_of_locations):
        for j in range(0, number_of_locations):
            if (adjacency_matrix[i][j] != "x"):
                edge_list.append("x" + str(i) + str(j))

    return edge_list

"""
This function maps input locations to an index in the order of their listing
in list_of_locations.
"""
def generate_index_map(list_of_locations, number_of_locations):
    index_map = {}
    for i in range(0, number_of_locations):
        index_map[list_of_locations[i]] = i
    
    return index_map

"""
This function generates the list of clh variables. clh = 1 if we drop off TA 
living at home h at location l, and clh = 0 if we do not drop TA h at l
"""
def generate_clh_list(list_of_locations, list_of_houses, number_of_locations):
    clh_list = []
    index_map = generate_index_map(list_of_locations, number_of_locations)

    for i in range(0, number_of_locations):
        for h in list_of_houses:
            clh_list.append("c" + str(i) + str(index_map[h]))

    return clh_list

"""
This function generates the objective function string that we are attempting
to minimize using LP. 
"""
def generate_objective_function():

    return

"""
This function generates the constraint string that the sum of all clh 
variables for each h is equal to 1, that is, the TA is only dropped off once.
"""
def generate_clh_dropoff_constraints(list_of_locations, list_of_houses, number_of_locations, index_map):
    clh_dropoff_constraints_string = ""
    for h in list_of_houses:
        h_index = str(index_map[h])
        for i in range(0, number_of_locations):
            clh_dropoff_constraints_string += "c" + str(i) + str(h_index) + " "
        clh_dropoff_constraints_string += "= 1" + "\n"
    
    return clh_dropoff_constraints_string

"""
This function generates the constraint string for each location in the graph,
the indegree must equal the outdegree for any location to maintain the tour
property.
"""
def generate_indegree_outdegree_constraints(list_of_locations, number_of_locations):
    indegree_outdegree_constraint_string = ""
    for i in range(0, number_of_locations):
        i_index = str(i)
        for j in range(0, number_of_locations):
            indegree_outdegree_constraint_string += "x" + str(j) + i_index + " - " + "x" + i_index + str(j) + " "
        indegree_outdegree_constraint_string += "= 0" + "\n"
    
    return indegree_outdegree_constraint_string

"""
This function generates constraints which ensure no subtours are selected,
rather one single tour is selected. 
"""
def generate_no_subtours_constraints():

    return

"""
This function generates valid dropoff constraints, essentially, the sum
of indegrees to a vertex must be greater than the corresponding clh. So,
if there is a positive indegree to the vertex, the corresponding clh can
be one. If there is no positive indegree, the vertex is not included in
our tour, and the corresponding clh must be 0 (we cannot dropoff at a vertex
not included in our tour).
"""
def generate_valid_dropoff_constraints():

    return 

"""
This function generates the source constraint which ensures that the source
location is in our tour.
"""
def generate_source_constraint(starting_location, number_of_locations, index_map):
    source_constraint_string = ""
    source_index = str(index_map[starting_location])
    for i in range(0, number_of_locations):
        source_constraint_string += "x" + source_index + str(i) + " "
    source_constraint_string += "> 0"

    return source_constraint_string

"""
This function generates the bounds of the program (sets xij for edges from i
to j not in our graph to 0).
"""
def generate_bounds(number_of_locations, adjacency_matrix):
    bounds_string = ""
    for i in range(0, number_of_locations):
        for j in range(0, number_of_locations):
            if (adjacency_matrix[i][j] == "x"):
                bounds_string += "x" + str(i) + str(j) + " = 0" + "\n"

    return bounds_string

"""
This function specifies which lp variables are restricted to take on the 
values 0 or 1 - all the xij and all the clh.
"""
def generate_binary(list_of_locations, list_of_houses, number_of_locations, adjacency_matrix):
    edge_list = generate_edge_list(number_of_locations, adjacency_matrix)
    clh_list = generate_clh_list(list_of_locations, list_of_houses, number_of_locations)
    xij_string = ""
    clh_string = ""
    binary_string = ""
    for edge in edge_list:
        xij_string += edge + " "

    for clh in clh_list:
        clh_string += clh + " "

    binary_string = xij_string + clh_string 
    return binary_string

"""
This function specifies which lp variables are restricted to take on 
integer values - these are the u variables for elimination of subtour 
constraint.
"""
def generate_integers(number_of_locations):
    u_variables = ""
    for i in range(1, number_of_locations):
        u_variables += "u" + str(i) + " "

    return u_variables




