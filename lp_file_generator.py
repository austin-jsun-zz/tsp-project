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
This function generates the list of clh variables. clh = 1 if we drop off TA 
living at home h at location l, and clh = 0 if we do not drop TA h at l
"""
def generate_clh_list(list_of_locations, list_of_houses, number_of_locations):
    clh_list = []
    index_map = {}
    for i in range(0, number_of_locations):
        index_map[list_of_locations[i]] = i
        
    for i in range(0, number_of_locations):
        for h in list_of_houses:
            clh_list.append("c" + str(i) + str(index_map[h]))

    return clh_list

