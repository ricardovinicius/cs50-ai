import sys
from PIL import Image, ImageDraw, ImageFont

class Node():
  def __init__(self, state, parent, action):
    self.state = state
    self.parent = parent
    self.action = action
    
class StackFrontier():
  def __init__(self):
    self.frontier = []
  
  def add(self, node):
    self.frontier.append(node)
  
  def contains_state(self, state):
    return any(node.state == state for node in self.frontier)
  
  def empty(self):
    return len(self.frontier) == 0
  
  def remove(self):
    if self.empty():
      raise Exception("empty frontier")
    else:
      node = self.frontier[-1]
      self.frontier = self.frontier[:-1]
      return node
    
  def sort_reverse(self, func):
    self.frontier.sort(key=func, reverse=True)
    
    return self

    
class QueueFrontier(StackFrontier):
  def remove(self):
    if self.empty():
      raise Exception("empty frontier")
    else:
      node = self.frontier[0]
      self.frontier = self.frontier[1:]
      return node
    
class Maze():

  def __init__(self, filename):

    # Read file and set height and width of maze
    with open(filename) as f:
      contents = f.read()

    # Validate start and goal
    if contents.count("A") != 1:
      raise Exception("maze must have exactly one start point")
    if contents.count("B") != 1:
      raise Exception("maze must have exactly one goal")

    # Determine height and width of maze
    contents = contents.splitlines()
    self.height = len(contents)
    self.width = max(len(line) for line in contents)

    # Keep track of walls
    self.walls = []
    for i in range(self.height):
      row = []
      for j in range(self.width):
        try:
          if contents[i][j] == "A":
            self.start = (i, j)
            row.append(False)
          elif contents[i][j] == "B":
            self.goal = (i, j)
            row.append(False)
          elif contents[i][j] == " ":
            row.append(False)
          else:
            row.append(True)
        except IndexError:
          row.append(False)
      self.walls.append(row)

    self.solution = None
    
  def print(self):
    solution = self.solution[1] if self.solution is not None else None
    print()
    for i, row in enumerate(self.walls):
      for j, col in enumerate(row):
        if col:
          print("#", end="")
        elif (i, j) == self.start:
          print("A", end="")
        elif (i, j) == self.goal:
          print("B", end="")
        elif solution is not None and (i, j) in solution:
          print("*", end="")
        else:
          print(" ", end="")
      print()
    print()


  def neighbors(self, state):
    row, col = state
    candidates = [
      ("up", (row - 1, col)),
      ("down", (row + 1, col)),
      ("left", (row, col - 1)),
      ("right", (row, col + 1))
    ]

    result = []
    for action, (r, c) in candidates:
      if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
        result.append((action, (r, c)))
    return result
  
  def h(self, node):
    row, col = node.state
    row_goal, col_goal = self.goal
    
    return abs((row_goal - row)) + abs((col_goal - col))
  
  def g(self, node):
    row, col = node.state
    row_start, col_start = self.start
    
    return abs((row_start - row)) + abs((col_start - col))
  
  def h_g(self, node):
    return self.h(node) + self.g(node)
  
  def solve(self):
    """Find a solution to maze, if one exists."""
    
    # Keep track of number of states explored
    self.num_explored = 0
    
    # Initialize frontier to just the starting position
    start = Node(state=self.start, parent=None, action=None)
    frontier = StackFrontier()
    frontier.add(start)
    
    # Initialize an empty explored set
    self.explored = set()
    
    # Keep looping until solution found
    while True:
      
      # If nothing left in frontier, then no path
      if frontier.empty():
        raise Exception("no solution")
      
      # Choose a node from the frontier
      node = frontier.sort_reverse(self.h_g).remove()
      self.num_explored += 1
      
      # If node is the goal, then we have a solution
      if node.state == self.goal:
        actions = []
        cells = []
        while node.parent is not None:
          actions.append(node.action)
          cells.append(node.state)
          node = node.parent
        actions.reverse()
        cells.reverse()
        self.solution = (actions, cells)
        return

      # Mark node as explored
      self.explored.add(node.state)
      
      # Add neighbors to frontier
      for action, state in self.neighbors(node.state):
        if not frontier.contains_state(state) and state not in self.explored:
          child = Node(state=state, parent=node, action=action)
          frontier.add(child)
      
  def output_image(self, filename, show_solution=True, show_explored=False):
      cell_size = 50
      cell_border = 2

      # Cria uma tela em branco
      img = Image.new(
          "RGBA",
          (self.width * cell_size, self.height * cell_size),
          "black"
      )
      draw = ImageDraw.Draw(img)

      # Define a fonte para desenhar o texto
      try:
          font = ImageFont.truetype("arial.ttf", 16)  # Tente usar a fonte Arial
      except IOError:
          font = ImageFont.load_default()  # Caso a fonte Arial não esteja disponível

      solution = self.solution[1] if self.solution is not None else None
      for i, row in enumerate(self.walls):
          for j, col in enumerate(row):

              # Pinta as paredes
              if col:
                  fill = (40, 40, 40)
              # Pinta o ponto de início
              elif (i, j) == self.start:
                  fill = (255, 0, 0)
              # Pinta o ponto final
              elif (i, j) == self.goal:
                  fill = (0, 171, 28)
              # Pinta a solução
              elif solution is not None and show_solution and (i, j) in solution:
                  fill = (220, 235, 113)
              # Pinta as células exploradas
              elif solution is not None and show_explored and (i, j) in self.explored:
                  fill = (212, 97, 85)
              # Célula vazia
              else:
                  fill = (237, 240, 252)

              # Desenha a célula
              draw.rectangle(
                  [(j * cell_size + cell_border, i * cell_size + cell_border),
                  ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)],
                  fill=fill
              )

              # Desenha o valor da heurística no meio da célula
              h_value = self.h_g(Node(state=(i, j), parent=None, action=None))
              text = str(h_value)

              # Usa textbbox para obter a largura e altura do texto
              text_bbox = draw.textbbox((0, 0), text, font=font)
              text_width = text_bbox[2] - text_bbox[0]
              text_height = text_bbox[3] - text_bbox[1]

              text_x = j * cell_size + (cell_size - text_width) / 2
              text_y = i * cell_size + (cell_size - text_height) / 2
              draw.text((text_x, text_y), text, fill="black", font=font)

      img.save(filename)

    
if len(sys.argv) != 2:
  sys.exit("Usage: python maze.py maze.txt")
  
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)

