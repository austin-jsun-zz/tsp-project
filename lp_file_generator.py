from utils import * 
from student_utils import *
from floyd_warshall import * 
import sys
from os import listdir
from os.path import isfile, join

"""
Some global variables for file directories
"""
input_dir = "./inputs/"
gurobi_sol_dir = "./sol_files/"
gurobi_inp = "./gurobi_inputs"
"""
This function generates the final lp file that reduces the problem to 
linear programming. This file is used as an input to Gurobi.
"""
def generate_lp_file(input_file, write_file):
    lp_file_string = ""
    # array to keep track of strings to join at the very end
    # for optimizing string concatenations
    join_strings = []
    input_data = read_file(input_file)
    number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix = data_parser(input_data)
    index_map = generate_index_map(list_of_locations, number_of_locations)

    shortest_dist_matrix = all_pairs_shortest_paths(adjacency_matrix, number_of_locations)
    objective_string = generate_objective_function(list_of_locations, list_of_houses, adjacency_matrix, shortest_dist_matrix, index_map, number_of_locations)
    join_strings.extend(["Minimize" + "\n", objective_string])

    #lp_file_string = ''.join([lp_file_string, "Subject To" + "\n"]) 
    clh_dropoff_string = generate_clh_dropoff_constraints(list_of_locations, list_of_houses, number_of_locations, index_map)
    #lp_file_string = ''.join([lp_file_string, clh_dropoff_string]) 
    indegree_outdegree_string = generate_indegree_outdegree_constraints(list_of_locations, number_of_locations)
    #lp_file_string += indegree_outdegree_string
    no_subtour_string = generate_no_subtours_constraints(number_of_locations)
    #lp_file_string += no_subtour_string
    dropoff_string = generate_valid_dropoff_constraints(list_of_locations, list_of_houses, number_of_locations, index_map)
    #lp_file_string += dropoff_string
    source_string = generate_source_constraint(starting_location, number_of_locations, index_map)
    #lp_file_string += source_string
    join_strings.extend(["Subject To" + "\n", clh_dropoff_string, indegree_outdegree_string,
                    no_subtour_string, dropoff_string, source_string
                    ])

    #lp_file_string += "Bounds" + "\n"
    bounds_string = generate_bounds(number_of_locations, adjacency_matrix)
    #lp_file_string += bounds_string
    join_strings.extend(["Bounds" + "\n", bounds_string])

    #lp_file_string += "Binary" + "\n"
    binary_string = generate_binary(list_of_locations, list_of_houses, number_of_locations, adjacency_matrix)
    #lp_file_string += binary_string
    join_strings.extend(["Binary" + "\n", binary_string])
    

    #lp_file_string += "Integers" + "\n"
    integer_string = generate_integers(number_of_locations)
    #lp_file_string += integer_string
    join_strings.extend(["Integers" + "\n", integer_string])

    #lp_file_string += "End" 
    join_strings.extend(["End"])
    lp_file_string = ''.join(join_strings)
    write_to_file(write_file, lp_file_string)
"""
This function generates the list of edge variables xij for edges in the graph.
This list contains only xij, xji for which there exist an edge between i and j
"""
def generate_edge_list(number_of_locations, adjacency_matrix):
    edge_list = []
    for i in range(0, number_of_locations):
        for j in range(0, number_of_locations):
            if (adjacency_matrix[i][j] != "x"):
                edge_list.append("x" + str(i) + "_" + str(j))

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
            clh_list.append("c" + str(i) + "_" + str(index_map[h]))

    return clh_list

"""
This function generates the objective function string that we are attempting
to minimize using LP. 
"""
def generate_objective_function(list_of_locations, list_of_houses, adjacency_matrix, shortest_dist_matrix, index_map, number_of_locations):
    objective_function_string = "\t"
    edge_list = generate_edge_list(number_of_locations, adjacency_matrix)
    #the edges first
    for i in range(0, len(edge_list)):
        e = edge_list[i]
        if (i != len(edge_list) - 1): 
            objective_function_string += "0.67 " + e + " + "
        else:
            objective_function_string += "0.67 " + e + "\n"
    #the dropoff points next
    objective_function_string += "\t"
    for l in range(number_of_locations):
        for h in list_of_houses:
            h_index = index_map[h]
            objective_function_string += "+ " + str(shortest_dist_matrix[l][h_index]) + " " + "c" + str(l) + "_" + str(h_index) + " "
    objective_function_string += "\n"

    return objective_function_string

"""
This function generates the constraint string that the sum of all clh 
variables for each h is equal to 1, that is, the TA is only dropped off once.
"""
def generate_clh_dropoff_constraints(list_of_locations, list_of_houses, number_of_locations, index_map):
    clh_dropoff_constraints_string = ""
    for h in list_of_houses:
        clh_dropoff_constraints_string += "\t"
        h_index = str(index_map[h])
        for i in range(0, number_of_locations):
            if (i != number_of_locations - 1):
                clh_dropoff_constraints_string += "c" + str(i) + "_" + str(h_index) + " + "
            else:
                clh_dropoff_constraints_string += "c" + str(i) + "_" + str(h_index)
        clh_dropoff_constraints_string += " = 1" + "\n"
    
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
        indegree_outdegree_constraint_string += "\t"
        for j in range(0, number_of_locations):
            if (j != number_of_locations - 1):
                indegree_outdegree_constraint_string += "x" + str(j) + "_" + i_index + " - " + "x" + i_index + "_" + str(j) + " + "
            else:
                indegree_outdegree_constraint_string += "x" + str(j) + "_" + i_index + " - " + "x" + i_index + "_" + str(j)
        indegree_outdegree_constraint_string += " = 0" + "\n"
    
    return indegree_outdegree_constraint_string

"""
This function generates constraints which ensure no subtours are selected,
rather one single tour is selected. 
"""
def generate_no_subtours_constraints(number_of_locations):
    no_subtour_string = ""
    n = str(number_of_locations)
    n_1 = str(number_of_locations - 1)
    for i in range(1, number_of_locations):
        for j in range(1, number_of_locations):
            if (i != j):
                no_subtour_string += "\t" + "u" + str(i) + " - " + "u" + str(j) + " + " + n + " " + "x" + str(i) + "_" + str(j) + " <= " + n_1 + "\n"

    return no_subtour_string

"""
This function generates valid dropoff constraints, essentially, the sum
of indegrees to a vertex must be greater than the corresponding clh. So,
if there is a positive indegree to the vertex, the corresponding clh can
be one. If there is no positive indegree, the vertex is not included in
our tour, and the corresponding clh must be 0 (we cannot dropoff at a vertex
not included in our tour).
"""
def generate_valid_dropoff_constraints(list_of_locations, list_of_houses, number_of_locations, index_map):
    dropoff_constraint_string = ""
    for h in list_of_houses:
        h_index = str(index_map[h])
        for i in range(0, number_of_locations):
            dropoff_constraint_string += "\t"
            i_index = str(i)
            for j in range(0, number_of_locations):
                if (j != number_of_locations - 1):
                    dropoff_constraint_string += "x" + str(j) + "_" + i_index + " + "
                else:
                    dropoff_constraint_string += "x" + str(j) + "_" + i_index
            dropoff_constraint_string += " - " + "c" + i_index + "_" + h_index + " >= 0" + "\n"

    return dropoff_constraint_string

"""
This function generates the source constraint which ensures that the source
location is in our tour.
"""
def generate_source_constraint(starting_location, number_of_locations, index_map):
    source_constraint_string = ""
    source_index = str(index_map[starting_location])
    source_constraint_string += "\t"
    for i in range(0, number_of_locations):
        if (i != number_of_locations - 1):
            source_constraint_string += "x" + source_index + "_" + str(i) + " + "
        else:
            source_constraint_string += "x" + source_index + "_" + str(i)
    source_constraint_string += " > 0" + "\n"

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
                bounds_string += "\t" + "x" + str(i) + "_" + str(j) + " = 0" + "\n"

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
    binary_string = "\t"
    for edge in edge_list:
        xij_string += edge + " "

    for clh in clh_list:
        clh_string += clh + " "

    binary_string += xij_string + clh_string + "\n"
    return binary_string

"""
This function specifies which lp variables are restricted to take on 
integer values - these are the u variables for elimination of subtour 
constraint.
"""
def generate_integers(number_of_locations):
    u_variables = "\t"
    for i in range(1, number_of_locations):
        u_variables += "u" + str(i) + " "

    return u_variables


""" checks if a file in input_dir has .in extension """
def fits_format(file):
    return isfile(file) and file[-3:] == ".in"

def write_lp_files(input_dir):
    inp_files = [f for f in listdir(input_dir) if fits_format(join(input_dir, f))]
    for i, inp_file in enumerate(inp_files):
        # format the .lp name for the input file
        lp_file = inp_file[:-3] + ".lp"
        generate_lp_file(join(input_dir, inp_file), join(gurobi_inp, lp_file))
        print('finished writing: {0}, the {1}th file'.format(lp_file, i))

def main():
    #write_lp_files(input_dir)
    generate_lp_file("./inputs/121_50.in", './gurobi_inputs/121_50.lp')
if __name__ == "__main__":
    main()
#generate_lp_file("./inputs/121_50.in")




