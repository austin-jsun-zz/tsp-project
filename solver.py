import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
from lp_file_generator import *
import subprocess
from process_sol import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(input_file, list_of_locations, starting_car_location): #list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Old Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    New Input: just the input_file, because it's a lot easier to use lp_file_generator this way
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    #generate the relevant LP file 
    input_dir = "./inputs/"
    gurobi_sol_dir = "./gurobi_solutions/"
    gurobi_inp = "./gurobi_inputs"
    lp_file = input_file[:-3] + ".lp"
    input_file_path = join(input_dir, input_file)
    lp_file_path = join(gurobi_inp, lp_file)
    generate_lp_file(input_file_path, lp_file_path)
    print('finished writing: {0}'.format(lp_file))
    #use gurobi bash script to generate a .sol file 
    subprocess.call(["bash", "./gurobi_solver_single.sh", lp_file_path])
    #use process_sol.py to generate list of locations and a dictionary mapping
    print("finished lp generation")
    sol_file = input_file[:-3] + ".sol"
    sol_file_path = join(gurobi_sol_dir, sol_file)
    pre, ext = os.path.splitext(sol_file_path)
    txt_file_path = pre + ".txt"
    os.rename(sol_file_path, txt_file_path)
    start_index = list_of_locations.index(starting_car_location)
    vertex_path, dropoff_dict = generate_tour_and_dropoffs_from_sol(txt_file_path, start_index)
    print(vertex_path)
    return vertex_path, dropoff_dict

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)
    input_dir = "./inputs/"
    input_file_path = join(input_dir, input_file)
    input_data = utils.read_file(input_file_path)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(input_file, list_locations, starting_car_location)
    #print(car_path)
    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')
    output_files = set(utils.get_files_with_extension(output_directory, 'out'))
    print(output_files)
    for input_file in input_files:
        out_file_path = "outputs/" + input_file[7:-3] + ".out"
        if (out_file_path not in output_files):
            solve_from_file(input_file[7:], output_directory, params=params)
            output_files.add(out_file_path)
            #print(input_file[:-3] + ".out")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
