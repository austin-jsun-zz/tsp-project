from utils import *
import re 

def generate_output_from_sol(sol_file, list_of_locations, start):
    data = read_file(sol_file)
    edge_list = []
    dropoff_dict = {}
    for line in data: 
        if (line[0] == "x"):
            split_line = re.split('[x_ ]', line)
            vertex_i = split_line[0]
            vertex_j = split_line[1]
            edge_exists = split_line[2]
            if (edge_exists):
                edge_list.append((vertex_i, vertex_j))
        elif (line[0] == "c"):
            split_line = re.split('[c_ ]', line)
            vertex_dropoff = split_line[0]
            vertex_home = split_line[1]
            dropped_off = split_line[2]
            if vertex_dropoff in dropoff_dict:
                dropoff_dict[vertex_dropoff].add(vertex_home)
            else:
                home_list = [vertex_home]
                dropoff_dict[vertex_dropoff] = home_list

    vertex_tour = return_vertex_tour(edge_list, start)

    return vertex_tour, dropoff_dict

def return_vertex_tour(edge_list, start):
    vertex_tour = []
    curr = start
    while (edge_list != []):
        edges_starting_at_curr = [e for e in edge_list if e[0] == curr]
        curr_edge = edges_starting_at_curr[0]
        vertex_tour.append(curr_edge[0])
        edge_list.remove(curr_edge)
        curr = curr_edge[1]
    vertex_tour.append(start)
    return vertex_tour

edge_list = [(0, 18), (10, 0), (11, 33), (14, 10), (15, 25), (16, 40), (18, 22),
(19, 16), (21, 34), (22, 43), (23, 11), (24, 14), (25, 31), (27, 38), (30, 44),
(31, 30), (33, 45), (34, 24), (36, 21), (38, 36), (40, 23), (43, 15), (44, 19),
(45, 2), (2, 27)]

start = 0

for vertex in return_vertex_tour(edge_list, start):
    print(vertex)
