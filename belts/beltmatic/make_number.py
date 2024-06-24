def add(a, b):
    return a+b

def mult(a, b):
    return a*b

def sub(a, b):
    return a-b

def div(a, b):
    if b == 0:
        return a
    if a % b != 0:
        return a
    return a // b

def divall(a, b):
    d, r = 0, 0
    if b == 0:
        d, r = 0, a
    elif a % b != 0:
        d, r = a // b, a % b
    else:
        print(a, b)
        assert False
    return d, r

def divadd(a, b):
    d, r = divall(a, b)
    
    return add(a, b)

def divmult(a, b):
    d, r = divall(a, b)
    return mult(a, b)

def divsub(a, b):
    d, r = divall(a, b)
    return sub(a, b)

def divsubi(a, b):
    d, r = divall(a, b)
    return sub(r, d)

def minimal_solutions(target, using):
    if target in using:
        return [str(target)]
    main_operator_dict = {add: '+', mult: '*', sub: '-', div: '/'}
    
    div_dict = {divadd: '/+', divmult: '/*', divsub: '/-', divsubi: '/i-'}
    operator_dict = {**main_operator_dict, **div_dict} 
    found_solutions = []
    queue = [[(number, (None, None))] for number in using]
    visited = dict([(number, 1) for number in using])
    while queue:
        path = queue.pop(0)
        node, _ = path[-1]
        if target in visited and visited[target] < len(path):
            break
        if node in visited and visited[node] < len(path):
            break
        if node == target:
            found_solutions.append(path) 
        else:
            edges = [(operator, operand) for operator in main_operator_dict.keys() for operand in using]
            edges += [(operator, operand) for operator in div_dict.keys() for operand in using if (operand == 0 or node % operand != 0)]
            for edge in edges:
                operator, operand = edge
                neighbour = operator(node, operand)
                if neighbour in visited and visited[neighbour] < len(path)+1:
                    continue
                new_path = path.copy()
                new_path.append((neighbour, edge))
                queue.append(new_path)
                visited[neighbour] = visited[node] + 1
    found_solutions.sort(key=path_score)
    found_solutions = [parsed_solution(solution, operator_dict) for solution in found_solutions]
    return found_solutions

def path_score(path):
    return len(set([path[0][0]]+[edge[1] for _,edge in path[1:]]))

def parsed_solution(raw_solution, operator_dict):
    ans = str(raw_solution[0][0])
    if len(raw_solution) <= 1:
        return ans
    for _, edge in raw_solution[1:-1]:
        operator, operand = edge
        ans = f"({ans}{operator_dict[operator]}{operand})"
    last_edge = raw_solution[-1][1]
    operator, operand = last_edge
    ans = f"{ans}{operator_dict[operator]}{operand}"

    return ans

if __name__ == "__main__":
    user_input = ""
    while not user_input.isdigit():
        user_input = input("Please enter an integer >> ").strip()
    number = int(user_input)
    print(f"How to make {number} in minimal numbers")
    allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
    print(f"Allowed to use {allowed_numbers}")
    solutions = minimal_solutions(number, allowed_numbers)
    print(f"{len(solutions)} solutions found")
    print(solutions)
