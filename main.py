import itertools

# generate bit strings with N-1 ones
def generate_bit_strings(num_edges, num_vertices):   
    
    required_ones = num_vertices - 1 

    for bit_string_tuple in itertools.combinations(range(num_edges), required_ones):
        bit_string = [0] * num_edges
        
        for pos in bit_string_tuple:
            bit_string[pos] = 1
        
        yield bit_string

def read_uwg_file(file_path):
    with open(file_path, 'r') as file:
        n = int(file.readline().strip())  # number of vertices
        m = int(file.readline().strip())  # number of edges
        
        edges = []
        
        # Loop through the next m lines to read the edges
        for _ in range(m):
            line = file.readline().strip()
            vertex1, vertex2, weight = map(int, line.split())
            edges.append((vertex1, vertex2, weight))
       
    return n, m, edges


def is_connected_and_cycle_free(selected_edges, num_vertices):
    
    #Check if the selected edges form a spanning tree
    
    adjacency_list = {i: [] for i in range(1, num_vertices + 1)}  # Vertices are 1-based
    
    for edge in selected_edges:
        vertex1, vertex2 = edge
        adjacency_list[vertex1].append(vertex2)
        adjacency_list[vertex2].append(vertex1)
    visited = set()
    
    def dfs(vertex):
        visited.add(vertex)
        for neighbor in adjacency_list[vertex]:
            if neighbor not in visited:
                dfs(neighbor)
    
    # Start DFS from vertex 1
    dfs(1)
    
    if len(visited) != num_vertices:
        return False
       
    return True

def calculate_weights(selected_edges, mirror_edges, edges):
    
    total_weight = 0
    mirror_weight = 0
    
    # Sum of the selected edges weights
    for edge_index in selected_edges:
        total_weight += edges[edge_index][2]  # The weight is the third element
    
    #  Sum of the mirroe edges weights
    for mirror_index in mirror_edges:
        mirror_weight += edges[mirror_index][2]
    
    return total_weight, mirror_weight

def check_spanning_tree(bit_string, edges, num_vertices, best_weight, indicator):
    
    selected_edges = []
    mirror_edges = []
    EDGEnumber = []
    
    
    for i, bit in enumerate(bit_string):
        if bit == 1:
            selected_edges.append(i)
            mirror_edges.append(len(edges) - 1 - i)  # Mirror index is the reverse in the list
            EDGEnumber.append(i+1)

    # Check if the selected edges form a spanning tree
    edge_list = [(edges[i][0], edges[i][1]) for i in selected_edges] 
    if not is_connected_and_cycle_free(edge_list, num_vertices):
        return False, float('inf'), float('inf'), best_weight, EDGEnumber  # Return infinity weights for invalid spanning trees
    
    total_weight, mirror_weight = calculate_weights(selected_edges, mirror_edges, edges)

    max_weight = max(total_weight, mirror_weight)

    #print("Maximum weight=",max_weight)
    if max_weight<best_weight:
        best_weight=max_weight
        #print("Best Weight",best_weight," From the bit string",bit_string," with edges",EDGEnumber)
        #indicator =1
         
    else:
        #print("Best Weight",best_weight)
        EDGEnumber = [0]
        
      
    return True, total_weight, mirror_weight, best_weight,EDGEnumber

#Main code
file_path = '/Users/lokeshwardevanand/Downloads/test05.uwg'  # Path to the .uwg file
n, m, edges = read_uwg_file(file_path)
best_weight=float('inf')
indicator = int(0)
best_egdes = []
best_egdes_number = []

# Print the output for verification
print("Number of vertices:", n)
print("Number of edges:", m)
#print("Edges (vertex1, vertex2, weight):", edges)


for valid_bit_string in generate_bit_strings(m, n):
    #print("Bit String",valid_bit_string)
    # Check the spanning tree and calculate the weights
    is_valid, total_weight, mirror_weight, best_weight,EDGEnumber = check_spanning_tree(valid_bit_string, edges, n, best_weight, indicator)
   
    # if indicator==1:
    #     best_egdes = edges

    # if is_valid:
    #     print(f"Valid spanning tree found with total weight {total_weight} and mirror weight {mirror_weight}. The current best weight is {best_weight}")
    # else:
    #     print("Invalid spanning tree")
 
    if EDGEnumber != [] and EDGEnumber != [0]:
        best_egdes_number = EDGEnumber[:]

print("The main final output")
if best_egdes_number == [] or best_weight == float('inf'):
    print("NO",end='\n')
else:
    for i in range(len(best_egdes_number)):
        print( best_egdes_number[i],end='\n')

    print(best_weight,end='\n')
