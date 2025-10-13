from collections import deque
import heapq, math
from typing import Tuple, Dict, List, Set, Union, Callable, Generator

from common import plugins
from .game import Maze

ROW_LOCATION_IN_POSITION_TUPLE = 0
COLUMN_LOCATION_IN_POSITION_TUPLE = 1
WALL_WEIGHT = float('inf')
NO_SOL_WEIGHT = float('inf')


def get_non_wall_neighbors(maze: Maze, location: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
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


def explore_neighbors_list_adt(maze: Maze,
                               node: Tuple[int, int],
                               nodes_to_explore: Union[deque[Tuple[int,int]], List[Tuple[int,int]]],
                               expanded: Set[tuple[int,int]],
                               prev_dict: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
    """
    look at the neighbors of a node by update the distances and prev dicts and adding the
    neighbors for check later (when depends on algorithm). This function works with algorithms that uses implementation
    of the ADT list to choose the next node to explore (BFS/DFS)
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
    :return: A solution to the maze ant the locations we visited in while trying to solve the maze
    """
    prev = {}
    expanded = set()
    node_queue = deque([maze.start])
    while node_queue and maze.goal not in expanded:
        node = node_queue.popleft()
        explore_neighbors_list_adt(maze, node, node_queue, expanded, prev)
    return build_path_from_prev_dict(maze.start, maze.goal, prev) if maze.goal in expanded else [], expanded


def dfs(maze: Maze)-> (List[Tuple[int, int]], Set[Tuple[int, int]]):
    """
    solve the maze using dfs algorithm
    :param maze: the maze
    :return: A solution to the maze ant the locations we visited in while trying to solve the maze
    """
    prev = {}
    expanded = set()
    node_stack = [maze.start]
    while node_stack and maze.goal not in expanded:
        node = node_stack.pop()
        explore_neighbors_list_adt(maze, node, node_stack, expanded, prev)
    return build_path_from_prev_dict(maze.start, maze.goal, prev) if maze.goal in expanded else [], expanded


def dijkstra(maze: Maze):
    """
    solve the maze using GBFS algorithm
    :param maze: the maze we try to solve
    :return: A solution to the maze ant the locations we visited in while trying to solve the maze
    """
    expanded = set()
    prev = {}
    nodes_heap = [(0, maze.start)]
    heapq.heapify(nodes_heap)
    while nodes_heap and maze.goal not in expanded:
        price, node = heapq.heappop(nodes_heap)
        expanded.add(node)
        for neighbor in get_non_wall_neighbors(maze, node):
            if neighbor not in prev:
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


def a_star(maze: Maze, heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float])\
        -> (List[Tuple[int, int]], Set[Tuple[int, int]]):
    """
    solve the maze using A* algorithm
    :param maze: the maze we try to solve
    :param heuristic: the heuristic function to decide on which node to explore next among neighbors
    :return: A solution to the maze ant the locations we visited in while trying to solve the maze
    """
    expanded = set()
    prev = {}
    nodes_heap = [(0.0, maze.start, heuristic(maze.start, maze.goal))]
    heapq.heapify(nodes_heap)
    while nodes_heap:
        est_price, node, node_distance = heapq.heappop(nodes_heap)
        expanded.add(node)
        if node == maze.goal:
            return build_path_from_prev_dict(maze.start, maze.goal, prev), expanded
        for neighbor in get_non_wall_neighbors(maze, node):
            if neighbor not in prev:
                prev[neighbor] = node
                #set the price in a way that the closest by heuristic function will have a lower key in heap
                fixed_price = est_price + maze.get_weight(*neighbor) + heuristic(neighbor, maze.goal) - node_distance
                heapq.heappush(nodes_heap, (fixed_price, neighbor, heuristic(neighbor, maze.goal)))
    return [], expanded


def gbfs(maze: Maze, heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float])\
        -> (List[Tuple[int, int]], Set[Tuple[int, int]]):
    """
    solve the maze using GBFS algorithm
    :param maze: the maze we try to solve
    :param heuristic: the heuristic function to decide on which node to explore next
    :return: A solution to the maze ant the locations we visited in while trying to solve the maze
    """
    expanded = set()
    prev = {}
    nodes_heap = [(0.0, maze.start)]
    heapq.heapify(nodes_heap)
    while nodes_heap and maze.goal not in expanded:
        distance, node = heapq.heappop(nodes_heap)
        expanded.add(node)
        for neighbor in get_non_wall_neighbors(maze, node):
            if neighbor not in prev:
                prev[neighbor] = node
                # set the key to be distance from goal
                heapq.heappush(nodes_heap, (heuristic(neighbor, maze.goal), neighbor))
    return build_path_from_prev_dict(maze.start, maze.goal, prev) if maze.goal in expanded else [], expanded

# === DO NOT EDIT: Heuristic registration for GUI ===
def zero_heuristic(a, b):
    return 0
plugins.register('maze', 'zero', zero_heuristic)
plugins.register('maze', 'manhattan', manhattan_distance)
plugins.register('maze', 'euclidean', euclidean_distance)
