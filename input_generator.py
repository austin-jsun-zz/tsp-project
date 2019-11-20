from adj_matrix_generator import *
import string 
import random 
from utils import *

INPUT_SIZES = [50, 100, 200] #number of vertices in each input file
def generate_inputs():
    """
    Generates inputs in the format specified: 
    number of vertices
    number of TAs
    list of locations 
    list of homes
    source vertex
    adjacency graph 

    Then, writes this data to three files names test1,2,3.in in the inputs folder
    """
    file_num = 1
    for size in INPUT_SIZES:
        max_num_TAs = size / 2 #the maximum number of TAs we can have is half the number of vertices
        numTAs = random.randint(1, max_num_TAs)
        locations = generate_vertex_list(size)
        homes = []
        for i in range(0, numTAs):
            homes.append(locations[i])
        random.shuffle(locations) 
        locations_not_homes = []
        for l in locations: 
            if l not in homes: 
                locations_not_homes.append(l)
        source = random.choice(locations_not_homes)
        adj_matrix = generate_matrix(size)
        input_string = convert_input_data_to_string(size, numTAs, locations, homes, source, adj_matrix)
        write_to_file("./inputs/test" + str(file_num) + ".in", input_string)
        file_num += 1

def generate_vertex_list(size):
    """
    Generates a random list of size size vertices in the form XY where X and Y 
    are random uppercase ASCII characters 
    """
    vertex_list = []
    while (len(vertex_list) != size):
        vertex = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        if vertex not in vertex_list: 
            vertex_list.append(vertex)
    return vertex_list

def convert_input_data_to_string(num_vertices, num_TAs, locations, homes, source, adj_matrix):
    """
    Given the input data that specify the problem, convert it to a string 
    format that can be read in by a solver client 
    """
    input_string = ""
    input_string += str(num_vertices) + "\n"
    input_string += str(num_TAs) + "\n"
    for l in locations:
        input_string += l + " "
    input_string += "\n"
    for h in homes: 
        input_string += h + " "
    input_string += "\n"
    input_string += source + "\n"
    for row in adj_matrix:
        for elem in row: 
            input_string += str(elem) + " "
        input_string += "\n"
    return input_string 
    
generate_inputs()