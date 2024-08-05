import functools
import heapq
import itertools
import math
import time
from collections import defaultdict

MAX_INT = 2147483647
MIN_INT = -2147483648

class LinkedNode:
    def __init__(self, value, parent_node=None):
        self.value = value
        self.parent_node = parent_node
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"LinkedNode({self.value})"

class ImmutableLinkedList:
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self.length = 0
        if iterable is not None:
            for value in iterable:
                new_node = LinkedNode(value)
                # print(f"new_node={new_node}")
                if self.head is None:
                    self.head = self.tail = new_node
                else:
                    new_node.parent_node = self.tail
                    self.tail = new_node
                self.length += 1

    def to_list(self):
        result = []
        current_node = self.tail
        while current_node is not None:
            result.append(current_node.value)
            current_node = current_node.parent_node
        return list(reversed(result))

    def __len__(self):
        return self.length
    
    def __getitem__(self, index):
        if isinstance(index,int):
            if index == 0:
                return self.head.value
            if index == -1:
                return self.tail.value
            assert False

    def __repr__(self):
        return f"ImmutableLinkedList({self.to_list()})"
    
    def __iter__(self):
        nodes = []
        current_node = self.tail
        while current_node is not None:
            nodes.append(current_node.value)
            current_node = current_node.parent_node
        return iter(nodes[::-1])
    
    def __lt__(self, other):
        # Check if 'other' is an instance of ImmutableLinkedList
        if not isinstance(other, ImmutableLinkedList):
            return False

        # Check if both lists have the same length
        if len(self) != len(other):
            return len(self) < len(other)

        # Compare the lists node by node
        node_self = self.head
        node_other = other.head
        while node_self is not None and node_other is not None:
            if node_self.value != node_other.value:
                return node_self.value < node_other.value
            node_self = node_self.parent_node
            node_other = node_other.parent_node

        # If we reached here, the lists are equal
        return False
    
    def __eq__(self, other):
        # Check if 'other' is an instance of ImmutableLinkedList
        if not isinstance(other, ImmutableLinkedList):
            return False

        # Check if both lists have the same length
        if len(self) != len(other):
            return False

        # Compare the lists node by node
        node_self = self.head
        node_other = other.head
        while node_self is not None and node_other is not None:
            if node_self.value != node_other.value:
                return False
            node_self = node_self.parent_node
            node_other = node_other.parent_node

        # If we reached here, the lists are equal
        return True

    
    def iter_excluding_ends(self):
        nodes = []
        current_node = self.tail
        while current_node is not None:
            nodes.append(current_node.value)
            current_node = current_node.parent_node
        return iter(nodes[-2:0:-1])

    def appended(self, value):
        copied = ImmutableLinkedList()
        copied.head = self.head
        new_node = LinkedNode(value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.parent_node = self.tail
            copied.tail = new_node
        copied.length = self.length+1
        return copied

class ExpressionPath(ImmutableLinkedList):
    def __init__(self, lst, belts_per_source=None):
        if isinstance(lst, ExpressionPath):
            self.head = lst.head
            self.tail = lst.tail
            self.length = lst.length
            self.calculated_sum = lst.calculated_sum
            self.occurences = lst.occurences
            self.calculated_sources = lst.calculated_sources
            self.belts_per_source = lst.belts_per_source
            self.calculated_max_occurence = lst.calculated_max_occurence
            self.calculated_max_operand = lst.calculated_max_operand
        else:
            super().__init__(lst)
            for item in lst:
                assert isinstance(item, tuple)
                assert len(item) == 2
            self.calculated_sum = None
            self.occurences = None
            self.calculated_sources = None
            self.belts_per_source = belts_per_source
            self.calculated_max_occurence = None
            self.calculated_max_operand = None

    
    def operand_occurences(self) -> defaultdict:
        if self.occurences is None:
            # print("Shouldn't be here often")
            self.occurences = defaultdict(lambda: 0)
            for operand in self.operand_list():
                assert isinstance(operand, int)
                self.occurences[operand] += 1
        return self.occurences

    def sources(self):
        assert self.belts_per_source != None
        if self.calculated_sources is None:
            occurences = self.operand_occurences()
            # t0 = time.time()
            self.calculated_sources = sum([math.ceil(value/self.belts_per_source) for value in occurences.values()])
            # print([math.ceil(value/belts_per_source) for value in occurences.values()])
            # print([occurences.values()])
            # print(f"{self} has {self.calculated_sources} source(s) now")
            # if len(self) > 1: assert False
            # t1 = time.time()
            # print(f"Sum took {round(t1-t0, 3)}s")
            # assert t1-t0<1
        return self.calculated_sources

    def sum(self):
        if self.calculated_sum is None:
            # print("Shouldn't be here often")
            self.calculated_sum = sum(operand*occurence_number for operand, occurence_number in self.operand_occurences().items())
        return self.calculated_sum

    # def appended(self, item):
    #     # print(self, item)
    #     operand = item[1][1]
    #     self.calculated_sum = self.sum() + operand
    #     self.occurences[operand] += 1
    #     if self.occurences[operand]%self.belts_per_source==1:
    #         self.calculated_sources += 1
    #     return super().appended(item)
    
    def appended(self, value):
        assert isinstance(value, tuple)
        assert len(value) == 2
        copied = ExpressionPath([], self.belts_per_source)
        # t0 = time.time()
        copied.head = self.head
        new_node = LinkedNode(value)
        # t1 = time.time()
        # if round(t1-t0,3)>=0.1: print(f"Step I took {round(t1-t0, 3)}s")
        if self.head is None:
            copied.head = copied.tail = new_node
        else:
            new_node.parent_node = self.tail
            copied.tail = new_node
        
        copied.length = self.length+1
        copied.calculated_sum = self.calculated_sum
        copied.calculated_sources = self.calculated_sources
        
        # t0 = time.time()
        copied.occurences = self.operand_occurences().copy()
        # t1 = time.time()
        # if round(t1-t0,3)>=0.1: print(f"Step J took {round(t1-t0, 3)}s")
        # The following is O(1)
        operand = value[1][1]
        copied.calculated_sum = self.sum() + operand
        # print(copied.occurences, operand)
        # print(copied.occurences[operand])
        copied.occurences[operand] += 1
        if copied.occurences[operand]%copied.belts_per_source==1:
            copied.calculated_sources = self.sources()+1
        copied.calculated_max_occurence = self.calculated_max_occurence
        if copied.occurences[operand] > copied.max_occurence():
            copied.calculated_max_occurence = copied.occurences[operand]
        copied.calculated_max_operand = self.max_operand()
        if copied.calculated_max_operand is None or operand > copied.calculated_max_operand:
            copied.calculated_max_operand = operand
        return copied

    def __str__(self):
        # print(self[0])
        assert isinstance(self[0], tuple)
        ans = str(self[0][0])
        if len(self) <= 1:
            return ans
        # print(list(raw_solution))
        for _, edge in self.iter_excluding_ends():
            operator, operand = edge
            ans = f"({ans}{operator}{operand})"
        last_edge = self[-1][1]
        operator, operand = last_edge
        ans = f"{ans}{operator}{operand}"
        return ans
    
    def __repr__(self):
        return str(self)

    def max_occurence(self):
        if self.calculated_max_occurence is None:
            # if self.operand_occurences().values():
            self.calculated_max_occurence = max(self.operand_occurences().values())
        return self.calculated_max_occurence

    def max_operand(self):
        if self.calculated_max_operand is None and self.head:
            self.calculated_max_operand = max(self.operand_set())
        return self.calculated_max_operand

    def operand_set(self):
        return set(self.operand_list())

    def operand_list(self):
        return [edge[1] for _,edge in self]

    def operator_list(self):
        # print(path)
        return [edge[0] for _,edge in self][1:]

class ExpressionEnd(ExpressionPath):
    def __init__(self, lst, belts_per_source, first_number):
        super().__init__(lst, belts_per_source)
        self.length = len(lst)
        self.first_number = first_number
    
    def appended(self, value, first_number):
        copied = ExpressionEnd(super().appended(value), self.belts_per_source, first_number)
        assert isinstance(copied, ExpressionEnd)
        # copied.first_number = first_number
        return copied
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        current_node = self.tail
        while current_node is not None:
            yield current_node.value
            current_node = current_node.parent_node

    def __str__(self):
        ans = str(self.first_number)
        if len(self) <= 0:
            return ans
        ordered = [i for i in iter(self)][:-1]        
        for _, edge in ordered:
            operator, operand = edge
            ans = f"({ans}{operator}{operand})"
        last_node, last_edge = self[0]
        operator, operand = last_edge
        ans = f"{ans}{operator}{operand}={last_node}"
        return ans
    def operator_list(self):
        # print(path)
        return [edge[0] for _,edge in self]

class ExpressionJoined():
    def __init__(self, start_path: ExpressionPath, end_path: ExpressionEnd):
        self.start_path = start_path
        self.end_path = end_path

    def to_path(self):
        copied = self.start_path
        for i in self.end_path:
            copied = copied.appended(i)
        return copied
    
    def __iter__(self):
        return iter([i for i in self.start_path]+[i for i in self.end_path])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.to_path())

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

def minimal_solution(target: int, using: list) -> ExpressionPath:
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
            return ExpressionPath(found_path)
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
                    # print(str(total_path))
                    current_score = path_score(total_path)
                    if best_score is None or best_score > current_score:
                        found_path = total_path
                        best_score = current_score
            # print(best_score)
            # print("Bong")
            return ExpressionPath(found_path)
        # start_dict = dict()
    print(f"NO PATH TO {target} FOUND")
    return None

def minimal_set_solution(target, using, belts_per_source):
    print(f"Finding {target}")
    sorted_using = sorted(using)
    min_using = sorted_using[0]
    assert min_using >= 1
    max_using = sorted_using[-1]
    using = set(using)
    # if target in using:
    #     return [(target, (None, target))]
    operator_symbols = ['+', '*', '-', '/', '^']
    # Consistent and admissable
    # Consistent -> h(n) <= c(n,a,n')+h(n')
    # Admissable -> h(n) <= h*(n)
    # Consistent -> Admissable
    def heuristic(path: ExpressionPath) -> int:
        # You can treat this as "best case" for finishing a problem
        # node, (old_operator, old_operand) = path[-1]
        return path.sources(), len(path), path_score(path)
        # return path.sources()+minimum_sources_from_target, len(path), path.max_operand(), path_score(path)# , abs(target-node)
    # The cost can be sources
    # h*(n) is the amount of sources it would actually take to get to n
    # h(n) <= the true amount of sources required, so undershoot (lower bound)
    # c(n, a, n') is the amount of added sources it took to get from n to n'
    # This can only be 0 or 1
    # If 0, h(n) <= h(n') holds true since they would have equal sources
    # If 1, h(n) < h(n') since h(n')=h(n)+1
     
    # counter = 1
    path_score = functools.cmp_to_key(path_set_cmp)
    def queue_input(path: ExpressionPath): # , counter=0):
        # number = path[-1][0]
        return (heuristic(path), path)
    def queue_input_back(path: ExpressionEnd):
        return (heuristic(path), path)
    def visit_cost(path: ExpressionPath):
        return path.sources()

    queue = [queue_input(ExpressionPath([(number, (None, number))], belts_per_source)) for number in using]
    heapq.heapify(queue)

    queue_back = [queue_input_back(ExpressionEnd([], belts_per_source, target))]
    heapq.heapify(queue_back)
    # print(queue)

    # visited = defaultdict(lambda: float('inf'), dict([((number, frozenset([number])), 1) for number in using]))
    # visited_back = defaultdict(lambda: float('inf'), dict([((target, frozenset()), 0)]))
    # visited = defaultdict(lambda: float('inf'), dict([((number, frozenset({number})), 1) for number in using]))
    visited = defaultdict(lambda: float('inf'))
    print(visited)
    visited_back = defaultdict(lambda: float('inf'), dict([((number, frozenset({})), 0) for number in {target}]))

    start_paths = []
    start_sets = defaultdict(lambda: set())
    end_dict = defaultdict(lambda: list(), {target: [ExpressionEnd([], belts_per_source, target)]})

    end_paths = []
    end_sets = defaultdict(lambda: set())
    start_dict = defaultdict(lambda: list(), dict([(number,[ExpressionPath([(number, (None, number))], belts_per_source)]) for number in using]))
    edges = [(operator, operand) for operator in operator_symbols for operand in using]
    # while not done
    while queue or queue_back:
        # Get area around the start until next length
        print(f"len(queue)={len(queue)}")
        layer = visit_cost(queue[0][1])
        print(f"layer = {layer}")
        while queue and visit_cost(queue[0][1]) == layer:
            _, path = heapq.heappop(queue)
            node, _ = path[-1]
            print(f"Here's the node from the start: {node}")
            
            worse = False
            for used_operands in all_subsets(path.operand_set()):
                used_operands = frozenset(used_operands)
                # bool([for for operand,occurence in path.operand_occurences().items()])
                if visited[(node, used_operands)] <= visit_cost(path):# or used_operands in start_sets:
                    worse = True
                    break
            if worse:
                continue
            visited[(node, frozenset(path.operand_set()))] = visit_cost(path)
            # print("It wasn't skipped")
            print(f"Here's the path for it: {str(path)}")
            found_condition = False
            for used_operands in all_subsets(path.operand_set()):
                if (node, frozenset(used_operands)) in visited_back:
                    print("Found a connection")
                    found_condition = True
                    break
            if found_condition:
                print(f"Got one, adding it: {path}")
                start_paths.append(path)
                # start_sets[frozenset(path.operand_list())].add(frozenset(path.operand_occurences().items()))
                break
            else:
                for edge in edges:
                    operator, operand = edge
                    neighbor = operate(operator, node, operand)
                    if neighbor in {node, operand} or neighbor <= 0:
                        continue
                    # new_visit_cost = cost+1
                    
                    new_path = path.appended((neighbor, edge))
                    new_visit_cost = visit_cost(new_path)
                    worse = False
                    for used_operands in all_subsets(new_path.operand_set()):
                        used_operands = frozenset(used_operands)
                        if visited[(neighbor, used_operands)] < new_visit_cost:# or used_operands in start_sets:
                            worse = True
                            break
                        # or (start_paths == [] and best_visit_cost == new_visit_cost)
                    if worse:
                        continue
                    # if I already started filling start_paths
                    # and if I can make the 
                    new_input = queue_input(new_path)
                    
                    start_dict[neighbor].append(new_path)
                    heapq.heappush(queue, new_input)
                    
        # If found, stop, mark
        if start_paths != []: # and end_paths != []:
            # Do the return here
            found_path = None
            best_score = None
            for start_path in start_paths:
                middle = start_path[-1][0]
                assert middle in end_dict
                # print(middle)
                # print(end_dict[middle])
                for end_path in end_dict[middle]:
                    assert isinstance(end_path, ExpressionEnd)
                    assert end_path.first_number == middle
                    total_path = ExpressionJoined(start_path, end_path).to_path()
                    current_score = path_score(total_path)
                    if best_score is None or best_score > current_score:
                        found_path = total_path
                        best_score = current_score
            # print("Bing")
            return found_path
        assert target not in using
        print(f"len(queue_back)={len(queue_back)}")
        layer = visit_cost(queue_back[0][1])
        print(f"layer = {layer}")
        while queue_back and visit_cost(queue_back[0][1]) == layer:
            _, path = heapq.heappop(queue_back)
            node = path.first_number
            print(f"Here's the node from the back: {node}")
            print(f"Here's the path for it: {str(path)}")
            if node == MAX_INT:
                print("MAX_INT Reached!")
            worse = False
            print(f"Full operand set: {path.operand_set()}")
            for used_operands in all_subsets(path.operand_set()):
                used_operands = frozenset(used_operands)
                if visited_back[(node, used_operands)] <= visit_cost(path) or used_operands in end_sets:
                    print(f"It looks like we can get {node} using {used_operands} in {visited_back[(node, frozenset(used_operands))]} layers, so skip")
                    worse = True
                    break
            if worse:
                continue
            print(f"It's actually better than any found method")
            visited_back[(node, frozenset(path.operand_set()))] = visit_cost(path)
            found_condition = False
            for used_operands in all_subsets(path.operand_set()):
                print(f"Have I visited {node} using {used_operands}?")
                if (node, frozenset(used_operands)) in visited:
                    print(f"We can get to {node} from the front only using {used_operands}, so we can send it")
                    found_condition = True
                    break
            if found_condition:
                end_paths.append(path)
                # end_sets[frozenset(path.operand_list())].add(frozenset(path.operand_occurences().items()))
                break
            else:
                print(f"We never found ({node}, {frozenset(used_operands)}) in there, look: {visited[(node, frozenset(used_operands))]}")
                # WHAT??? Why would we need to do that???? Don't be dumb. 
                # Visualize. Here's the back:           <-
                # We need to check the start_dict to see if there's a connection
                # The problem is, there isn't a null connection 
                # Forgot the check null operands
                
                for edge in edges:
                    operator, operand = edge
                    neighbor = invert(operator, operand, node)
                    if node in {neighbor, operand} or neighbor <= 0:
                        continue
                    # new_cost = cost+1
                    new_path = path.appended((path.first_number, edge), neighbor)
                    new_visit_cost = visit_cost(new_path)
                    worse = False
                    for used_operands in all_subsets(new_path.operand_set()):
                        used_operands = frozenset(used_operands)
                        if visited_back[(neighbor, used_operands)] < new_visit_cost or used_operands in end_sets:
                            worse = True
                            break
                    if worse:
                        continue
                    new_input = queue_input_back(new_path)
                    
                    end_dict[neighbor].append(new_path)
                    heapq.heappush(queue_back, new_input)
        # If found, stop, mark
        if end_paths != []: # and start_paths != []:
            # Do the return here
            found_path = None
            best_score = None
            # print(start_dict)
            for end_path in end_paths:
                # print(end_path)
                assert isinstance(end_path, ExpressionEnd)
                middle = end_path.first_number
                # print(f"Middle: {middle}")
                assert middle in start_dict
                for start_path in start_dict[middle]:
                    total_path = ExpressionJoined(start_path, end_path).to_path()
                    # print(str(total_path))
                    current_score = path_score(total_path)
                    if best_score is None or best_score > current_score:
                        found_path = total_path
                        best_score = current_score
            # print(best_score)
            # print("Bong")
            return found_path
        assert end_paths == []
        
        
        # end_dict = dict()
        # Get area around the end until next length
        # print(queue_back)
        # print(queue_back[0])
        # print(queue_back[0][1])
        # print(visit_cost(queue_back[0][1]))
        # assert queue_back[0]
        # assert isinstance(queue_back[0][1], ExpressionEnd)
        
        # start_dict = dict()
    print(f"NO PATH TO {target} FOUND")
    return None
    # queue = [queue_input(ExpressionPath([(number, (None, number))], belts_per_source=belts_per_source)) for number in using]
    # heapq.heapify(queue)
    # # print(queue)

    # visited = defaultdict(lambda: float('inf'))
    # worst_path = make_worst_path(target, sorted_using, belts_per_source)
    # worst_score = path_score(worst_path)
    # edges = [(operator, operand) for operator in operator_symbols for operand in using]
    # while queue:
    #     _, path = heapq.heappop(queue)
    #     node, (old_operator, old_operand) = path[-1]
    #     worse = False
    #     for used_operands in non_empty_subsets(path.operand_set()):
    #         if visited[(node, frozenset(used_operands))] <= path.sources():
    #             worse = True
    #             break
        
    #     if worse:
    #         continue
    #     visited[(node, frozenset(path.operand_set()))] = path.sources()
    #     print(f"{str(path)}={node}")
    #     # if old_operator == '/' and old_operand == 7 and node == 5: print(f"{str(path)}={node}")
    #     if node == target:
    #         # print(str(path, operator_dict))
    #         return path
    #     else:
    #         # edges_# t0 = time.time()
    #         for edge in edges:
    #             # t0 = time.time()
    #             operator, operand = edge
    #             neighbor = operate(operator, node, operand)
                
    #             # t1 = time.time()
    #             # # if round(t1-t0,3)>=0.03: print(f"Step B took {round(t1-t0, 3)}s")

    #             # t0 = time.time()
    #             if neighbor in {node, operand}:
    #                 continue
    #             if '-' in operator_symbols and \
    #                 (old_operand==operand and (old_operator, operator) in {('+', '-'), ('-', '+')}):
    #                 continue
    #             if '/' in operator_symbols and \
    #                 (old_operand==operand and (old_operator, operator) in {('*', '/'), ('/', '*')}):
    #                 continue
    #             # t1 = time.time()
    #             # # if round(t1-t0,3)>=0.03: print(f"Step C took {round(t1-t0, 3)}s")
    #             # t0 = time.time()
    #             new_length = len(path)+1
    #             if '/' in operator_symbols and new_length>neighbor+1 and operand*node<=MAX_INT :
    #                 # Making x is as easy as (n*x)/n=(n+n+n+..+n_x)/n, even with small belts_per_source
    #                 # There are x n's divided by 1 n, giving x+1 operands
    #                 continue
    #             if '^' in operator_symbols and neighbor == MAX_INT and new_length>=math.ceil(math.log(max_using, MAX_INT)):
    #                 continue
    #             new_path = path.appended((neighbor, edge))
    #             new_cost = path_score(new_path)
    #             if new_cost > worst_score:
    #                 continue
    #             new_visit_cost =  new_path.sources()
    #             # new_visit_cost = new_length                
    #             worse = False
    #             for used_operands in non_empty_subsets(new_path.operand_set()):
    #                 if visited[(neighbor, frozenset(used_operands))] < new_visit_cost:
    #                     worse = True
    #                     break
                
    #             if worse:
    #                 continue
    #             new_input = queue_input(new_path) #, counter)
    #             heapq.heappush(queue, new_input)
    #             # t1 = time.time()
    #             # if round(t1-t0,3)>=0.1: print(f"Step H took {round(t1-t0, 3)}s")
    #             # visited[neighbor] = new_visit_cost
    #             # visited[(neighbor, frozenset(new_path.operand_set()))] = new_visit_cost
                
    #             # counter += 1
                
    #         # edges_# t1 = time.time()
    #         # assert edges_t1-edges_t0 < 0.3
    # print(f"NO PATH TO {target} FOUND")
    # # This should be impossible in all cases where 1 exists
    # return worst_path

def non_empty_subsets(input_set):
    subsets = []
    for i in range(1, len(input_set) + 1):
        subsets.extend(itertools.combinations(input_set, i))
    return [set(subset) for subset in subsets]

def all_subsets(input_set):
    subsets = []
    for i in range(len(input_set) + 1):
        subsets.extend(itertools.combinations(input_set, i))
    return [set(subset) for subset in subsets]

def make_worst_path(target, sorted_list, belts_per_source):
    assert sorted_list[0] == 1
    tetration = False
    exponentiation = False
    path = None
    largest_base = -1
    power = -1
    tetration_base = -1
    height = -1
    for base in reversed(sorted_list):
        if base == 1: continue
        # print(base, target)
        potential_power = round(math.log(target, base))
        is_base = base**potential_power==target
        if is_base:
            if not exponentiation:
                largest_base = base
                power = potential_power
                exponentiation = True
            # Check tetration base
            if potential_power == 0:
                continue
            # print(f"{base}^x={potential_power}")
            potential_height = round(math.log(potential_power, base))
            # Calculate the tetration result
            tetration_result = base ** (base ** (potential_height - 1))
            if tetration_result == target:
                height = potential_height
                tetration_base = base
                break
    if height >= power:
        tetration = False
    if tetration:
        edge = ('^', tetration_base)
        path = ExpressionPath([(tetration_base**(tetration_base**(i)), edge) for i in range(height)], belts_per_source)
    elif exponentiation:
        edge = ('*', largest_base)
        path = ExpressionPath([(largest_base**(i+1), edge) for i in range(power)], belts_per_source)
        # print(f"Exp = {path}")
    else:
        divisor = next((num for num in reversed(sorted_list) if target % num == 0), 1)
        edge = ('+', divisor)
        path =  ExpressionPath([((i+1)*divisor, edge) for i in range(round(target/divisor))], belts_per_source)

    return path

def path_cmp(a, b) -> int:
    # Returns -1 if a<b, 0 if a=b, 1 if a>b
    if not isinstance(a, ExpressionPath):
        a = ExpressionPath(a)
    if not isinstance(b, ExpressionPath):
        b = ExpressionPath(b)
    a_list = a.operand_list()
    b_list = b.operand_list()
    a_len, b_len = len(a_list), len(b_list)
    if a_len != b_len:
        return int(a_len > b_len)*2-1
    
    a_numbers, b_numbers = a.operand_set(), b.operand_set()
    a_unique, b_unique = len(a_numbers), len(b_numbers)
    if a_unique != b_unique:
        return int(a_unique > b_unique)*2-1
    
    max_a, max_b = a.max_operand(), b.max_operand()
    if max_a != max_b:
        return int(max_a > max_b)*2-1
    sum_a, sum_b = sum(a_numbers), sum(b_numbers)
    if sum_a != sum_b:
        return int(sum_a > sum_b)*2-1
    
    if a_list != b_list:
        return int(a_list > b_list)*2-1
    
    operator_dict = {'':0, '+':1, '*':2, '-':3, '/':4, '^':5}
    operator_vals_a = [operator_dict[operator] for operator in a.operator_list()]
    operator_vals_b = [operator_dict[operator] for operator in b.operator_list()]

    if operator_vals_a != operator_vals_b:
        return int(operator_vals_a > operator_vals_b)*2-1
    # print(f"No difference between {a} and {b}")
    print(a, b)
    print(a.operator_list(), b.operator_list())
    assert str(a) == str(b)
    return 0

def path_set_cmp(a: ExpressionPath, b: ExpressionPath):
    # t1 = tuple([(1, (None, 1)), (2, ('+', 1)), (3, ('+', 1))])
    # t2 = tuple([(2, (None, 2)), (4, ('+', 2)), (6, ('+', 2))])
    # if (t1 in {tuple(a), tuple(b)} and t2 in {tuple(a), tuple(b)}):
    #     print("Let's see this")
    # Returns -1 if a<b, 0 if a=b, 1 if a>b
    assert isinstance(a, ExpressionPath)
    assert isinstance(b, ExpressionPath)
    sources_a = a.sources()
    sources_b = b.sources()
    if sources_a != sources_b:
        return int(sources_a > sources_b)*2-1
    # print(f"{a}.sources=={b}.sources=={sources_a}=={sources_b}")
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
        parsed = str(solution)
        if '/' in parsed:
            print(f"{i}={parsed}")

def path_test_1():
    lst = [1, 2, 3, 4, 5]
    immutable_linked_list = ImmutableLinkedList(lst)
    # print(f"{lst} vs {immutable_linked_list.to_list()}")
    assert len(immutable_linked_list) == 5
    assert lst == immutable_linked_list.to_list()

    # print(f"{lst} vs {[i for i in immutable_linked_list]}")
    assert lst == [i for i in immutable_linked_list]

    # print(f"{lst[1:-1]} vs {[i for i in immutable_linked_list.iter_excluding_ends()]}")
    assert lst[1:-1] == [i for i in immutable_linked_list.iter_excluding_ends()]

    lst.append(6)
    appended_list = immutable_linked_list.appended(6)
    # print(f"{lst} vs {[i for i in appended_list]}")
    assert lst == [i for i in appended_list]
    assert len(appended_list) == 6
    
    lst = [1,2,3,4,5]
    assert lst == immutable_linked_list.to_list()

    # print(f"{lst} vs {[i for i in immutable_linked_list]}")
    assert lst == [i for i in immutable_linked_list]

    # print(f"{lst[1:-1]} vs {[i for i in immutable_linked_list.iter_excluding_ends()]}")
    assert lst[1:-1] == [i for i in immutable_linked_list.iter_excluding_ends()]

def path_test_2():
    path_lst = [(1, (None, 1))]
    path = ExpressionPath(path_lst, 2)
    assert path.operand_occurences()[1] == 1
    
    path_lst.append((2, ('+', 1)))
    assert path.operand_occurences()[1] == 1
    path = ExpressionPath(path_lst, 2)
    assert path.operand_occurences()[1] == 2
    assert path.sources() == 1

    new_path = path.appended((3, ('+', 1)))
    assert new_path.operand_occurences()[1] == 3
    assert new_path.sources() == 2
    assert path.operand_occurences()[1] == 2
    assert path.sources() == 1

    path = ExpressionPath(path_lst, 2)
    path2 = path.appended((4, ('*', 2)))
    path_lst.append((4, ('*', 2)))
    path1 = ExpressionPath(path_lst, 2)
    assert path1 == path2


def score_tests():
    path_score = functools.cmp_to_key(path_cmp)

    path_a = [(1, (None, 1))]
    path_b = [(1, (None, 1)), (1, ('*', 1))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (6, ("*", 3))]
    path_b = [(2, (None, 1)), (6, ("+", 4))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(5, (None, 5)), (25, ('*', 5))]
    path_b = [(17, (None, 17)), (25, ('+', 8))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(9, (None, 9)), (18, ('+', 9))]
    path_b = [(3, (None, 3)), (18, ('*', 6))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (4, ('+', 2)), (6, ('+', 2))]
    path_b = [(2, (None, 2)), (4, ('+', 2)), (8, ('*', 2))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (4, ('+', 2)), (8, ('*', 2))]
    path_b = [(2, (None, 2)), (4, ('+', 2)), (16, ('^', 2))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

def score_set_tests():
    path_score = functools.cmp_to_key(path_set_cmp)

    path_a = [(1, (None, 1))]
    path_b = [(1, (None, 1)), (1, ('*', 1))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (6, ("*", 3))]
    path_b = [(2, (None, 1)), (6, ("+", 4))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(5, (None, 5)), (25, ('*', 5))]
    path_b = [(17, (None, 17)), (25, ('+', 8))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(9, (None, 9)), (18, ('+', 9))]
    path_b = [(3, (None, 3)), (18, ('*', 6))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (4, ('+', 2)), (6, ('+', 2))]
    path_b = [(2, (None, 2)), (4, ('+', 2)), (8, ('*', 2))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

    path_a = [(2, (None, 2)), (4, ('+', 2)), (8, ('*', 2))]
    path_b = [(2, (None, 2)), (4, ('+', 2)), (16, ('^', 2))]
    path_a, path_b = ExpressionPath(path_a), ExpressionPath(path_b)
    assert path_score(path_a) < path_score(path_b)

def test_1():
    allowed_numbers = [1]
    number = 4
    result = minimal_solution(number, allowed_numbers)
    assert str(result) == "((1+1)+1)+1"
    number = 5
    result = minimal_solution(number, allowed_numbers)
    assert str(result) == "(((1+1)+1)+1)+1"

    allowed_numbers = [1, 2]
    number = 4
    result = minimal_solution(number, allowed_numbers)
    assert str(result) in {"2+2", "2*2", "2^2"}

    allowed_numbers = [1, 2, 3]
    number = 27
    result = minimal_solution(number, allowed_numbers)
    assert str(result) == "3^3"

def test_2():
    allowed_numbers = [3, 6, 9]
    number = 18
    result = minimal_solution(number, allowed_numbers)
    assert str(result) == "9+9"

def test_3():
    allowed_numbers = [5, 8, 17]
    number = 25
    result = minimal_solution(number, allowed_numbers)
    assert str(result) == "5*5"


    allowed_numbers = [1, 2, 3, 4, 5, 8, 17, 31]
    number = 69273666
    result = minimal_solution(number, allowed_numbers)
    assert str(result) == "((31^31)-1)/31"

def subset_test_1():
    s = {1, 2}
    assert non_empty_subsets(s) == [{1}, {2}, {1, 2}]
    assert all_subsets(s) == [set(), {1}, {2}, {1, 2}]

def end_path_test_1():
    end_path = ExpressionEnd([], 100, 10)
    assert len(end_path) == 0
    end_path = end_path.appended((10, ('+', 1)), 9)
    assert len(end_path) == 1
    assert str(end_path) == "9+1=10"
    end_path = end_path.appended((9, ('+', 2)), 7)
    assert len(end_path) == 2
    assert str(end_path) == "(7+2)+1=10"

def test_set_1():
    allowed_numbers = [1]
    number = 1
    result = minimal_set_solution(number, allowed_numbers, 10000)
    assert str(result) == "1"

    number = 2
    result = minimal_set_solution(number, allowed_numbers, 1000)
    assert str(result) == "1+1"

    number = 4
    result = minimal_set_solution(number, allowed_numbers, 1000)
    assert str(result) == "((1+1)+1)+1"

    number = 5
    result = minimal_set_solution(number, allowed_numbers, 1000)
    assert str(result) == "(((1+1)+1)+1)+1"

    allowed_numbers = [1, 2]
    number = 4
    result = minimal_set_solution(number, allowed_numbers, 1000)
    assert str(result) in {"2+2", "2*2", "2^2"}

    allowed_numbers = [1, 2, 3]
    number = 27
    result = minimal_set_solution(number, allowed_numbers, 1000)
    assert str(result) == "3^3"

def test_set_2():
    allowed_numbers = [1, 2]
    number = 5
    result = minimal_set_solution(number, allowed_numbers, 2)
    assert result != None
    print(result)
    assert str(result) in {"(1+2)+2"}
    # assert str(result) in {"(1+2)+2", "(2+2)+1"}
    # assert str(result) in {"(1+2)+2", "(2+1)+2", "(2+2)+1", "(2*2)+1", "(2^2)+1"}

    number = 7
    result = minimal_set_solution(number, allowed_numbers, 100)
    assert result != None
    # print(result)
    print(result)
    assert str(result) in {"(((2+2)^2)-2)/2"}

    number = 3
    result = minimal_set_solution(number, allowed_numbers, 100)
    assert result != None
    # print(result)
    assert str(result) in {"(1+1)+1"}


def test_set_3():
    allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    number = 64
    result = minimal_set_solution(number, allowed_numbers, 100)
    assert result != None
    print(result)
    assert str(result) in {"8*8"}

    number = 16777216
    result = minimal_set_solution(number, allowed_numbers, 100)
    assert result != None
    print(result)
    assert str(result) in {"8^8"}

    allowed_numbers = [i+1 for i in range(20)]
    number = 57
    result = minimal_set_solution(number, allowed_numbers, 100)
    assert result != None
    print(result)
    assert str(result) in {"(19+19)+19"}

def run_tests():
    path_test_1()
    path_test_2()

    score_tests()
    test_1()
    test_2()
    test_3()

    subset_test_1()

    end_path_test_1()

    test_set_1()
    test_set_2()
    test_set_3()

    print(f"ALL CURRENT TESTS PASSED! :D")

def sort_by_difficulty(numbers, allowed_numbers):    
    path_score = functools.cmp_to_key(path_cmp)
    paths = [minimal_solution(number, allowed_numbers) for number in numbers]
    numbers_paths = zip(numbers, paths)
    scores = [path_score(path) for path in paths]

    sorting_list = sorted(zip(numbers_paths, scores), key=lambda x:x[1])
    for (number, path), _ in sorting_list:
        print()
        print(number)
        print(path)
        
    return sorting_list

def sort_by_set_difficulty(numbers, allowed_numbers, belts_per_source):
    t0 = time.time()
    path_score = functools.cmp_to_key(path_set_cmp)
    paths = [minimal_set_solution(number, allowed_numbers, belts_per_source) for number in numbers]
    numbers_paths = zip(numbers, paths)
    scores = [path_score(path) for path in paths]
    # print(paths)
    sorting_list = sorted(zip(numbers_paths, scores), key=lambda x:x[1])
    for (number, path), _ in sorting_list:
        print()
        print(number)
        print(path)
    print([(i+1,str(path)) for i,path in enumerate(paths)])
    # print([(i+1,str(path)) for i,path in enumerate(paths) if not ('*' in str(path) or '-' in str(path) or '/' in str(path) or '^' in str(path))])
    # print([i+1 for i,path in enumerate(paths) if ('*' in str(path))])
    # print([i+1 for i,path in enumerate(paths) if (len(path)==1 or '+' not in operators_in_path_list(path[2:]))])
    print([len(path) for path in paths])
    print([number for (number, _), _ in sorting_list])
    t1 = time.time()
    print(f"That took {round(t1-t0, 3)}s total for an average of {round((t1-t0)/len(paths), 3)}s")
    return sorting_list

def main(allowed_numbers, belts_per_source):
    user_input = ""
    while not user_input.isdigit():
        user_input = input("Please enter an integer >> ").strip()
    number = int(user_input)
    print(f"How to make {number} in minimal numbers")
    assert number <= MAX_INT
    # allowed_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    # allowed_numbers = [1, 2]
    print(f"Allowed to use {allowed_numbers}")
    # test_div(allowed_numbers)
    # solution = minimal_solution(number, allowed_numbers)
    t0 = time.time()
    solution = minimal_set_solution(number, allowed_numbers, belts_per_source)
    t1 = time.time()
    print(f"Calculation took {round(t1-t0, 3)} seconds")
    if solution != None:
        print(f"Solution found")
        print(str(solution))

def replace_base(lst, base) -> int:
    step = 0
    result = 0
    for number in lst:
        result += number*(base**step)
        step += 1
    return result

if __name__ == "__main__":
    nonexistent = {10}
    max_num = 39
    # max_num = 2
    # If your belts_per_source is too high, this will take ages (ex. 1+1+1+1+1...)
    belts_per_source = 9
    # belts_per_source = 100000
    allowed_numbers = [i+1 for i in range(0, max_num) if i+1 not in nonexistent]
    # allowed_numbers = [1, 9 , 29]
    numbers = [79312, 12279, 11058, 3988839]
    numbers = [i+1 for i in range(0, 104)]# if i+1 not in allowed_numbers]
    # print(numbers, allowed_numbers)
    run_tests()
    # main(allowed_numbers, belts_per_source)
    # sort_by_difficulty(numbers, allowed_numbers)
    sort_by_set_difficulty(numbers, allowed_numbers, belts_per_source)
    # test_div(allowed_numbers, 2000)
