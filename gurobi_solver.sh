#!/bin/sh
for f in ./gurobi_inputs/*.lp
do
    echo "solving ${f} file..."
    file_name=${f:16}
    res_file="./gurobi_solutions/${file_name::${#file_name}-3}.sol"
    gurobi_cl TIME_LIMIT=60 ResultFile=$res_file $f
    exit()
done
