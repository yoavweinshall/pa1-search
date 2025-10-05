from collections import deque
import heapq, math
from typing import Tuple

from common import plugins
from .game import Maze

ROW_LOCATION_IN_POSITION_TUPLE = 0
COLUMN_LOCATION_IN_POSITION_TUPLE = 1

def bfs(maze: Maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded


def dfs(maze: Maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded


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
