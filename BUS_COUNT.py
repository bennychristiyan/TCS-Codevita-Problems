"""
BUS COUNT

Description:
-> M * M matrix : represents distance between each locations.
-> Value of i th row & j th column represents distance between i th & j th places.
-> All locations are connected by roads.
-> 1 st location is office (top left element) [0,0].
-> Distance between i th & j th place = Distance between j th & i th place.
-> Number of people on bus is limited.
-> Bus can start from any location.
-> Bus must take only shortest path to office.
-> Bus can pick up employees along it's route.
-> Assume, there is only 1 shortest path between office and each remaining locations.
-> Determine the minimum number of buses required to pick up all employees

Constraints:
1 < M < 12
0 < Distance between locations < 300
0 < Total number of employees < 500

Time Limit:
1 sec

Input:
M                                                -> Number of locations, including office.
M lines consits of M integers seperated by space -> distance matrix.
M-1 space seperated integers                     -> Number of employees at each location, except office.
An integer representing maximum number of people that can travel in bus at 1 time.

Output:
Minimum number of buses required to pick up all employees to the office.

Example:
I/p:
4
0 10 10 30
10 0 30 20
10 30 0 10
30 20 10 0
23 52 11
25

O/p:
4

Explanation:

(Office [0,0])    ----- 10 -----> (Location 1 (23))
   |          \                    /       |
   10          -------- 30 --------        20
   |          /                    \       |
(Location 2 (52)) ----- 10 -----> (Location 3 (11))

Shortest routes:
Location 1: 1 -> 0 (office)
Location 2: 2 -> 0 (office)
Location 3: 3 -> 2 -> 0 (office)

Bus Count:
Location 1: (23) -> 1 bus (23)
Location 2: (52) -> 25 + 25 + 2 -> 2 bus (50) + remaining 2
Location 3: (11) -> 11 -> 11 + remaining 2 at location 2 is picked up along the bus route of Location 3 -> 1 bus (13)

1 + 2 + 1 = 4
Thus, 4 buses are required to pick up all employees to the office.
"""

# Number of vertices (or locations) in the graph.
M = int(input())
# Adjacency matrix, representing distances between vertices.
dist_mat = []
for i in range(M):
    # Takes a space-separated row of integers as input, representing distances from one vertex to others.
    a = list(map(int, input().split()))
    dist_mat.append(a)
# List of integers representing the number of employees at each vertex (location), except at office.
no_of_emp = list(map(int, input().split()))
# The maximum number of employees a bus can carry at one time.
max_emp = int(input())

# Dijkstra's algotithm to find the shortest route from each location to the office.
class Graph:
    def __init__(self, vertices):
        # Stores the number of vertices in the graph.
        self.v = vertices
        # Creates a 2D list (matrix) of size vertices × vertices initialized with 0. This matrix will later store the adjacency matrix.
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def dijkstra(self, source):
        # List to store the shortest distances from the source (office) to all vertices.
        # Initialized to the largest value (500) for all vertices, except the source (office), which is set to 0.
        dist = [500] * self.v
        dist[source] = 0

        # Boolean list to track which vertices are already processed.
        shortest_path_tree = [False] * self.v
        # List to store the predecessor of each vertex, which helps reconstruct the shortest path later.
        pred = [-1] * self.v
        
        for _ in range(self.v):
            # Finds the vertex u with the smallest distance that hasn't been processed yet.
            u = self.shortest_distance_vertex(dist, shortest_path_tree)
            # Marks vertex u as processed.
            shortest_path_tree[u] = True
            
            # Loops through all vertices v in the graph to check whether each vertex can have its distance improved (shortened) using the currently selected vertex u.
            for v in range(self.v):

                # -> self.graph[u][v] > 0                 : Checks if there is an edge (connection) between vertex u (current vertex being processed) and vertex v.
                # -> not shortest_path_tree[v]            : Ensures that vertex v has not already been included in the shortest path tree.
                # -> dist[v] > dist[u] + self.graph[u][v] : Compares the current shortest known distance to vertex v (dist[v]) with the distance obtained by traveling 
                #                                           through vertex u.
                if(self.graph[u][v] > 0 and not shortest_path_tree[v] and dist[v] > dist[u] + self.graph[u][v]):
                    # -> dist[u]                    : The shortest distance to the current vertex u from the source (office).
                    # -> self.graph[u][v]           : The weight of the edge between vertex u and vertex v.
                    # -> dist[u] + self.graph[u][v] : The potential new shorter distance to vertex v through vertex u.
                    dist[v] = dist[u] + self.graph[u][v]
                    # Sets the predecessor of vertex v to u. This means the shortest known path to v passes through u. This information is used later to reconstruct the 
                    # full path from the source (office) to any vertex.
                    pred[v] = u 

        # Creates an empty list, paths, which will store the reconstructed paths for all vertices in the graph.
        paths = []

        # The goal is to reconstruct the path from the source (office) vertex (assumed to be 0) to each vertex i.
        for i in range(self.v):
            # Calls the reconstruct_path method to compute the shortest path from the source (office) vertex to vertex i.
            # -> pred : The predecessor array stores which vertex leads to another in the shortest path.
            # -> i    : The target vertex for which the path is being reconstructed.
            path = self.reconstruct_path(pred, i)
            paths.append(path)

        # Returns the list paths, which now contains the shortest paths from the source (office) vertex to all other vertices.
        return paths

    # This function finds the vertex with the smallest known distance that hasn't been processed yet. It is used in Dijkstra's algorithm to decide the next vertex to 
    # process.
    # -> dist               : A list of the current shortest distances from the source (office) to all vertices.
    # -> shortest_path_tree : A boolean list indicating whether each vertex has been processed (True) or not (False).
    def shortest_distance_vertex(self, dist, shortest_path_tree):
        # Largest value is used as an initial comparison for finding the minimum distance.
        min = 500
        # Holds the index of the vertex with the smallest distance.
        min_index = -1


        for v in range(self.v):

            # Checks if the current distance to vertex v is smaller than the current minimum (min) and if vertex v has not yet been processed.
            if (dist[v] < min and not shortest_path_tree[v]):
                min = dist[v]
                min_index = v

        # After checking all vertices, return min_index, which is the index of the vertex with the smallest unprocessed distance.
        return min_index

    # This function reconstructs the shortest path from the source (office) vertex to a given target vertex using the pred (predecessor) list.
    # -> pred   : A list where each index contains the predecessor of the corresponding vertex in the shortest path.
    # -> vertex : The target vertex for which the path needs to be reconstructed.
    def reconstruct_path(self, pred, vertex):
        # A list to store the reconstructed path.
        path = []

        # Use a while loop to trace the path backward. The loop continues until vertex is -1, which indicates the source vertex has been reached.
        while vertex != -1:
            # Insert the current vertex at the beginning of the path.
            path.insert(0, vertex)
            # Update vertex to its predecessor (pred[vertex]).
            vertex = pred[vertex]

        # Return the reconstructed path, which is now a list of vertices forming the shortest path from the source (office) to the target.
        return path

# This function identifies the index of the longest path (in terms of the number of vertices) from the list of paths.
# -> path : A list where each element is a path (list of vertices).
def find_max(paths):
    # Start by assuming the longest path is at index 0.
    max_index = 0

    # For each path in paths (starting from index 1).
    for i in range(1, len(paths)):

        # Compare the length of the current path with the length of the path at max_index.
        if len(paths[i]) > len(paths[max_index]):
            max_index = i

    # Return max_index, which is the index of the longest path.
    return max_index

# A Graph object is created with M vertices.
g = Graph(M)
# The adjacency matrix dist_mat (input representing distances between vertices) is assigned to g.graph.
g.graph = dist_mat


# The dijkstra(0) method is called to compute the shortest paths from the source (office) to all vertices. 
# Paths now contains the reconstructed paths from the office to each location.
paths = g.dijkstra(0)

# The path to the office itself (index 0) is removed from paths because it is not needed.
paths.pop(0)

# Tracks the total number of bus trips required.
bus_count = 0
# Tracks the number of locations (other than the office) processed
k = 0

# The loop continues until all M-1 non-office locations are processed.
while k < M-1:
    # Step 1: Find the Longest Path:
    # returns the index of the path with the most vertices (longest route). This ensures buses take the most efficient route covering multiple locations.
    max_index = find_max(paths)
    # The path is adjusted to exclude the office (first vertex) and the destination location (last vertex) using [1:-1].
    route = paths[max_index][1:-1]

    # Step 2: Transport Employees at max_index:
    # Case 1: Employees Fit in One Bus:
    # If the employees at the location indexed by max_index exceed or equal the bus capacity (max_emp).
    if no_of_emp[max_index] >= max_emp:
        # Subtract max_emp from no_of_emp[max_index].
        no_of_emp[max_index] -= max_emp
        # Increment the bus trip counter by 1.
        bus_count += 1

    # Case 2: Employees Fit in Part of a Bus:
    # If the number of employees is less than the bus capacity.
    else:
        # Compute the remaining capacity (max_emp - no_of_emp[max_index]).
        remaining = max_emp - no_of_emp[max_index]
        # Set the employee count at this location to 0.
        no_of_emp[max_index] = 0

        # Transport Employees Along the Route:
        # If the route contains intermediate locations (len(route) != 0)
        if len(route) != 0:

            for i in route:

                # If there is no remaining capacity (remaining == 0), exit the loop.
                if remaining == 0:
                    break

                # If employees at location i-1 fit into the remaining capacity
                if no_of_emp[i-1] <= remaining:
                    # Reduce the remaining capacity by the employee count.
                    remaining -= no_of_emp[i-1]
                    # Set no_of_emp[i-1] to 0.
                    no_of_emp[i-1] = 0

                else:
                    # Reduce the employee count at i-1 by the remaining capacity.
                    no_of_emp[i-1] -= remaining
                    # Set the remaining capacity to 0.
                    remaining = 0
                    # Increment the bus trip counter by 1.
                    bus_count += 1

        # No Route Case:
        else:
            # If there are no intermediate locations in the route, increment the bus trip counter by 1.
            bus_count += 1

    # Step 3: Update Processed Location:
    # If all employees at the max_index location are transported
    if no_of_emp[max_index] == 0:
        # Remove the path from paths and the corresponding employee count from no_of_emp.
        paths.pop(max_index)
        no_of_emp.pop(max_index)
        # Increment k (processed location count).
        k += 1

print(bus_count)
    