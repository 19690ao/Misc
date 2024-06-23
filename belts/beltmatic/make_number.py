def add(a, b):
    return a+b

def mult(a, b):
    return a*b

def minimal_solutions(target, using):
    if target in using:
        return []
    # Starting to realize the graph
    operator_count = 0
    operator_dict = {add: '+', mult: '*'}
    found_solutions = []
    found = False
    queue = using.copy()
    visited = dict([(start, 0) for start in queue])
    parent = dict([(start, []) for start in queue])

    while queue:
        current_node = queue.pop(0)
        if found and visited[current_node] > visited[target]-1:
            break
        adjacent_edges = [(operator, operand) for operator in operator_dict.keys() for operand in using]
        for adjacent_edge in adjacent_edges:
            operator, operand = adjacent_edge
            adjacent_node = operator(current_node, operand)
            if adjacent_node not in visited:
                visited[adjacent_node] = visited[current_node] + 1
                queue.append(adjacent_node)
                parent[adjacent_node] = [(current_node, adjacent_edge)]
            elif visited[current_node] == visited[adjacent_node]:
                parent[adjacent_node].append((current_node, adjacent_edge))
        if current_node == target:
            print(f"Op count is {visited[current_node]}")
            found = True
    path = []
    last_node = target
    while parent.get(target) != None:
        print(path)
        for edge in path[-1]:
            operator, operand = edge
            path.append(parent[path[-1]])
    
    path.reverse()
    found_solutions.append(path)        
    print(visited)
    return parent

def parsed_solution(raw_solution):
    return str(raw_solution)



if __name__ == "__main__":
    number = 6
    print(f"How to make {number} in minimal numbers")
    allowed_numbers = list(range(1, 6))
    print(f"Allowed to use {allowed_numbers}")
    print(parsed_solution(minimal_solutions(number, allowed_numbers)))
