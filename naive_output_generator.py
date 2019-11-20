from utils import *
from student_utils import *
def generate_naive_outputs(filename):
    data = read_file(filename)
    number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix = data_parser(data)
    naive_output = convert_input_to_naive_output_string(starting_location, number_of_houses, list_of_houses)
    write_to_file("./outputs/" + str(number_of_locations) + ".out", naive_output)

def convert_input_to_naive_output_string(starting_location, number_of_houses, list_of_houses):
    naive_output = ""
    naive_output += starting_location + " " + starting_location + "\n"
    naive_output += str(number_of_houses) + "\n"
    naive_output += starting_location + " "
    for h in list_of_houses:
        naive_output += h + " "
    return naive_output

generate_naive_outputs("./inputs/50.in")
generate_naive_outputs("./inputs/100.in")
generate_naive_outputs("./inputs/200.in")

