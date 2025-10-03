from collections import deque
import heapq, math
from common import plugins

def bfs(maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded


def dfs(maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded

def dijkstra(maze):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded

def manhattan_distance(a, b):
    # TODO
    return None

def euclidean_distance(a, b):
    # TODO
    return None

def a_star(maze, heuristic):
    start, goal = maze.start, maze.goal
    path = []
    expanded = set()

    # TODO
    pass

    return path, expanded

def gbfs(maze, heuristic):
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
