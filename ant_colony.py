import math
import random

#food --> cidades

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D list): Square matrix of distances. Diagonal is assumed to be math.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iterations (int): Number of iterations
            decay (float): Pheromone decay rate. 0.95 means slow decay, 0.5 faster decay.
            alpha (float): Weight of pheromone, higher alpha emphasizes pheromone. Default=1
            beta (float): Weight of distance, higher beta emphasizes distance. Default=1
        """
        self.distances = distances
        self.pheromone = [[1 / len(distances) for _ in row] for row in distances]
        self.all_inds = list(range(len(distances)))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = (None, math.inf)
        
        for _ in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromone(all_paths, self.n_best)
            shortest_path = min(all_paths, key=lambda x: x[1])

            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path

            # Apply pheromone decay
            self.pheromone = [[p * self.decay for p in row] for row in self.pheromone]

        return all_time_shortest_path

    def spread_pheromone(self, all_paths, n_best):
        # Deposit pheromone on the best paths
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move[0]][move[1]] += 1.0 / dist

    def gen_path_dist(self, path):
        # Calculate total distance of a path
        return sum(self.distances[move[0]][move[1]] for move in path)

    def gen_all_paths(self):
        # Generate all paths for this iteration
        all_paths = []
        for _ in range(self.n_ants):
            path = self.gen_path(0)
            total_dist = self.gen_path_dist(path)
            all_paths.append((path, total_dist))
        return all_paths

    def gen_path(self, start):
        # Generate a path starting from a given node
        path = []
        visited = {start}
        prev = start

        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            visited.add(move)
            prev = move

        path.append((prev, start))  # Return to the starting node
        return path

    def pick_move(self, pheromone, dist, visited):
        # Choose the next move based on pheromone and distance
        pheromone = [p if i not in visited else 0 for i, p in enumerate(pheromone)]
        weights = [(p ** self.alpha) * ((1 / d) ** self.beta) if d != 0 else 0
                    for p, d in zip(pheromone, dist)]
        
        total = sum(weights)
        if total == 0:
            return random.choice([i for i in self.all_inds if i not in visited])

        probabilities = [w / total for w in weights]
        return random.choices(self.all_inds, probabilities)[0]

if __name__ == '__main__':
    distances = [
        [math.inf, 2, 2, 5, 7],
        [2, math.inf, 4, 8, 2],
        [2, 4, math.inf, 1, 3],
        [5, 8, 1, math.inf, 2],
        [7, 2, 3, 2, math.inf]
    ]

    ant_colony = AntColony(distances, n_ants=1, n_best=1, n_iterations=100, decay=0.95, alpha=1, beta=1)
    shortest_path = ant_colony.run()
    print(f"Shortest path: {shortest_path}")
