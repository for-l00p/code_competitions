from pprint import pprint
import copy

infile = open('input.txt', 'r')
outfile = open('output.txt', 'w')

num_problems = int(infile.readline())

def output(text):
	print(text)
	global outfile
	outfile.write("%s\n" % text)

def print_grid(grid):
	for line in grid:
		print(''.join(line))
	print('')

def find_shortest_path(graph, start, end):
	steps = 1
	seen = []
	new = [start]
	found = False
	while not found:
		last = copy.copy(new)
		for l in last:
			seen.append(l)
		new = []
		for n in last:
			for g in graph[n]:
				if end == g:
					found = True
					new = [1]
					break
				if g not in seen and g not in last and g not in new:
					new.append(g)
			if found:
				break
		steps = steps + 1
		if not new:
			return False
	return steps

def locate(grid, symbol):
	global m,n
	for y in range(m):
		for x in range(n):
			if grid[y][x] == symbol:
				return x,y
	die("Error: symbol not found")
	
def grid_step(grid):
	for y in range(m):
		for x in range(n):
			if grid[y][x] == '-':
				grid[y][x] = '.'
	for y in range(m):
		for x in range(n):
			if grid[y][x] == '^':
				grid[y][x] = '>'
				for laser in range(x+1,n):
					if grid[y][laser] in ['^','>','v','<','#']:
						break
					grid[y][laser] = '-'
			elif grid[y][x] == '>':
				grid[y][x] = 'v'
				for laser in range(y+1,m):
					if grid[laser][x] in ['^','>','v','<','#']:
						break
					grid[laser][x] = '-'
			elif grid[y][x] == 'v':
				grid[y][x] = '<'
				for laser in range(x-1,-1,-1):
					if grid[y][laser] in ['^','>','v','<','#']:
						break
					grid[y][laser] = '-'
			elif grid[y][x] == '<':
				grid[y][x] = '^'
				for laser in range(y-1,-1,-1):
					if grid[laser][x] in ['^','>','v','<','#']:
						break
					grid[laser][x] = '-'
	return grid

def c(x,y,z):
	return "%s-%s-%s" % (x,y,z)

def solve(grid):
	S_x, S_y = locate(grid,'S')
	G_x, G_y = locate(grid,'G')
	grid[S_y][S_x] = '.'
	grid[G_y][G_x] = '.'
	grids = []
	for i in range(4):
		grids.append(copy.deepcopy(grid_step(grid)))
	# Our 3-d graph is created; let's connect some things:
	graph = {}
	for x in range(n):
		for y in range(m):
			for z in range(4):
				graph[c(x,y,z)] = []
				#left
				if x-1 >= 0 and grids[z][y][x] not in ['^','>','v','<','#'] and grids[(z+1)%4][y][x-1] not in ['^','>','v','<','#','-']:
					graph[c(x,y,z)].append(c(x-1,y,(z+1)%4))
				#right
				if x+1 < n and grids[z][y][x] not in ['^','>','v','<','#'] and grids[(z+1)%4][y][x+1] not in ['^','>','v','<','#','-']:
					graph[c(x,y,z)].append(c(x+1,y,(z+1)%4))
				#up
				if y-1 >= 0 and grids[z][y][x] not in ['^','>','v','<','#'] and grids[(z+1)%4][y-1][x] not in ['^','>','v','<','#','-']:
					graph[c(x,y,z)].append(c(x,y-1,(z+1)%4))
				#down
				if y+1 < m and grids[z][y][x] not in ['^','>','v','<','#'] and grids[(z+1)%4][y+1][x] not in ['^','>','v','<','#','-']:
					graph[c(x,y,z)].append(c(x,y+1,(z+1)%4))
	lengths = []
	for i in range(4):
		steps = find_shortest_path(graph, c(S_x,S_y,3), c(G_x,G_y,i))
		if steps:
			lengths.append(steps)
	if not lengths:
		return 0
	else:
		return min(lengths)-1
	
for i in range(num_problems):
	global m, n
	m, n = [int(x) for x in infile.readline().split(' ')]
	grid = []
	for row in range(m):
		grid.append(list(infile.readline().rstrip()))
	result = solve(grid)
	if result:
		output("Case %s: %s" % (i+1,result))
	else:
		output("Case %s: impossible" % (i+1))

infile.close()
outfile.close()