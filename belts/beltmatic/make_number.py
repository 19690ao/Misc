import functools
import heapq

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

def exp(a, b):
    return a**b

def minimal_solution(target, using):
    if target in using:
        return str(target)
    operator_dict = {add: '+', mult: '*', sub: '-', div: '/', exp: '^'}

    def heuristic(number):
        return abs(target - number)

    path_score = functools.cmp_to_key(path_cmp)
    queue = [(0, heuristic(number), path_score([(number, (None, number))]), 0, [(number, (None, number))]) for number in using]
    heapq.heapify(queue)
    # print(queue)
    counter = 1
    visited = dict([(number, 1) for number in using])
    while queue:
        operation_count, _, _,  _, path = heapq.heappop(queue)
        node, _ = path[-1]
        if node != target and target in visited and visited[target] < len(path):
            break
        if node in visited and visited[node] < len(path):
            break
        if node == target:
            return parsed_solution(path, operator_dict)
        else:
            edges = [(operator, operand) for operator in operator_dict.keys() for operand in using]
            neighbours = set()
            for edge in edges:
                operator, operand = edge
                neighbour = operator(node, operand)
                if neighbour in {node, operand}:
                    continue
                if neighbour in visited and visited[neighbour] < len(path)+1:
                    continue
                new_path = path.copy()
                new_path.append((neighbour, edge))
                heapq.heappush(queue, (operation_count+1, heuristic(neighbour), path_score(new_path), counter, new_path))
                counter += 1
                visited[neighbour] = visited[node] + 1
                neighbours.add(neighbour)
    return None

def numbers_in_path(path):
    return set([edge[1] for _,edge in path])

def path_cmp(a, b):
    # Returns -1 if a<b, 0 if a=b, 1 if a>b\
    a_numbers, b_numbers = numbers_in_path(a), numbers_in_path(b)
    a_unique, b_unique = len(a_numbers), len(a_numbers)
    if a_unique != b_unique:
        return int(a_unique > b_unique)*2-1
    
    max_a, max_b = max(a_numbers), max(b_numbers)
    if max_a != max_b:
        return int(max_a > max_b)*2-1
    sum_a, sum_b = sum(a_numbers), sum(b_numbers)
    if sum_a != sum_b:
        return int(sum_a > sum_b)*2-1
    a_str, b_str = str(a), str(b)
    if a_str != b_str:
        return int(a_str > b_str)*2-1
    return 0

def parsed_solution(raw_solution, operator_dict):
    if raw_solution == None:
        return ''
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
    allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15]
    # allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"Allowed to use {allowed_numbers}")
    solution = minimal_solution(number, allowed_numbers)
    if solution != None:
        print(f"Solution found")
        print(solution)
