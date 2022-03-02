import numpy as np
import collections
import cv2

class Node:
	def __init__(self, coords = None, parent = None, children = None):
		self.parent = parent
		self.children = children
		self.coords = coords

def calc_error(x, y, point1, point2):
	if point2[0]-point1[0] != 0:
		slope = (point2[1]-point1[1])/(point2[0]-point1[0])
		constant = point1[1] - (slope*point1[0])
		error = y - (slope*x + constant)

	else:
		slope = (point2[0]-point1[0])/(point2[1]-point1[1])
		constant = point1[0] - (slope*point1[1])
		error = x - (slope*y + constant)
	return error

def create_graph():
	graph = np.zeros((250,400))
	org = 250
	points1 = [(65,36),(40,115),(70,80),(150,105)]
	points2 = [(org-120,165), (org-140,200), (org-120,235), (org-80,235), (org-60,200), (org-80,165)]

	for i in range(graph.shape[0]):
		for j in range(graph.shape[1]):
			e11 = calc_error(i, j, points1[0], points1[1])
			e12 = calc_error(i, j, points1[1], points1[3])
			e13 = calc_error(i, j, points1[3], points1[0])

			e14 = calc_error(i, j, points1[2], points1[1])
			e15 = calc_error(i, j, points1[1], points1[3])
			e16 = calc_error(i, j, points1[3], points1[2])


			e21 = calc_error(i, j, points2[0], points2[1])
			e22 = calc_error(i, j, points2[1], points2[2])
			e23 = calc_error(i, j, points2[2], points2[3])
			e24 = calc_error(i, j, points2[3], points2[4])
			e25 = calc_error(i, j, points2[4], points2[5])
			e26 = calc_error(i, j, points2[5], points2[0])

			ec = 40**2 - (j-300)**2 - (i-65)**2
			if ec >= 0: # Circle
				graph[i,j] = 1

			# Abstract shape
			if e11 >= 0 and e12 <= 0 and e13 >= 0:
				graph[i,j] = 1
			if e14 >= 0 and e15 <= 0 and e16 >= 0:
				graph[i,j] = 0

			# Hexagon
			if e21 >= 0 and e22 <= 0 and e24 <= 0 and e25 >= 0 and e23 <= 0 and e26 >= 0:
				graph[i,j] = 1

	return graph

def check(coords1, coords2):
	if coords1 == coords2:
		return True
	else:
		return False

def exist(coords, storage):
	val = False
	new_coords = coords
	for i, ele in enumerate(storage):
		if ele == coords:
			val = True
			new_coords = i
	return val, new_coords

def move_up(node, graph):
	# import pdb; pdb.set_trace()
	if node[0]-1 >= 0 and graph[node[0]-1, node[1]] == 0:
		return True, [node[0]-1, node[1]]
	else:
		return False, None

def move_down(node, graph):
	# import pdb; pdb.set_trace()
	if node[0]+1 <= graph.shape[0]-1 and graph[node[0]+1, node[1]] == 0:
		return True, [node[0]+1, node[1]]
	else:
		return False, None

def move_left(node, graph):
	if node[1]-1 >= 0 and graph[node[0], node[1]-1] == 0:
		return True, [node[0], node[1]-1]
	else:
		return False, None

def move_right(node, graph):
	if node[1]+1 <= graph.shape[1]-1 and graph[node[0], node[1]+1] == 0:
		return True, [node[0], node[1]+1]
	else:
		return False, None

def move_ul(node, graph):
	if node[0]-1 >= 0 and node[1]-1 >= 0 and graph[node[0]-1, node[1]-1] == 0:
		return True, [node[0]-1, node[1]-1]
	else:
		return False, None

def move_ur(node, graph):
	if node[0]-1 >= 0 and node[1]+1 <= graph.shape[1]-1 and graph[node[0]-1, node[1]+1] == 0:
		return True, [node[0]-1, node[1]+1]
	else:
		return False, None

def move_dl(node, graph):
	if node[0]+1 <= graph.shape[0]-1 and node[1]-1 >= 0 and graph[node[0]+1, node[1]-1] == 0:
		return True, [node[0]+1, node[1]-1]
	else:
		return False, None

def move_dr(node, graph):
	if node[0]+1 <= graph.shape[0]-1 and node[1]+1 <= graph.shape[1]-1 and graph[node[0]+1, node[1]+1] == 0:
		return True, [node[0]+1, node[1]+1]
	else:
		return False, None

def action(curr_node, storage, parent, graph, closed):
	length = len(storage)-1
	animate = graph.copy()
	up, up_node = move_up(curr_node, graph)
	down, down_node = move_down(curr_node, graph)
	left, left_node = move_left(curr_node, graph)
	right, right_node = move_right(curr_node, graph)
	ul, ul_node = move_ul(curr_node, graph)
	ur, ur_node = move_ur(curr_node, graph)
	dl, dl_node = move_dl(curr_node, graph)
	dr, dr_node = move_dr(curr_node, graph)
	# import pdb; pdb.set_trace()
	if ul:
		yes, location = exist(ul_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]+1.4:
			storage[location][0][1] = storage[parent][0][1]+1.4
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([ul_node, storage[parent][0][1]+1.4, parent])
			closed.append(ul_node)
			animate[ul_node] = 155
			length += 1
	if ur:
		yes, location = exist(ur_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]+1.4:
			storage[location][0][1] = storage[parent][0][1]+1.4
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([ur_node, storage[parent][0][1]+1.4, parent])
			closed.append(ur_node)
			animate[ur_node] = 155
			length += 1
	if dl:
		yes, location = exist(dl_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]+1.4:
			storage[location][0][1] = storage[parent][0][1]+1.4
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([dl_node, storage[parent][0][1]+1.4, parent])
			closed.append(dl_node)
			animate[dl_node] = 155
			length += 1
	if dr:
		yes, location = exist(dr_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]+1.4:
			storage[location][0][1] = storage[parent][0][1]+1.4
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([dr_node, storage[parent][0][1]+1.4, parent])
			closed.append(dr_node)
			animate[dr_node] = 155
			length += 1

	if up:
		yes, location = exist(up_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]:
			storage[location][0][1] = storage[parent][0][1]+1
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([up_node, storage[parent][0][1]+1, parent])
			closed.append(up_node)
			animate[up_node] = 155
			length += 1
	if down:
		yes, location = exist(down_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]:
			storage[location][0][1] = storage[parent][0][1]+1
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([down_node, storage[parent][0][1]+1, parent])
			closed.append(down_node)
			animate[down_node] = 155
			length += 1
	if left:
		yes, location = exist(left_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]:
			storage[location][0][1] = storage[parent][0][1]+1
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([left_node, storage[parent][0][1]+1, parent])
			closed.append(left_node)
			animate[left_node] = 155
			length += 1
	if right:
		yes, location = exist(right_node, closed)
		if yes and storage[location][0][1] > storage[parent][0][1]:
			storage[location][0][1] = storage[parent][0][1]+1
			storage[location][0][2] = parent
		elif not yes:
			storage[length].append([right_node, storage[parent][0][1]+1, parent])
			closed.append(right_node)
			animate[right_node] = 155
			length += 1

	return storage

def dijkstra(initial, goal):
	graph = create_graph()*255
	clearance = 5
	storage = collections.defaultdict(list)
	closed = []
	opn = []
	# cv2.imshow('Graph', graph)
	# cv2.waitKey(0)
	origin_shift = graph.shape[0]-1
	initial[0] = origin_shift - initial[0]
	goal[0] = origin_shift - goal[0]
	curr_node = initial
	storage[0].append([curr_node, 0, 0])
	closed.append(curr_node)
	counter = 0
	animate = graph.copy()
	# import pdb; pdb.set_trace()
	while not check(curr_node, goal):
		storage, closed = action(storage[counter][0][0], storage, counter, graph, closed)
		counter += 1
		curr_node = storage[counter][0][0]
		print(curr_node)
		animate[curr_node[0],curr_node[1]] = 80
		cv2.imshow('Graph', animate)
		cv2.waitKey(1)

def main():
	initial = [200,80]
	goal = [249, 399]
	dijkstra(initial, goal)

if __name__ == '__main__':
	main()