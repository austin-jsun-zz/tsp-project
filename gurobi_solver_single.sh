#!/bin/sh
echo "solving ${1} file..."
file_name=${1:16}
res_file="./sol_files/${file_name::${#file_name}-3}.sol"
gurobi_cl TIME_LIMIT=60 ResultFile=$res_file $1