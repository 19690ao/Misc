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
        self.nearest_a = defaultdict(lambda: None)
        self.nearest_b = defaultdict(lambda: None)

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

    def generate_points(self, is_random):
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
            args = Vector.coordinate_array
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
            raise TypeError(f"Unsupported operand type for +: 'Vector' and '{type(other).__name__}'")
            
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

    def __repr__(self):
        return f"Vector{self.get_dimensions()}({','.join([str(item) for item in self.coordinate_array])})"

    def copy(self):
        return Vector(self)

    def distance_from_origin(self) -> float:
        return math.sqrt(sum([dimension**2 for dimension in self.coordinate_array]))

if __name__ == "__main__":
    PairLocations.print_running_file_name()

    program = PairLocations()

    program.generate_points(False)

    print(program.points_a, program.points_b)

    print([item.distance_from_origin() for item in program.points_a])

    print(Vector((1,2)) == Vector((1,2)))