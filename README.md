# Maze Generator

MazeMaker is a Python and Pygame visualizer that generates a maze with randomized depth-first search (recursive backtracking), then explores it with depth-first and breadth-first search.

## Features

- Watch a maze being carved one cell at a time.
- Explore the completed maze with DFS, followed by BFS.
- Set the square grid size when launching the program.

## Requirements

- Python
- Pygame

Install Pygame with:

```bash
python -m pip install pygame
```

## Run

```bash
python mazemaker.py [grid_size]
```

`grid_size` is optional and sets the number of cells along each side of the square grid. It defaults to `10`. For example:

```bash
python mazemaker.py 20
```

## Controls

- Wait for maze generation to finish.
- Press **Space** to start the DFS search.
- After DFS finishes, press **Space** again to start the BFS search.
- Close the window to exit.

## Gallery

<p align="center">
  <img width="628" height="666" alt="mazemaker-pygame-demo-showcase" src="https://github.com/user-attachments/assets/53f40737-9125-4fdb-8d9a-02c1c101b709" />
</p>
