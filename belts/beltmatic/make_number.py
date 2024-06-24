def add(a, b):
    return a+b

def mult(a, b):
    return a*b

def sub(a, b):
    return a-b

def minimal_solutions(target, using):
    if target in using:
        return [str(target)]
    operator_dict = {add: '+', mult: '*', sub: '-'}
    found_solutions = []
    queue = [[(number, (None, None))] for number in using]
    visited = dict([(number, 1) for number in using])
    while queue:
        path = queue.pop(0)
        # print(f"{parsed_solution(path, operator_dict)}")
        node, _ = path[-1]
        # input()
        if target in visited and visited[target] < len(path):
            break
        if node in visited and visited[node] < len(path):
            break
        if node == target:
            if node in visited and visited[node] < len(path):
                break
            found_solutions.append(parsed_solution(path, operator_dict))
            # input(f"FOUND: {path}")   
        else:
            edges = [(operator, operand) for operator in operator_dict.keys() for operand in using]
            for edge in edges:
                operator, operand = edge
                # print(edge, node)
                neighbour = operator(node, operand)
                if neighbour in visited and visited[neighbour] < len(path)+1:
                    continue
                new_path = path.copy()
                new_path.append((neighbour, edge))
                queue.append(new_path)
                visited[neighbour] = visited[node] + 1
                # print(visited[node], path)
            # assert visited[node] == len(path)

    return found_solutions

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
    allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    # allowed_numbers = [1, 2]
    print(f"Allowed to use {allowed_numbers}")
    solutions = minimal_solutions(number, allowed_numbers)
    print(f"{len(solutions)} solutions found")
    print(minimal_solutions(number, allowed_numbers))
