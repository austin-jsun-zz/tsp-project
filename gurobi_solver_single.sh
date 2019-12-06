#!/bin/sh
echo "solving ${1} file..."
file_name=${1:16}
res_file="./gurobi_solutions/${file_name::${#file_name}-3}.sol"
gurobi_cl TIME_LIMIT=300 ResultFile=$res_file $1