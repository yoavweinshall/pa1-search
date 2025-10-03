# HW1: Classical Search Algorithms

Welcome to HW1! In this assignment, you will implement five fundamental search algorithms for solving weighted mazes: **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, **Dijkstra's Algorithm**, **A\* search**, and **Greedy Best-First Search (GBFS)**.

## Assignment Overview

You will be working with a maze-solving application that provides a visual interface for testing your search algorithms. The maze is represented as a grid where:
- **White cells** have weight 1 (normal cost)
- **Blue cells** have weight 5 (higher cost)
- **Black cells** are unwalkable (walls)
- **Green cell** is the start position
- **Red cell** is the goal position
  
**You will only be submitting ai.py to gradescope!**

## What You Need to Implement

**You will need to edit two files:**

### 1. `maze/ai.py` - Search Algorithms
This file contains five functions that you need to implement:

1. **`bfs(maze, metrics=None)`** - Implement Breadth-First Search
2. **`dfs(maze, metrics=None)`** - Implement Depth-First Search  
3. **`dijkstra(maze, metrics=None)`** - Implement Dijkstra's Algorithm
4. **`a_star(maze, heuristic, metrics=None)`** - Implement A* search with a given heuristic
5. **`gbfs(maze, heuristic, metrics=None)`** - Implement Greedy Best-First Search
6. **`manhattan_distance(pos1, pos2)`** - Calculate Manhattan distance between two positions
7. **`euclidean_distance(pos1, pos2)`** - Calculate Euclidean distance between two positions
8. **Zero heuristic** - Already implemented (always returns 0)

### Function Requirements

**Search Algorithm Functions:**
- Each function should return a **path** (list of (row, col) tuples) from start to goal (inclusive) and a set of **expanded nodes**
- Return an **empty list** if no path exists
- For A* and GBFS, the `heuristic` parameter is a function that takes two positions and returns an estimated distance

**Heuristic Functions:**
- Each heuristic function takes two position tuples `(row, col)` and returns a numeric distance estimate
- **Manhattan distance**: |x1-x2| + |y1-y2| (sum of absolute differences)
- **Euclidean distance**: √((x1-x2)² + (y1-y2)²) (straight-line distance)
- These heuristics are used by A* and GBFS algorithms to estimate remaining distance to goal

## How to Test Your Code

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Use the GUI to test your algorithms:**
   - Select an algorithm (BFS, DFS, Dijkstra, A*, or GBFS)
   - Choose a heuristic (for A* and GBFS)
   - Click "Solve" to run your algorithm
   - Click "Regenerate" to create a new random maze

## Maze Interface

The `Maze` class provides these methods:
- `maze.start` - Start position (row, col)
- `maze.goal` - Goal position (row, col)  
- `maze.neighbors(r, c)` - Returns valid neighboring cells from position (r, c)
- `maze.grid[r][c]` - Access grid cell at row r, column c
- `maze.get_weight(r, c)` - Get the weight/cost of moving to cell (r, c)

## Example Usage

```python
# Get all valid neighbors from current position
for neighbor in maze.neighbors(current_row, current_col):
    # Process neighbor...

# Check if position is the goal
if current_pos == maze.goal:
    # Found the goal!
```

## Tips

- Use appropriate data structures (queues for BFS, stacks for DFS, priority queues for Dijkstra/A*/GBFS)
- Keep track of visited nodes to avoid cycles
- For Dijkstra: Use actual path costs (g(n)) for priority queue
- For A*: Remember that f(n) = g(n) + h(n) where g(n) is the actual cost and h(n) is the heuristic
- For GBFS: Use only heuristic cost h(n) for priority queue (ignores actual path cost)
- Use `maze.get_weight(r, c)` to get the cost of moving to a cell

## Getting Started

1. Open `maze/ai.py` and implement the five search algorithms and heuristics
2. Test with `python main.py`
3. Experiment with different maze sizes and densities
4. Compare how Dijkstra finds optimal paths while A* uses heuristics for efficiency
5. Try different heuristics (zero, manhattan, euclidean) with A* and GBFS to see their impact

Good luck with your implementation!
