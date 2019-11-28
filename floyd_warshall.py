import math 

"""
Return a matrix of all pairs shortest paths, given an input graph in the 
form of an adjacency matrix. This is the Floyd-Warshall algorithm.
"""
def all_pairs_shortest_paths(adjacency_matrix, number_of_locations):
    n = number_of_locations
    shortest_dist_matrix = [[math.inf] * n for _ in range(n)]
    #initialize same-vertex distance to 0, distance between present edges to 
    #the edge weight
    for i in range(n):
        for j in range(n):
            if (i == j):
                shortest_dist_matrix[i][j] = 0
            elif (adjacency_matrix[i][j] != "x"):
                shortest_dist_matrix[i][j] = adjacency_matrix[i][j]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if (shortest_dist_matrix[i][j] > 
                    shortest_dist_matrix[i][k] + shortest_dist_matrix[k][j]):
                    shortest_dist_matrix[i][j] = shortest_dist_matrix[i][k] + shortest_dist_matrix[k][j]
    
    return shortest_dist_matrix