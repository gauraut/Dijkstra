import numpy as np
import cv2
import time

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

def create_graph(pad_size = 10):
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

def exist(coords, storage, opened):
	# import pdb; pdb.set_trace()
	if len(opened) != 0:
		opn = np.array(opened)[:,1].tolist()
		# print(opn)
		storage = storage[::-1]
		if (coords in storage) and (coords in opn):
			return True, storage.index(coords), opn.index(coords), True
		elif (coords in storage) and (coords not in opn):
			return True, storage.index(coords), None, False
	return False, None, None, False

def xor(a,b):
	if a != b:
		return True
	else:
		return False

def check_dist(node,graph):
	shape = graph.shape
	# print(graph[65,300])
	if  node[0]+cl2 <= shape[0]-1 and node[0]-cl2 >= 0 and node[1]+cl2 <= shape[1]-1 and node[1]-cl2 >= 0 and graph[node[0]+cl2,node[1]] == 0 and graph[node[0]-cl2,node[1]] == 0 and graph[node[0],node[1]-cl2] == 0  and graph[node[0],node[1]+cl2]:
		return True
	return False

def detect(y,x,graph):
	cl =5
	y = abs(249-y)
	if (250 - (y+cl) > 0):
		if (graph[249-(y+cl)][x] > 0):
			#print("1")
			return False
	if (250 - (y-cl) <= 249):
		if (graph[249-(y-cl)][x] > 0):
			#print("2")
			return False
	if ( x+cl < 399 ):
		if (graph[249-y][x+cl] > 0):
			#print("3")
			return False
	if ( x-cl > 0 ):
		if (graph[249-y][x-cl] > 0):
			#print("4")
			return False
		
	if (250 - (y+cl) > 0) and ( x+cl < 399 ):
		if (graph[249-(y+cl)][x+cl] > 0):
			#print("1")
			return False
	if (250 - (y-cl) <= 249) and ( x-cl > 0 ):
		if (graph[249-(y-cl)][x-cl] > 0):
			#print("2")
			return False
	if (250 - (y-cl) <= 249) and ( x+cl < 399 ):
		if (graph[249-(y-cl)][x+cl] > 0):
			#print("2")
			return False
	if (250 - (y-cl) <= 249) and ( x-cl > 0 ):
		if (graph[249-(y-cl)][x-cl] > 0):
			#print("2")
			return False
	
	return True

def move_up(node, graph):
	if detect(node[0],node[1],graph):
		if node[0]-1 >= 0 and graph[node[0]-1, node[1]] == 0:
			return True, [node[0]-1, node[1]]
	return False, None

def move_down(node, graph):
	if detect(node[0],node[1],graph):
		if node[0]+1 <= graph.shape[0]-1 and graph[node[0]+1, node[1]] == 0:
			return True, [node[0]+1, node[1]]
	return False, None

def move_left(node, graph):
	if detect(node[0],node[1],graph):
		if node[1]-1 >= 0 and graph[node[0], node[1]-1] == 0:
			return True, [node[0], node[1]-1]
	return False, None

def move_right(node, graph):
	if detect(node[0],node[1],graph):
		if node[1]+1 <= graph.shape[1]-1 and graph[node[0], node[1]+1] == 0:
			return True, [node[0], node[1]+1]
	return False, None

def move_ul(node, graph):
	if detect(node[0],node[1],graph):
		if node[0]-1 >= 0 and node[1]-1 >= 0 and graph[node[0]-1, node[1]-1] == 0:
			return True, [node[0]-1, node[1]-1]
	return False, None

def move_ur(node, graph):
	if detect(node[0],node[1],graph):
		if node[0]-1 >= 0 and node[1]+1 <= graph.shape[1]-1 and graph[node[0]-1, node[1]+1] == 0:
			return True, [node[0]-1, node[1]+1]
	return False, None

def move_dl(node, graph):
	if detect(node[0],node[1],graph):
		if node[0]+1 <= graph.shape[0]-1 and node[1]-1 >= 0 and graph[node[0]+1, node[1]-1] == 0:
			return True, [node[0]+1, node[1]-1]
	return False, None

def move_dr(node, graph):
	if detect(node[0],node[1],graph):
		if node[0]+1 <= graph.shape[0]-1 and node[1]+1 <= graph.shape[1]-1 and graph[node[0]+1, node[1]+1] == 0:
			return True, [node[0]+1, node[1]+1]
	return False, None

def action(curr_node, storage, parent, graph, goal, closed, opn):
	length = len(storage)
	found = False
	up, up_node = move_up(curr_node, graph)
	down, down_node = move_down(curr_node, graph)
	left, left_node = move_left(curr_node, graph)
	right, right_node = move_right(curr_node, graph)

	if up:
		yes, location, oploc, opyes = exist(up_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1:
			storage[location][1] = storage[parent][1]+1
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1
				opn[oploc][3] = parent
		elif not yes:
			if check(up_node, goal):
				found = True
				storage[length] = [up_node, storage[parent][1]+1, parent]
				# opn.append([length, up_node, storage[parent][1]+1, parent])
				return storage, found, closed, opn
			storage[length] = [up_node, storage[parent][1]+1, parent]
			opn.append([length, up_node, storage[parent][1]+1, parent])
			closed.append(up_node)
			length += 1

	if down:
		yes, location, oploc, opyes = exist(down_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1:
			storage[location][1] = storage[parent][1]+1
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1
				opn[oploc][3] = parent

		elif not yes:
			if check(down_node, goal):
				found = True
				storage[length] = [down_node, storage[parent][1]+1, parent]
				return storage, found, closed, opn
			storage[length] = [down_node, storage[parent][1]+1, parent]
			opn.append([length, down_node, storage[parent][1]+1, parent])
			closed.append(down_node)
			length += 1


	if right:
		yes, location, oploc, opyes = exist(right_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1:
			storage[location][1] = storage[parent][1]+1
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1
				opn[oploc][3] = parent

		elif not yes:
			if check(right_node, goal):
				found = True
				storage[length] = [right_node, storage[parent][1]+1, parent]
				return storage, found, closed, opn
			storage[length] = [right_node, storage[parent][1]+1, parent]
			opn.append([length, right_node, storage[parent][1]+1, parent])
			closed.append(right_node)
			length += 1


	if left:
		yes, location, oploc, opyes = exist(left_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1:
			storage[location][1] = storage[parent][1]+1
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1
				opn[oploc][3] = parent

		elif not yes:
			if check(left_node, goal):
				found = True
				storage[length] = [left_node, storage[parent][1]+1, parent]
				return storage, found, closed, opn
			storage[length] = [left_node, storage[parent][1]+1, parent]
			opn.append([length, left_node, storage[parent][1]+1, parent])
			closed.append(left_node)
			length += 1

	
	ul, ul_node = move_ul(curr_node, graph)
	if ul:
		yes, location, oploc, opyes = exist(ul_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1.4:
			storage[location][1] = storage[parent][1]+1.4
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1.4
				opn[oploc][3] = parent

		elif not yes:
			if check(ul_node, goal):
				found = True
				storage[length] = [ul_node, storage[parent][1]+1.4, parent]
				return storage, found, closed, opn

			storage[length] = [ul_node, storage[parent][1]+1.4, parent]
			opn.append([length, ul_node, storage[parent][1]+1.4, parent])
			closed.append(ul_node)
			length += 1

	ur, ur_node = move_ur(curr_node, graph)

	if ur:
		yes, location, oploc, opyes = exist(ur_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1.4:
			storage[location][1] = storage[parent][1]+1.4
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1.4
				opn[oploc][3] = parent

		elif not yes:
			if check(ur_node, goal):
				found = True
				storage[length] = [ur_node, storage[parent][1]+1.4, parent]
				return storage, found, closed, opn
			storage[length] = [ur_node, storage[parent][1]+1.4, parent]
			opn.append([length, ur_node, storage[parent][1]+1.4, parent])
			closed.append(ur_node)
			length += 1

	dl, dl_node = move_dl(curr_node, graph)

	if dl:
		yes, location, oploc, opyes = exist(dl_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1.4:
			storage[location][1] = storage[parent][1]+1.4
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1.4
				opn[oploc][3] = parent

		elif not yes:
			if check(dl_node, goal):
				found = True
				storage[length] = [dl_node, storage[parent][1]+1.4, parent]
				return storage, found, closed, opn
			storage[length] = [dl_node, storage[parent][1]+1.4, parent]
			opn.append([length, dl_node, storage[parent][1]+1.4, parent])
			closed.append(dl_node)
			length += 1

	dr, dr_node = move_dr(curr_node, graph)
	if dr:
		yes, location, oploc, opyes = exist(dr_node, closed, opn)
		if yes and storage[location][1] > storage[parent][1]+1.4:
			storage[location][1] = storage[parent][1]+1.4
			storage[location][2] = parent
			if opyes:
				opn[oploc][2] = storage[parent][1]+1.4
				opn[oploc][3] = parent
		elif not yes:
			if check(dr_node, goal):
				found = True
				storage[length] = [dr_node, storage[parent][1]+1.4, parent]
				return storage, found, closed, opn
			storage[length] = [dr_node, storage[parent][1]+1.4, parent]
			opn.append([length, dr_node, storage[parent][1]+1.4, parent])
			closed.append(dr_node)
			length += 1

	return storage, found, closed, opn

def dijkstra(initial, goal):
	pad_size = 0
	graph = create_graph(pad_size)*255
	animate = graph.copy()
	clearance = 5
	closed = []
	opn = []

	origin_shift = graph.shape[0]-1
	initial[0] = origin_shift - initial[0]
	goal[0] = origin_shift - goal[0]
	explored = []
	curr_node = initial
	storage = {0: [curr_node, 0, 0]}
	closed.append(curr_node)
	explored.append(0)
	counter = 0
	found = False

	while not check(curr_node, goal):
		storage, found, closed, opn = action(curr_node, storage.copy(), counter, graph, goal, closed.copy(), opn.copy())
		if found:
			explored.append(len(storage)-1)
			break

		new = np.argsort(np.array(opn.copy())[:,2])[0]
		temp = opn.pop(new)
		counter = temp[0]
		print(counter, len(storage)-1)
		if len(storage) > 90000:
			print("Node not found")
			return storage, False, explored

		explored.append(temp[0])
		curr_node = storage[counter][0]

	return storage, True, explored

def animate(storage, explored):
	b = create_graph()*0
	g = create_graph()*255
	r = create_graph()*0
	graph = np.dstack([b,g,r]).astype(np.uint8)

	for i in explored:
		graph[storage[i][0][0], storage[i][0][1]] = np.array([0, 155, 255])
		cv2.imshow('Graph', graph)
		cv2.waitKey(1)

	curr_key = len(storage)-1
	while curr_key != 0:
		graph[storage[curr_key][0][0], storage[curr_key][0][1]] = np.array([255, 0, 0])
		curr_key = storage[curr_key][2]
	cv2.imshow('Graph', graph)
	cv2.waitKey(0)

def main():
	start_time = time.time()
	ip_x = int(input("Enter initial x coordinate:\n"))
	ip_y = int(input("Enter initial y coordinate:\n"))
	g_x = int(input("Enter goal x coordinate:\n"))
	g_y = int(input("Enter goal y coordinate:\n"))
	initial = [ip_y, ip_x]
	goal = [g_y, g_x]
	storage, val, explored = dijkstra(initial, goal)
	if val == True:
		animate(storage, explored)
	end_time = time.time()
	print("Total time elapsed: ", end_time-start_time)


if __name__ == '__main__':
	main()