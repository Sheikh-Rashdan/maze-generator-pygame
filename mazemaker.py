import pygame
from sys import exit, argv as ARGUMENTS
from random import choice
from os import walk

class Vector:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
	def __repr__(self):
		return f'<{self.x},{self.y}>'
	def __add__(self, other):
		return Vector(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
		return Vector(self.x-other.x,self.y-other.y)
	def __neg__(self):
		return Vector(-self.x,-self.y)
	def __mul__(self, other):
		if type(other) not in (int, float):
			raise TypeError
		return Vector(self.x*other,self.y*other)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
		
	def to_tuple(self):
		return (self.x, self.y)
		
# static attributes
Vector.up = Vector(0,-1)
Vector.right = Vector(1,0)
Vector.down = Vector(0,1)
Vector.left = Vector(-1,0)
Vector.dirs = [Vector.up,Vector.right,Vector.down,Vector.left]


class Canvas:
	def __init__(self, size = Vector(5,5)):
		self.size = size
		self.values = [Cell(self, Vector(x,y)) for y in range(self.size.y) for x in range(self.size.x)]
		
		self.traversed_count = 0
		
	@property
	def can_traverse(self):
		return self.traversed_count<self.size.x*self.size.y
		
	def check_pos_in_range(self, pos):
		if not(0<=pos.x<self.size.x and 0<=pos.y<self.size.y):
			raise ValueError
			
	def get_index_from_pos(self, pos):
		return pos.y*self.size.x+pos.x
			
	def traverse(self):
			generator = self.get_traversal_generator()
			while self.can_traverse:
				next(generator)
			
	def get_traversal_generator(self, start_pos = Vector()):
		cur_cell = self[start_pos]
		self.visited_cells = [cur_cell]
			
		while self.can_traverse:
			cur_cell = self.visited_cells[-1]
			if not cur_cell.visited:
				cur_cell.visited = True
				self.traversed_count += 1

			unvisited_neighbour_cells = self.get_unvisited_neighbour_cells(cur_cell)
				
			if unvisited_neighbour_cells:
				next_cell = choice(unvisited_neighbour_cells)
				self.create_entrance(cur_cell, next_cell)
				self.visited_cells.append(next_cell)
				
			else:
				if self.visited_cells:
					self.visited_cells.pop()
			
			yield
				
	def get_unvisited_neighbour_cells(self, cell):
		unvisited_neighbour_cells = []
		for Vdir in Vector.dirs:
			try:
				neighbour_cell = self[cell.pos+Vdir]
				if not neighbour_cell.visited:
					unvisited_neighbour_cells.append(neighbour_cell)
			except ValueError:
				pass
		return unvisited_neighbour_cells
			
	def create_entrance(self, cellA, cellB):
		cellA.entrances.append(cellB.pos-cellA.pos)
		cellB.entrances.append(cellA.pos-cellB.pos)
					
	def __getitem__(self, pos):
		self.check_pos_in_range(pos)
		i = self.get_index_from_pos(pos)
		return self.values[i]
	def __setitem__(self, pos, value):
		i = self.get_index_from_pos(pos)
		self.values[i] = value
	def __iter__(self):
		return iter(self.values)
	def __repr__(self):
		return f'{self.values}'
		

class Cell:
	def __init__(self, parent_canvas, pos):
		self.canvas = parent_canvas
		
		self.pos = pos
		self.visited = False
		self.entrances = []
		
	def __repr__(self):
		return f'C{self.pos}{"T" if self.visited else "F"}'


def load_sprites():
	sprites = {}
	for path, _, files in list(walk('sprites')):
		for file in files:
			image = pygame.image.load(path+'/'+file).convert()
			image = pygame.transform.scale(image, (grid_size,grid_size))
			sprites[file.rpartition('.')[0]] = image
	return sprites
	
def get_sprite_name(cell):
	name = ''
	for Vdir in Vector.dirs:
		if Vdir in cell.entrances:
			name += 'T'
		else:
			name += 'F'
	return name
	

pygame.init()

canvas_grid_count = 10
if(len(ARGUMENTS)!=1): canvas_grid_count = int(ARGUMENTS[1])
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Mazemaker")
w,h = screen.get_size()

# canvas
canvas_size = Vector(canvas_grid_count,canvas_grid_count)
canvas = Canvas(canvas_size)
start_pos = Vector()
canvas_traversal_generator = canvas.get_traversal_generator(start_pos)

# values
grid_size = w/canvas.size.x
max_cells = -1
speed = 100 # limited by fps

# sprites
sprites = load_sprites()

def draw_canvas(canvas):
	for cell in canvas:
		pos = (cell.pos*grid_size).to_tuple()
		name = get_sprite_name(cell)
		screen.blit(sprites[name], (pos,(grid_size,)*2))
		
def draw_cursor(canvas):
	cursor_cell = canvas.visited_cells[-1]
	pos = (cursor_cell.pos*grid_size).to_tuple()
	pygame.draw.rect(screen, 'orange', (pos,(grid_size,)*2))

while True:
	
	dt = pygame.time.Clock().tick(speed)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
			
	screen.fill('black')
	draw_canvas(canvas)
	if canvas.can_traverse and (max_cells <= 0 or canvas.traversed_count<max_cells-1):
		next(canvas_traversal_generator)
		draw_cursor(canvas)
	
	pygame.display.flip()