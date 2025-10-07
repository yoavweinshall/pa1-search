from collections import deque
import heapq, math
from typing import Tuple, Generator, Dict, Set, List

from common import plugins
from .game import Maze

ROW_LOCATION_IN_POSITION_TUPLE = 0
COLUMN_LOCATION_IN_POSITION_TUPLE = 1
WALL_WEIGHT = float('inf')
NO_SOL_WEIGHT = float('inf')

def get_non_wall_neighbors(maze: Maze, location: Tuple[int, int]) -> Generator[Tuple[int, int]]:
    """
    wrapper to the get neighbor function that returns only the none wall neighbors
    :param maze: the maze
    :param location: the location we want its neighbors
    :return: a generator that yields the none wall neighbors
    """
    for neighbor in maze.neighbors(*location):
        if maze.get_weight(*neighbor) != WALL_WEIGHT:
            yield neighbor


def build_path_from_prev_dict(start: Tuple[int, int], goal: Tuple[int, int],
                              prev_dict: Dict[Tuple[int, int], Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    go over the prev node dict to extract the path to solve the maze. We call this function only if we solved the maze
    :param start: starting position
    :param goal: goal position
    :param prev_dict: dictionary that for every node in the maze holds the previous node in the shortest
                      path that has been found to this node
    :return: the path from start to goal
    """
    path = [goal, ]
    node = goal
    while node != start:
        node = prev_dict[node]
        path.append(node)
    path.reverse()
    return path


def bfs(maze: Maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded


def dfs(maze: Maze):
    start, goal = maze.start, maze.goal
    expanded = set()
    distances = {}
    for row in range(goal[ROW_LOCATION_IN_POSITION_TUPLE] + 1):
        for col in range(goal[COLUMN_LOCATION_IN_POSITION_TUPLE] + 1):
            distances[(row, col)] = float('inf')
    distances[start] = 0
    prev = {}
    node_stack = [start]
    expanded.add(start)
    while node_stack:
        node = node_stack.pop()
        expanded.add(node)
        for neighbor in get_non_wall_neighbors(maze, node):
            dist_to_neighbor = maze.get_weight(*neighbor) + distances[node]

            if dist_to_neighbor < distances[neighbor]:  # replace path to a better one
                distances[neighbor] = dist_to_neighbor
                prev[neighbor] = node
                # if we find a better way to a node its neighbors might be also a better way through it
                for neighbor_of_neighbor in get_non_wall_neighbors(maze, neighbor):
                    node_stack.append(neighbor_of_neighbor)

            if neighbor not in expanded:  # explor new nodes
                node_stack.append(neighbor)
    return (build_path_from_prev_dict(start, goal, prev), expanded) if goal in expanded else ([], expanded)


def dijkstra(maze: Maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    calculates manhattan distance between to cells
    :param a: position of first cell in a (row,column) tuple
    :param b: position of second cell in a (row,column) tuple
    :return: The manhattan distance between two cells defined to be |a.x - b.x| + |a.y - b.y|
    """
    return math.sqrt((a[ROW_LOCATION_IN_POSITION_TUPLE] - b[ROW_LOCATION_IN_POSITION_TUPLE]) ** 2 +
                     (a[COLUMN_LOCATION_IN_POSITION_TUPLE] - b[COLUMN_LOCATION_IN_POSITION_TUPLE]) ** 2)


def euclidean_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    calculates Euclidean distance between two cells
    :param a: position of first cell in a (row,column) tuple
    :param b: position of second cell in a (row,column) tuple
    :return: The Euclidian distance between two cells defined to be sqrt((a.x - b.x)^2 + (a.y - b.y)^2)
    """
    return (abs(a[ROW_LOCATION_IN_POSITION_TUPLE] - b[ROW_LOCATION_IN_POSITION_TUPLE]) +
            abs(a[COLUMN_LOCATION_IN_POSITION_TUPLE] - b[COLUMN_LOCATION_IN_POSITION_TUPLE]))

def a_star(maze: Maze, heuristic):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded

def gbfs(maze: Maze, heuristic):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded

# === DO NOT EDIT: Heuristic registration for GUI ===
def zero_heuristic(a, b):
    return 0
plugins.register('maze', 'zero', zero_heuristic)
plugins.register('maze', 'manhattan', manhattan_distance)
plugins.register('maze', 'euclidean', euclidean_distance)
