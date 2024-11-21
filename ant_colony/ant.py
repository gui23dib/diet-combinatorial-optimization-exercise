import random

class AntClass:
    def __init__(self, starting_point: int, tour_path: list[int] = [], visited: list[int] = []):
        self.tour_path: list[int] = tour_path or [starting_point]#caminho do tour
        self.visited: list[int] = visited or [starting_point]
        self.starting_point: int = starting_point
        self.fitness: float = 0.0

    def generate_path(max: int = 0):
        pass