import math
import os
import random
from abc import ABC, abstractmethod
from collections import defaultdict

class PairLocations:
    """
    A class to get the name of the file that is currently running the code.
    """
    def __init__(self) -> None:
        self.points_a = None
        self.points_b = None
        self.distances = dict()
        self.nearest_a = []
        self.nearest_b = []
        self.pairs = []

    @staticmethod
    def get_current_file_name() -> str:
        """
        Returns the name of the file that is currently running the code.
        
        Returns:
        str: The name of the current file.
        """
        # Check if the code is being run in a script or an interactive session
        if __file__:
            # Get the full path of the current file
            current_file_path = __file__
        else:
            # If the code is being run interactively, return a default message
            return "The code is being run interactively."
        
        # Extract the filename from the full path
        current_file_name = os.path.basename(current_file_path)
        
        return current_file_name

    @staticmethod
    def print_running_file_name() -> None:
        print(f"Running '{PairLocations.get_current_file_name()}'")

    def generate_vectors(self, is_random):
        list1, list2 = [], []
        if is_random:
            list1_length = random.randint(1, 100)
            list2_length = random.randint(1, 100)
            
            list1 = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(list1_length)]
            list2 = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(list2_length)]

        else:
            list1 = [(1,2), (4,2), (-2.5, -9), (-4,4), (5,-5)]
            list2 = [(1, 1), (2, 1), (1, 2), (4, -2), (-2,-7), (9,-5), (-2,-3), (-1,-1), (9,1), (-9,1)]
        self.points_a = [Vector(item) for item in list1]
        self.points_b = [Vector(item) for item in list2]

    def calculate_distances(self):
        for i,coord_a in enumerate(self.points_a):
            for j,coord_b in enumerate(self.points_b):
                self.distances[(i,j)] = coord_a.distance_to(coord_b)

    def calculate_nearest(self):
        for i,_ in enumerate(self.points_a):
            nearest_distance = float("inf")
            nearest = -1
            for j,_ in enumerate(self.points_b):
                current_distance = self.distances[(i,j)]
                if current_distance < nearest_distance:
                    nearest_distance = current_distance
                    nearest = j
            self.nearest_a.append(nearest)
        
        for j,_ in enumerate(self.points_b):
            nearest_distance = float("inf")
            nearest = -1
            for i,_ in enumerate(self.points_a):
                current_distance = self.distances[(i,j)]
                if current_distance < nearest_distance:
                    nearest_distance = current_distance
                    nearest = i
            self.nearest_b.append(nearest)

    def calculate_pairs(self):
        for i,_ in enumerate(self.points_a):
            for j,_ in enumerate(self.points_b):
                if self.nearest_a[i] == j and self.nearest_b[j] == i:
                    self.pairs.append((i,j))
        self.pairs.sort(key = lambda x: self.distances[(x[0],x[1])])

    def get_pairs(self):
        assert self.points_a != None and self.points_b != None
        func_index = 3
        funcs = [self.calculate_distances, self.calculate_nearest, self.calculate_pairs]
        if len(self.distances.keys()) == 0:
            func_index = 0
        elif self.nearest_a == [] or self.nearest_b == []:
            func_index = 1
        elif self.pairs == []:
            func_index = 2
        for i in range(func_index, 3):
            funcs[i]()
        return [(self.points_a[a].copy(), self.points_b[b].copy()) for a,b in self.pairs]

class Coordinates(ABC):
    @abstractmethod
    def __add__(self, other):
        pass
    
    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass
    
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def distance_from_origin(self) -> float:
        pass

class Vector(Coordinates):
    def __init__(self, args):
        if isinstance(args, Vector):
            args = args.coordinate_array
        self.coordinate_array = args
        self.coordinate_array = self.get_coordinate_array()
    
    def get_dimensions(self) -> int:
        return len(self.coordinate_array)
    
    def get_coordinate_array(self):
        return [item.copy() if hasattr(item, "copy") else item for item in self.coordinate_array]

    def __add__(self, other):
        if isinstance(other, Vector):
            vec_a = self
            dim_a = self.get_dimensions()
            vec_b = other
            dim_b = other.get_dimensions()
            
            if dim_a>dim_b:
                return other + self   
            # dim_a<=dim_b
            new_vector = Vector(vec_a)
            for index, coord in enumerate(vec_b.coordinate_array):
                new_vector.coordinate_array[index] += coord
            return new_vector
        else:
            raise TypeError(f"Unsupported operand type for +: 'Vector' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other, Vector):
            vec_a = self
            dim_a = self.get_dimensions()
            vec_b = other
            dim_b = other.get_dimensions()
            
            if dim_a>dim_b:
                return -1*(other - self)   
            # dim_a<=dim_b
            new_vector = Vector(vec_a)
            for index, coord in enumerate(vec_b.coordinate_array):
                new_vector.coordinate_array[index] -= coord
            return new_vector
        else:
            raise TypeError(f"Unsupported operand type for -: 'Vector' and '{type(other).__name__}'")
            
    def __mul__(self, other):
        if isinstance(other, Vector):
            # Cross-Multiplication
            vec_a = self
            dim_a = self.get_dimensions()
            vec_b = other
            dim_b = other.get_dimensions()
            
            if dim_a>dim_b:
                return other * self   
            # dim_a<=dim_b
            new_vector = Vector(vec_a)
            for index, coord in enumerate(vec_b.coordinate_array):
                new_vector.coordinate_array[index] *= coord
            return new_vector
        else:
            # Scalar-Multiplication
            new_vector = Vector(self)
            for index, coord in enumerate(self.coordinate_array):
                new_vector.coordinate_array[index] *= other
            return new_vector

    def __eq__(self, other):
        return isinstance(other, Vector) and self.coordinate_array == other.coordinate_array

    def __repr__(self):
        return f"Vector{self.get_dimensions()}({','.join([str(item) for item in self.coordinate_array])})"

    def copy(self):
        return Vector(self)

    def distance_from_origin(self) -> float:
        return math.sqrt(sum([dimension**2 for dimension in self.coordinate_array]))

    def distance_to(self, other):
        assert isinstance(other, Vector)
        return abs((self - other).distance_from_origin())
    
class PolarVector(Coordinates):
    def __init__(self, args):
        self.r = args[0]
        self.r = self.get_radius()
        self.angle_array = [math.radians(angle) for angle in args[1:]]
    
    def get_dimensions(self) -> int:
        return 1 + len(self.angle_array)
    
    def get_coordinate_array(self):
        return [self.get_radius()]+self.get_angle_array()
    
    def get_radius(self):
        if hasattr(self.r, "copy"):
            return self.r.copy()
        return self.r
    
    def get_angle_array(self):
        return [math.degrees(radians) for radians in self.get_radians_array()]
    
    def get_radians_array(self):
        return [item.copy() if hasattr(item, "copy") else item for item in self.angle_array]
    
    def __add__(self, other):
        if isinstance(other, PolarVector):
            # Addition in polar coordinates involves converting to Cartesian, adding, and converting back
            vec_a = self.to_cartesian()
            vec_b = other.to_cartesian()
            new_vector = vec_a + vec_b
            return PolarVector.from_cartesian(new_vector)
        else:
            raise TypeError(f"Unsupported operand type for +: 'PolarVector' and '{type(other).__name__}'")
    
    def __sub__(self, other):
        if isinstance(other, PolarVector):
            # Subtraction in polar coordinates involves converting to Cartesian, subtracting, and converting back
            vec_a = self.to_cartesian()
            vec_b = other.to_cartesian()
            new_vector = vec_a - vec_b
            return PolarVector.from_cartesian(new_vector)
        else:
            raise TypeError(f"Unsupported operand type for -: 'PolarVector' and '{type(other).__name__}'")
    
    def __mul__(self, other):
        if isinstance(other, PolarVector):
            # Multiplication in polar coordinates involves converting to Cartesian, multiplying, and converting back
            vec_a = self.to_cartesian()
            vec_b = other.to_cartesian()
            new_vector = vec_a * vec_b
            return PolarVector.from_cartesian(new_vector)
        else:
            # Scalar multiplication
            new_vector = PolarVector(self.r * other, self.theta)
            return new_vector
    
    def __eq__(self, other):
        return isinstance(other, PolarVector) and self.r == other.r and self.theta == other.theta
    
    def __repr__(self):
        return f"PolarVector(r={self.r}, theta={self.theta})"
    
    def copy(self):
        return PolarVector(self.r, self.theta)
    
    def distance_from_origin(self) -> float:
        return self.r
    
    def distance_to(self, other):
        assert isinstance(other, PolarVector)
        return abs(self.distance_from_origin() - other.distance_from_origin())
    
    @staticmethod
    def from_cartesian(cartesian_vector):
        r = math.sqrt(cartesian_vector[0]**2 + cartesian_vector[1]**2)
        theta = math.atan2(cartesian_vector[1], cartesian_vector[0])
        return PolarVector(r, theta)
    
    def to_cartesian(self):
        x = self.r * math.cos(self.theta)
        y = self.r * math.sin(self.theta)
        return Vector([x, y])
    
if __name__ == "__main__":
    PairLocations.print_running_file_name()

    program = PairLocations()

    program.generate_vectors(True)
    
    program.get_pairs()

    print(program.points_a, program.points_b)

    print([item.distance_from_origin() for item in program.points_a])

    print(program.distances)

    print(program.nearest_a)

    print(program.nearest_b)

    print(program.pairs)

    print(program.get_pairs())