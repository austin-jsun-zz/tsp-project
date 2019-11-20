import random 
edge_weights = list(range(10, 21))
def generate(n, edge_weights):
    """
    Generates an adj matrix that represents a fully connected graph
    using only weights in edge_weights.
    """
    g = []
    for _ in range(n):
        row = [random.choice(edge_weights) for j in range(n)]
        g.append(row)
    return g
print(generate(3, edge_weights))