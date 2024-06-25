import functools
import heapq

def add(a, b):
    return a+b

def mult(a, b):
    return a*b

def sub(a, b):
    if a <= b:
        return a
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
    
    counter = 1
    path_score = functools.cmp_to_key(path_cmp)
    def queue_input(path, path_length, counter=0):
        number = path[-1][0]
        return ((path_length, heuristic(number), path_score(path), counter), path)

    
    queue = [queue_input([(number, (None, number))], 1) for number in using]
    heapq.heapify(queue)
    # print(queue)

    visited = dict([(number, 1) for number in using])
    while queue:
        score, path = heapq.heappop(queue)
        path_length, _, _, _ = score
        node, _ = path[-1]
        if node != target and target in visited and visited[target] < path_length:
            break
        if node in visited and visited[node] < path_length:
            break
        if node == target:
            # print(parsed_solution(path, operator_dict))
            return parsed_solution(path, operator_dict)
        else:
            edges = [(operator, operand) for operator in operator_dict.keys() for operand in using]
            neighbours = set()
            for edge in edges:
                operator, operand = edge
                neighbour = operator(node, operand)
                if neighbour in {node, operand}:
                    continue
                new_path_length = path_length+1
                if neighbour in visited and visited[neighbour] < new_path_length:
                    continue
                new_path = path.copy()
                new_path.append((neighbour, edge))
                new_input = queue_input(new_path, new_path_length, counter)
                if neighbour in visited and visited[neighbour] < new_path_length:
                    continue
                
                heapq.heappush(queue, new_input)
                visited[neighbour] = new_path_length
                counter += 1
                neighbours.add(neighbour)
    return None

def numbers_in_path_set(path):
    return set(numbers_in_path_list(path))

def numbers_in_path_list(path):
    return [edge[1] for _,edge in path]

def path_cmp(a, b):
    # Returns -1 if a<b, 0 if a=b, 1 if a>b
    a_numbers, b_numbers = numbers_in_path_set(a), numbers_in_path_set(b)
    a_unique, b_unique = len(a_numbers), len(a_numbers)
    if a_unique != b_unique:
        return int(a_unique > b_unique)*2-1
    
    max_a, max_b = max(a_numbers), max(b_numbers)
    if max_a != max_b:
        return int(max_a > max_b)*2-1
    sum_a, sum_b = sum(a_numbers), sum(b_numbers)
    if sum_a != sum_b:
        return int(sum_a > sum_b)*2-1
    a_list = numbers_in_path_list(a)
    b_list = numbers_in_path_list(b)
    if a_list != b_list:
        return int(a_list > b_list)*2-1
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

def test_div(allowed_numbers):
    for i in range(1, 999):
        solution = minimal_solution(i, allowed_numbers)
        if '/' in solution:
            print(f"{i}={solution}")

if __name__ == "__main__":
    user_input = ""
    while not user_input.isdigit():
        user_input = input("Please enter an integer >> ").strip()
    number = int(user_input)
    print(f"How to make {number} in minimal numbers")
    allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]
    # allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"Allowed to use {allowed_numbers}")
    # test_div(allowed_numbers)
    solution = minimal_solution(number, allowed_numbers)
    if solution != None:
        print(f"Solution found")
        print(solution)
