from utils import *
import re 

"""
This function reads an lp sol file and returns a vertex tour and 
dropoff dictionary which maps each location to a list of TA's dropped 
off at that location. This function should be used in solver.py in the 
solve method. 
"""
def generate_tour_and_dropoffs_from_sol(sol_file, start_index):
    print("start")
    data = read_file(sol_file)
    #print(data)
    edge_list = []
    dropoff_dict = {}
    for line in data: 
        #print(line)
        if (line[0][0] == "x"):
            split_line = re.split('[x_]', line[0])
            #print(split_line)
            vertex_i = int(split_line[1])
            vertex_j = int(split_line[2])
            edge_exists = int(line[1])
            if (edge_exists == 1):
                edge_list.append((vertex_i, vertex_j))
            #print((vertex_i, vertex_j))
        elif (line[0][0] == "c"):
            split_line = re.split('[c_]', line[0])
            vertex_dropoff = int(split_line[1])
            vertex_home = int(split_line[2])
            dropped_off = int(line[1])
            if (dropped_off == 1):
                if vertex_dropoff in dropoff_dict:
                    dropoff_dict[vertex_dropoff].append(vertex_home)
                else:
                    home_list = [vertex_home]
                    dropoff_dict[vertex_dropoff] = home_list
    print(edge_list)
    vertex_tour = return_vertex_tour(edge_list, start_index)

    return vertex_tour, dropoff_dict

"""
This function is a helper function. Given a list of edges consisting of a tour 
and a start vertex, it will return a list of vertices that represents the 
order in which vertices are visited in this tour. 
"""
def return_vertex_tour(edge_list, start_index):
    vertex_tour = []
    curr = start_index
    while (edge_list != []):
        edges_starting_at_curr = [e for e in edge_list if e[0] == curr]
        if (len(edges_starting_at_curr) == 0): 
            break
        curr_edge = edges_starting_at_curr[0]
        vertex_tour.append(curr_edge[0])
        edge_list.remove(curr_edge)
        curr = curr_edge[1]
    vertex_tour.append(start_index)
    return vertex_tour

"""
TEST
edge_list = [(0, 18), (10, 0), (11, 33), (14, 10), (15, 25), (16, 40), (18, 22),
(19, 16), (21, 34), (22, 43), (23, 11), (24, 14), (25, 31), (27, 38), (30, 44),
(31, 30), (33, 45), (34, 24), (36, 21), (38, 36), (40, 23), (43, 15), (44, 19),
(45, 2), (2, 27)]

start = 0

for vertex in return_vertex_tour(edge_list, start):
    print(vertex)
"""
"""
vertex_tour, drop_dict = generate_tour_and_dropoffs_from_sol("./sol_files/121_50.txt", 0)
print(vertex_tour)
print(drop_dict)
"""