import functools
import heapq
import math
import time

MAX_INT = 2147483647
MIN_INT = -2147483648

def operate(symbol, a, b):
    assert a > 0 and b > 0
    assert a==a//1 and b==b//1
    match symbol:
        case '+':
            return min(MAX_INT, a+b)
        case '*':
            return min(MAX_INT, a*b)
        case '-':
            if a <= b:
                return a
            return min(MAX_INT, a-b)
        case '/':
            if b == 0:
                return a
            if a % b != 0:
                return a
            return min(MAX_INT, a // b)
        case '^':
            return min(MAX_INT, a**b)
        case _:
            return None

def invert(symbol, b, c):
    # func is the operation used to get from b to a
    # a is the target side
    # b is the operand used to get to a
    # returns the value a such that func(a, b)=c
    # if a doesn't have exactly one whole number solution, return c
    
    # Getting from a to MAX_INT using b might me hard
    assert c <= MAX_INT
    assert b > 0 and c > 0
    assert b==b//1 and c==c//1
    match symbol:
        case '+':
            if c<b:
                return c
            if c-b>MAX_INT:
                return c
            return c - b
        case '*':
            # If a*b=c, a=c//b IFF b!=0 and c%b=0
            # If b==0, then a*0=c, so c==0
            # If c%b!=0, then a is not an integer
            if b!=0 and c%b==0:
                if c//b>MAX_INT:
                    return c
                return c // b
            # c is prime
            return c
        case '-':
            # If a-b=c, c+b=a IFF c+b>0
            if c+b>MAX_INT:
                return c
            return c + b
        case '/':
            # When b=0, c=a
            # Otherwise, if a%b!=0, c=a
            # Else, a//b=c, so a=b*c IFF a%b==0
            # That'd mean (b*c)%b==0, which is True since c//1=c
            if c*b>MAX_INT:
                return c
            return c * b
        case '^':
            # If a**b==c, c^(1/b)
            a_guess = round(c ** (1/b))
            if a_guess**b==c:
                if a_guess>MAX_INT:
                    return c
                return a_guess
            # c is not a perfect power
            return c
        case _:
            return None

def minimal_solution(target, using):
    using = set(using)
    if target in using:
        return [(target, (None, target))]
    operator_symbols = {'+', '*', '-', '/', '^'}
    
    counter = 1
    path_score = functools.cmp_to_key(path_cmp)
    def queue_input(path, cost, counter=0):
        number = path[-1][0]
        return ((cost, abs(target - number), path_score(path), counter), path)

    def queue_input_back(path, cost, counter=0):
        # TODO: Put a heuristic in here between counter and cost
        # min_using = min(using)
        # max_using =
        # abs(target - number)
        return ((cost, counter), path)

    queue = [queue_input([(number, (None, number))], 1) for number in using]
    heapq.heapify(queue)

    queue_back = [queue_input_back([(target, None)], 0)]
    heapq.heapify(queue_back)
    # print(queue)

    visited = dict([(number, 1) for number in using])
    visited_back = dict([(target, 0)])    

    start_paths = []
    end_dict = {target: [[(target, None)]]}

    end_paths = []
    start_dict = dict([(number,[[number, (None, number)]]) for number in using])

    # while not done
    while queue or queue_back:
        # Get area around the start until next length
        new_queue = []
        heapq.heapify(new_queue)
        while queue:
            score, path = heapq.heappop(queue)
            cost, _, _, _ = score
            node, _ = path[-1]
            if node in visited_back:
                start_paths.append(path)
            else:
                edges = [(operator, operand) for operator in operator_symbols for operand in using]
                
                for edge in edges:
                    operator, operand = edge
                    neighbor = operate(operator, node, operand)
                    if neighbor in {node, operand} or neighbor in using:
                        continue
                    new_cost = cost+1
                    if neighbor in visited and visited[neighbor] < new_cost:
                        continue
                    new_path = path.copy()
                    new_path.append((neighbor, edge))
                    new_input = queue_input(new_path, new_cost, counter)
                    
                    if neighbor not in start_dict:
                        start_dict[neighbor] = []
                    start_dict[neighbor].append(new_path)
                    heapq.heappush(new_queue, new_input)
                    visited[neighbor] = new_cost
                    counter += 1
        queue = new_queue
        # If found, stop, mark
        if start_paths != []:
            # Do the return here
            found_path = None
            best_score = None
            for start_path in start_paths:
                middle = start_path[-1][0]
                assert middle in end_dict
                # print(middle)
                # print(end_dict[middle])
                for reversed_end_path in end_dict[middle]:
                    end_path = list(reversed(reversed_end_path))
                    total_path = start_path+end_path[1:]
                    current_score = path_score(total_path)
                    if best_score is None or best_score > current_score:
                        found_path = total_path
                        best_score = current_score
            # print("Bing")
            return found_path
        # end_dict = dict()
        # Get area around the end until next length
        new_queue_back = []
        heapq.heapify(new_queue_back)
        while queue_back:
            score, path = heapq.heappop(queue_back)
            cost, _ = score
            node, _ = path[-1]
            if node == MAX_INT:
                print("MAX_INT Reached!")
            if node in visited:
                end_paths.append(path)
            else:
                edges = [(operator, operand) for operator in operator_symbols for operand in using]
                
                for edge in edges:
                    operator, operand = edge
                    neighbor = invert(operator, operand, node)
                    if neighbor in {node, operand}:
                        continue
                    new_cost = cost+1
                    if neighbor in visited_back and visited_back[neighbor] < new_cost:
                        continue
                    new_path = path.copy()
                    # This is gonna be weird
                    new_path[-1] = (node, edge)
                    new_path.append((neighbor, None))
                    new_input = queue_input_back(new_path, new_cost, counter)
                    
                    if neighbor not in end_dict:
                        end_dict[neighbor] = []
                    end_dict[neighbor].append(new_path)
                    heapq.heappush(new_queue_back, new_input)
                    visited_back[neighbor] = new_cost
                    counter += 1
        queue_back = new_queue_back
        # If found, stop, mark
        if end_paths != []:
            # Do the return here
            found_path = None
            best_score = None
            # print(start_dict)
            for reversed_end_path in end_paths:
                end_path = list(reversed(reversed_end_path))
                # print(end_path)
                middle = end_path[0][0]
                # print(f"Middle: {middle}")
                assert middle in start_dict
                for start_path in start_dict[middle]:
                    total_path = start_path+end_path[1:]
                    # print(parsed_solution(total_path))
                    current_score = path_score(total_path)
                    if best_score is None or best_score > current_score:
                        found_path = total_path
                        best_score = current_score
            # print(best_score)
            # print("Bong")
            return found_path
        # start_dict = dict()
    return None

def minimal_set_solution(target, using, belt_max):
    # print(target)
    sorted_using = sorted(using)
    using = set(using)
    if target in using:
        return [(target, (None, target))]
    operator_symbols = {'+', '*', '-', '/', '^'}
    # Consistent and admissable
    # Consistent -> h(n) <= c(n,a,n')+h(n')
    # Admissable -> h(n) <= h*(n)
    # Consistent -> Admissable
    def heuristic(number):
        return abs(target - number)
    
    counter = 1
    path_score = functools.cmp_to_key(lambda a, b: path_set_cmp(a, b, belt_max))
    def queue_input(path, counter=0):
        number = path[-1][0]
        return ((path_score(path), heuristic(number), counter), path)
    
    queue = [queue_input([(number, (None, number))]) for number in using]
    heapq.heapify(queue)
    # print(queue)

    visited = dict([(number, path_score([(number, (None, number))])) for number in using])
    max_using = sorted_using[-1]
    worst_path = [(None, (None, max_using))]*(target-len(using))+list(reversed([(None, (None, i)) for i in sorted_using]))
    worst_score = path_score(worst_path)
    while queue:
        _, path = heapq.heappop(queue)
        node, _ = path[-1]
        if node == target:
            # print(parsed_solution(path, operator_dict))
            return path
        else:
            edges = [(operator, operand) for operator in operator_symbols for operand in using]
            for edge in edges:
                operator, operand = edge
                neighbor = operate(operator, node, operand)
                if neighbor in {node, operand} or neighbor in using:
                    continue
                new_path = path.copy()
                new_path.append((neighbor, edge))
                # Might be necessary to make this faster
                # if max_occurence_in_path(new_path) > belt_max:
                #     continue
                new_cost = path_score(new_path)
                if neighbor in visited and visited[neighbor] < new_cost:
                    continue
                if new_cost > worst_score:
                    print(f"{new_path}>{worst_path}")
                    continue
                new_input = queue_input(new_path, counter)
                heapq.heappush(queue, new_input)
                visited[neighbor] = new_cost
                counter += 1
    print(f"NO PATH TO {target} FOUND")
    # This should be impossible in all cases where 1 exists
    return None

def max_occurence_in_path(path):
    occurence = occurences_in_list(numbers_in_path_list(path))
    return max(occurence.values())

def occurences_in_list(numbers):
    occurences = dict()
    for number in numbers:
        if number not in occurences:
            occurences[number] = 0
        occurences[number] += 1
    return occurences

def numbers_in_path_set(path):
    return set(numbers_in_path_list(path))

def numbers_in_path_list(path):
    return [edge[1] for _,edge in path]

def path_cmp(a, b):
    # Returns -1 if a<b, 0 if a=b, 1 if a>b
    a_list = numbers_in_path_list(a)
    b_list = numbers_in_path_list(b)
    a_len, b_len = len(a_list), len(b_list)
    if a_len != b_len:
        return int(a_len > b_len)*2-1
    
    a_numbers, b_numbers = numbers_in_path_set(a), numbers_in_path_set(b)
    a_unique, b_unique = len(a_numbers), len(b_numbers)
    if a_unique != b_unique:
        return int(a_unique > b_unique)*2-1
    
    max_a, max_b = max(a_numbers), max(b_numbers)
    if max_a != max_b:
        return int(max_a > max_b)*2-1
    sum_a, sum_b = sum(a_numbers), sum(b_numbers)
    if sum_a != sum_b:
        return int(sum_a > sum_b)*2-1
    
    if a_list != b_list:
        return int(a_list > b_list)*2-1
    return 0

def path_set_cmp(a, b, max_allowed=9):
    # Returns -1 if a<b, 0 if a=b, 1 if a>b
    occurences_a = occurences_in_list(numbers_in_path_list(a))
    sources_a = sum([math.ceil(value/max_allowed) for value in occurences_a.values()])
    occurences_b = occurences_in_list(numbers_in_path_list(b))
    sources_b = sum([math.ceil(value/max_allowed) for value in occurences_b.values()])
    if sources_a != sources_b:
        return int(sources_a > sources_b)*2-1
    return path_cmp(a, b)

def parsed_solution(raw_solution):
    if raw_solution is None:
        return ''
    # print(raw_solution)
    ans = str(raw_solution[0][0])
    if len(raw_solution) <= 1:
        return ans
    # print(list(raw_solution))
    for _, edge in raw_solution[1:-1]:
        operator, operand = edge
        ans = f"({ans}{operator}{operand})"
    last_edge = raw_solution[-1][1]
    operator, operand = last_edge
    ans = f"{ans}{operator}{operand}"

    return ans

def test_div(allowed_numbers, last):
    for i in range(1, last+1):
        solution = minimal_solution(i, allowed_numbers)
        parsed = parsed_solution(solution)
        if '/' in parsed:
            print(f"{i}={parsed}")

def score_tests():
    path_score = functools.cmp_to_key(path_cmp)

    path_a = [(1, (None, 1))]
    path_b = [(1, (None, 1)), (1, ('*', 1))]
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (6, ("*", 3))]
    path_b = [(2, (None, 1)), (6, ("+", 4))]
    assert path_score(path_a) < path_score(path_b)

    path_a = [(5, (None, 5)), (25, ('*', 5))]
    path_b = [(17, (None, 17)), (25, ('+', 8))]
    assert path_score(path_a) < path_score(path_b)

    path_a = [(9, (None, 9)), (18, ('+', 9))]
    path_b = [(3, (None, 3)), (18, ('*', 6))]
    assert path_score(path_a) < path_score(path_b)

def test_1():
    allowed_numbers = [1]
    number = 4
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) == "((1+1)+1)+1"
    number = 5
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) == "(((1+1)+1)+1)+1"

    allowed_numbers = [1, 2]
    number = 4
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) in {"2+2", "2*2", "2^2"}

    allowed_numbers = [1, 2, 3]
    number = 27
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) == "3^3"

def test_2():
    allowed_numbers = [3, 6, 9]
    number = 18
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) == "9+9"

def test_3():
    allowed_numbers = [5, 8, 17]
    number = 25
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) == "5*5"


    allowed_numbers = [1, 2, 3, 4, 5, 8, 17, 31]
    number = 69273666
    result = minimal_solution(number, allowed_numbers)
    assert parsed_solution(result) == "((31^31)-1)/31"

def test_set_1():
    allowed_numbers = [1, 2]
    number = 5
    result = minimal_set_solution(number, allowed_numbers, 2)
    assert result != None
    # print(parsed_solution(result))
    assert parsed_solution(result) in {"(1+2)+2", "(2+1)+2", "(2+2)+1", "(2*2)+1", "(2^2)+1"}

def run_tests():
    score_tests()
    test_1()
    test_2()
    test_3()

    test_set_1()

def sort_by_difficulty(numbers, allowed_numbers):    
    path_score = functools.cmp_to_key(path_cmp)
    paths = [minimal_solution(number, allowed_numbers) for number in numbers]
    numbers_paths = zip(numbers, paths)
    scores = [path_score(path) for path in paths]

    sorting_list = sorted(zip(numbers_paths, scores), key=lambda x:x[1])
    for (number, path), _ in sorting_list:
        print()
        print(number)
        print(parsed_solution(path))
        
    return sorting_list

def sort_by_set_difficulty(numbers, allowed_numbers, belt_max):
    path_score = functools.cmp_to_key(lambda a, b: path_set_cmp(a, b, belt_max))
    paths = [minimal_set_solution(number, allowed_numbers, belt_max) for number in numbers]
    numbers_paths = zip(numbers, paths)
    scores = [path_score(path) for path in paths]
    print(paths)
    sorting_list = sorted(zip(numbers_paths, scores), key=lambda x:x[1])
    for (number, path), _ in sorting_list:
        print()
        print(number)
        print(parsed_solution(path))
    print([parsed_solution(path) for path in paths])
    print([number for (number, _), _ in sorting_list])
    return sorting_list

def main(allowed_numbers, belt_max):
    user_input = ""
    while not user_input.isdigit():
        user_input = input("Please enter an integer >> ").strip()
    number = int(user_input)
    print(f"How to make {number} in minimal numbers")
    # allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    # allowed_numbers = [1, 2]
    print(f"Allowed to use {allowed_numbers}")
    # test_div(allowed_numbers)
    # solution = minimal_solution(number, allowed_numbers)
    t0 = time.time()
    solution = minimal_set_solution(number, allowed_numbers, belt_max)
    t1 = time.time()
    print(f"Calculation took {round(t1-t0, 3)} seconds")
    if solution != None:
        print(f"Solution found")
        print(parsed_solution(solution))

if __name__ == "__main__":
    nonexistent = {10}
    max_num = 37
    max_num = 2
    # If your belt_max is too high, this will take ages (ex. 1+1+1+1+1...)
    belt_max = float('inf')
    allowed_numbers = [i+1 for i in range(0, max_num) if i+1 not in nonexistent]
    numbers = [79312, 12279, 11058, 3988839]
    numbers = [i+1 for i in range(0, 100) if i+1 not in allowed_numbers]
    print(numbers, allowed_numbers)
    run_tests()
    # main(allowed_numbers, belt_max)
    # sort_by_difficulty(numbers, allowed_numbers)
    sort_by_set_difficulty(numbers, allowed_numbers, belt_max)
    # test_div(allowed_numbers, 2000)
