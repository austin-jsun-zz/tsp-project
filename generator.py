import random 
edge_weights = list(range(10, 21))
def generate(n, edge_weights):
    """
    Generates an adj matrix that represents a fully connected graph
    using only weights in edge_weights.
    """
    g = [['x'] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            weight = random.choice(edge_weights)
            g[i][j] = weight
            g[j][i] = weight
    return g

def print_mat(mat):
    for row in mat:
        print(str(row))

adj_mat = generate(3, edge_weights)
print_mat(adj_mat)