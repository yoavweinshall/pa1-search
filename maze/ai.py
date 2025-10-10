from collections import deque
import heapq, math
from typing import Tuple, Dict, List, Set, Union

from common import plugins
from .game import Maze

ROW_LOCATION_IN_POSITION_TUPLE = 0
COLUMN_LOCATION_IN_POSITION_TUPLE = 1
WALL_WEIGHT = float('inf')
NO_SOL_WEIGHT = float('inf')


def get_non_wall_neighbors(maze: Maze, location: Tuple[int, int]):
    """
    wrapper to the get neighbor function that returns only the none wall neighbors
    :param maze: the maze
    :param location: the location we want its neighbors
    :return: a generator that yields the none wall neighbors
    """
    for neighbor in maze.neighbors(*location):
        if maze.get_weight(*neighbor) != WALL_WEIGHT:
            yield neighbor


def build_path_from_prev_dict(start: Tuple[int, int],
                              goal: Tuple[int, int],
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


def explore_neighbors(maze: Maze,
                      node: Tuple[int, int],
                      nodes_to_explore: Union[deque[Tuple[int,int]],
                      List[Tuple[int,int]]],expanded: Set[tuple[int,int]],
                      prev_dict: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
    """
    look at the neighbors of a node by update the distances and prev dicts and adding the
    neighbors for check later (when depends on algorithm)
    :param maze: The maze
    :param node: the node we want to explore its neighbors
    :param nodes_to_explore: data structure that holds the nodes that we need yet to explore
    :param expanded: nodes we visited in
    :param prev_dict: the dictionary that holds the previous node on the shortest path found to each node
    :return: None
    """
    expanded.add(node)
    for neighbor in get_non_wall_neighbors(maze, node):
        if neighbor not in prev_dict:
            prev_dict[neighbor] = node
            nodes_to_explore.append(neighbor)


def bfs(maze: Maze)-> (List[Tuple[int, int]], Set[Tuple[int, int]]):
    """
    solve the maze using bfs algorithm
    :param maze: the maze
    :return: the shortest path and the locations we visited in while trying to solve the naze
    """
    prev = {}
    expanded = set()
    node_queue = deque([maze.start])
    while node_queue:
        node = node_queue.popleft()
        explore_neighbors(maze, node, node_queue, expanded, prev)
    return build_path_from_prev_dict(maze.start, maze.goal, prev) if maze.goal in expanded else [], expanded


def dfs(maze: Maze)-> (List[Tuple[int, int]], Set[Tuple[int, int]]):
    """
    solve the maze using dfs algorithm
    :param maze: the maze
    :return: the shortest path and the locations we visited in while trying to solve the naze
    """
    prev = {}
    expanded = set()
    node_stack = [maze.start]
    while node_stack:
        node = node_stack.pop()
        explore_neighbors(maze, node, node_stack, expanded, prev)
    return build_path_from_prev_dict(maze.start, maze.goal, prev) if maze.goal in expanded else [], expanded


def dijkstra(maze: Maze):
    expanded = {maze.start}
    prev = {}
    nodes_heap = [(0, maze.start)]
    heapq.heapify(nodes_heap)
    while nodes_heap and maze.goal not in expanded:
        price, node = heapq.heappop(nodes_heap)
        for neighbor in get_non_wall_neighbors(maze, node):
            if neighbor not in expanded:
                expanded.add(neighbor)
                prev[neighbor] = node
                heapq.heappush(nodes_heap, (price + maze.get_weight(*neighbor), neighbor))
    return build_path_from_prev_dict(maze.start, maze.goal, prev) if maze.goal in expanded else [], expanded

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    calculates manhattan distance between to cells
    :param a: position of first cell in a (row,column) tuple
    :param b: position of second cell in a (row,column) tuple
    :return: The manhattan distance between two cells defined to be |a.x - b.x| + |a.y - b.y|
    """
    return (abs(a[ROW_LOCATION_IN_POSITION_TUPLE] - b[ROW_LOCATION_IN_POSITION_TUPLE]) +
                abs(a[COLUMN_LOCATION_IN_POSITION_TUPLE] - b[COLUMN_LOCATION_IN_POSITION_TUPLE]))


def euclidean_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    calculates Euclidean distance between two cells
    :param a: position of first cell in a (row,column) tuple
    :param b: position of second cell in a (row,column) tuple
    :return: The Euclidian distance between two cells defined to be sqrt((a.x - b.x)^2 + (a.y - b.y)^2)
    """
    return math.sqrt((a[ROW_LOCATION_IN_POSITION_TUPLE] - b[ROW_LOCATION_IN_POSITION_TUPLE]) ** 2 +
                     (a[COLUMN_LOCATION_IN_POSITION_TUPLE] - b[COLUMN_LOCATION_IN_POSITION_TUPLE]) ** 2)


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
