import sys
import random

import numpy as np
import os
import cv2 as cv
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.animation import FuncAnimation
from matplotlib.image import imread
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib.patches as mpatches
import time

## Plotting a Grid Layout for Robots to move
"""Nodes Label
   intersection, pickup, dropoff, charging, left, right, up, down
"""
fig, ax = plt.subplots()
grid_layout = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,0],
[0,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,0],
[0,2,3,9,9,9,6,6,9,9,9,6,6,9,9,9,6,6,9,9,9,6,6,9,9,9,2,3,0],
[0,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,0], # 5
[0,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,0],
[0,2,3,1,7,7,6,6,7,7,7,6,6,7,7,7,6,6,7,7,7,6,6,7,7,1,2,3,0],
[0,2,3,7,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,3,7,2,3,0],
[0,2,3,7,2,3,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,3,7,2,3,0],
[0,6,6,6,2,3,6,6,8,8,8,6,6,8,8,8,6,6,8,8,8,6,6,2,3,6,6,6,0], # 10
[0,6,6,6,2,3,6,6,8,8,8,6,6,8,8,8,6,6,8,8,8,6,6,2,3,6,6,6,0],
[0,2,3,7,2,3,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,2,3,7,2,3,0],
[0,2,3,7,2,3,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,2,3,7,2,3,0],
[0,6,6,6,2,3,6,6,8,8,8,6,6,8,8,8,6,6,8,8,8,6,6,2,3,6,6,6,0],
[0,6,6,6,2,3,6,6,8,8,8,6,6,8,8,8,6,6,8,8,8,6,6,2,3,6,6,6,0], # 15
[0,2,3,7,2,3,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,2,3,7,2,3,0],
[0,2,3,7,2,3,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,2,3,7,2,3,0],
[0,6,6,6,2,3,6,6,8,8,8,6,6,8,8,8,6,6,8,8,8,6,6,2,3,6,6,6,0],
[0,6,6,6,2,3,6,6,8,8,8,6,6,8,8,8,6,6,8,8,8,6,6,2,3,6,6,6,0],
[0,2,3,7,2,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,2,3,7,2,3,0], # 20
[0,2,3,7,2,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,7,2,3,0],
[0,2,3,1,7,7,6,6,7,7,7,6,6,7,7,7,6,6,7,7,7,6,6,7,7,1,2,3,0],
[0,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,0],
[0,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,0],
[0,2,3,9,9,9,6,6,9,9,9,6,6,9,9,9,6,6,9,9,9,6,6,9,9,9,2,3,0], # 25
[0,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,4,4,4,6,6,0],
[0,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,5,5,5,6,6,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 29
]

class TokenManager:
    def __init__(self, grid_layout):
        self.token_map = {(y, x): True for y, row in enumerate(grid_layout) for x, _ in enumerate(row)}

    def request_token(self, position):
        if self.token_map.get(position, False):
            self.token_map[position] = False
            return True
        return False

    def release_token(self, position):
        self.token_map[position] = True

token_manager = TokenManager(grid_layout)

# Draw the graph
Layout = nx.grid_2d_graph(len(grid_layout), len(grid_layout[0]))
pos = {(y, x): (x, -y) for x, y in Layout.nodes}  # Positioning nodes

print(len(grid_layout))
print(len(grid_layout[0]))
# To find the desired position on the graph
"""
0. Border
1. Walls
2. Only Up
3. Only Down
4. Only Left
5. Only Right
6. Intersection (Able to move freely)
7. Pick Up
8. Drop Off
9. Charging
"""
startloc = []
pickup = []
dropoff = []
charging = []
def find_loc(grid):
    for row_idx, row in enumerate(grid_layout):
        for col_idx, value in enumerate(row):
            if value in [2,3,4,5,6]: # Random location on start (On the road)
                # pass
                # loc = row_idx, col_idx;
                startloc.append((row_idx, col_idx))

            elif value == 7:
                # pass
                # loc = row_idx, col_idx;
                pickup.append((row_idx, col_idx))

            elif value == 8:
                # pass
                # loc = row_idx, col_idx;
                dropoff.append((row_idx, col_idx))

            elif value == 9:
                # pass
                # loc = row_idx, col_idx;
                charging.append((row_idx, col_idx))



find_loc(grid_layout)

#global robotid
#robotid = {i: startloc[i] for i in range(len(startloc))}
#print(robotid)

# Define node colors based on the grid_layout
def layoutbg():
    fig, ax = plt.subplots()
    value_to_color = {
        0: 'black',
        1: 'brown',
        2: 'none',
        3: 'orange',
        4: 'yellow',
        5: 'green',
        6: 'purple',
        7: 'grey',
        8: 'white',
        9: 'cyan'
    }

    # Plotting out the graph
    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val in value_to_color:  # Check if the value should be drawn
                color = value_to_color[val]
                nx.draw_networkx_nodes(Layout, pos, nodelist=[(y, x)], node_color=color, node_size=40, node_shape='s')

    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val == 2:
                center_x, center_y = pos[(y, x)]
                arrow = mpatches.FancyArrow(center_x, center_y, 0, 0.1, width=0.5, head_width=0.4, head_length=0.4,
                                            color='green')
                ax.add_patch(arrow)

    plt.axis('off')
    plt.grid(False)
    plt.gca().set_aspect('equal')
    plt.savefig('background.png', bbox_inches='tight')
    plt.close(fig)

layoutbg()

background = imread('background.png')

def graph(position):

    node_colors = []

    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val == 0:
                node_colors.append('black')
            elif val == 1:
                node_colors.append('black')
            elif val == 2:
                node_colors.append('none')
            elif val == 3:
                node_colors.append('none')
            elif val == 4:
                node_colors.append('none')
            elif val == 5:
                node_colors.append('none')
            elif val == 6:
                node_colors.append('grey')
            elif val == 7:
                node_colors.append('lime')
            elif val == 8:
                node_colors.append('teal')
            elif val == 9:
                node_colors.append('gold')

    # Plotting out the graph
    assert len(node_colors) == len(Layout.nodes)

    ## Layout
    nx.draw(Layout, pos, node_size=120, node_color=node_colors, node_shape='s', font_size=8, font_color='black')

    for i in position:
        nx.draw_networkx_nodes(Layout, pos, nodelist=[i], node_color='blue', node_size=70, node_shape='o')

    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val == 2:
                center_x, center_y = pos[(y, x)]
                arrow = mpatches.FancyArrow(center_x, center_y, 0, 0.1, width=0.45, head_width=0.4, head_length=0.4,
                                            color='navy')
                ax.add_patch(arrow)

            elif val == 3:
                center_x, center_y = pos[(y, x)]
                arrow = mpatches.FancyArrow(center_x, center_y, 0, -0.1, width=0.45, head_width=0.4, head_length=0.4,
                                            color='turquoise')
                ax.add_patch(arrow)

            elif val == 4:
                center_x, center_y = pos[(y, x)]
                arrow = mpatches.FancyArrow(center_x, center_y, -0.1, 0, width=0.45, head_width=0.4, head_length=0.4,
                                            color='coral')
                ax.add_patch(arrow)

            elif val == 5:
                center_x, center_y = pos[(y, x)]
                arrow = mpatches.FancyArrow(center_x, center_y, 0.1, 0, width=0.45, head_width=0.4, head_length=0.4,
                                            color='violet')
                ax.add_patch(arrow)


    plt.gca().set_aspect('equal')  # Make the plot aspect ratio equal
    plt.show()


## Creating Robots that will be moving on the grid
""" Assumptions of Robots:
    1. Battery Health of Robots (Needs to be initalized)
    2. Moves with the directions that is set on the grid
    3. Speed and Acceleration (TBC)
"""

# Function to create a graph from the grid layout
def robot_movement_graph(grid):
    # Need to solve path finding only limited on [1-6], last node only can [7-9]

    G = nx.DiGraph()
    rows = len(grid)
    cols = len(grid[0])

    for y in range(rows):
        for x in range(cols):
            node = (y, x)
            G.add_node(node)

            if grid[y][x] in [7, 8, 9]:

                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions: UP, DOWN, LEFT, RIGHT
                    ey, ex = y + dy, x + dx
                    if 0 <= ey < rows and 0 <= ex < cols:  # Check bounds
                        adj_val = grid[ey][ex]

                        # Add edges for destination nodes
                        if grid[y][x] in [7, 8, 9] and adj_val in [2, 3, 4, 5, 6]:
                            G.add_edge(node, (ey, ex))


            if grid[y][x] in [1, 2, 3, 4, 5, 6]:

                if grid[y][x] == 2:
                    G.add_edge(node, (y-1, x)) # UP
                elif grid[y][x] == 3:
                    G.add_edge(node, (y+1, x)) # DOWN
                elif grid[y][x] == 4:
                    G.add_edge(node, (y, x-1)) # LEFT
                elif grid[y][x] == 5:
                    G.add_edge(node, (y, x+1)) # RIGHT
                elif grid[y][x] in [1, 6] :  # Free movement
                    G.add_edge(node, (y - 1, x))
                    G.add_edge(node, (y + 1, x))
                    G.add_edge(node, (y, x - 1))
                    G.add_edge(node, (y, x + 1))

                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions: UP, DOWN, LEFT, RIGHT
                    ey, ex = y + dy, x + dx
                    if 0 <= ey < rows and 0 <= ex < cols:  # Check bounds
                        adj_val = grid[ey][ex]

                        # Add edges for destination nodes
                        if grid[y][x] in [2, 3, 4, 5, 6] and adj_val in [7, 8, 9]:
                            G.add_edge(node, (ey, ex))

    return G
## Path Updates

# To find out the path for robots to travel via dijkstra
# Assuming where their first task will be pickup.
global robotpath
global robot_destination
global robotstate
global robotamount
robotamount = 40
robotpath = [] # Pathway of Robots to move
robot_destination = [] # Coordinates of the tasks
robotstate = {} # Determine if the robot is doing pickup(False) or dropoff(True)

CHARGING_THRESHOLD = 30  # Battery threshold to go charging
CHARGE_AMOUNT_PER_FRAME = 5  # Amount of battery charged per frame at the charging station
battery = [random.randint(10,100) for _ in range(robotamount)]
print(battery)

def initial_robot_path():
    Grid = robot_movement_graph(grid_layout)
    for i in range(robotamount):
        start_point = random.choice(startloc)
        startloc.remove(start_point)
        if battery[i] < CHARGING_THRESHOLD:
            go_point = random.choice(charging)
            try:
                path = nx.dijkstra_path(Grid, start_point, go_point)
                robotpath.append(path)

                # Update robot_tasks mapping
                robot_destination.append((start_point, go_point))
                robotstate[i] = "Charging"

            except nx.NetworkXNoPath:
                print(f"No starting path found from {start_point} to {go_point}")
        else:
            go_point = random.choice(pickup)

            try:
                path = nx.dijkstra_path(Grid, start_point, go_point)
                robotpath.append(path)

                # Update robot_tasks mapping
                robot_destination.append((start_point, go_point))
                robotstate[i] = "Pickup"

            except nx.NetworkXNoPath:
                print(f"No starting path found from {start_point} to {go_point}")




# Update the path
def robot_path_update(robotid, new_start, new_end):

    Grid = robot_movement_graph(grid_layout)
    if new_start in Grid and new_end in Grid:
        try:
            path = nx.dijkstra_path(Grid, new_start, new_end)
            robot_destination[robotid] = (new_start, new_end)
            robotpath[robotid] = path

        except nx.NetworkXNoPath:
            print(f"No path found from {new_start} to {new_end}")

    else:
        print(f"Invalid path update for Robot ID {robotid}: {new_start} to {new_end}")

initial_robot_path()
print(robotstate)

## Task Allocator

def allocator(robotid, currentpos):
    new_start = currentpos

    if battery[robotid] < CHARGING_THRESHOLD and robotstate[robotid] == "Pickup": # Only can go charge after dropoff
        new_end = random.choice(charging)
        robotstate[robotid] = "Charging"
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end

    elif battery[robotid] < CHARGING_THRESHOLD and robotstate[robotid] == "Dropoff": # Persist to finish job even low battery
        new_end = random.choice(dropoff)
        robotstate[robotid] = "Pickup"
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end

    elif battery[robotid] < 90 and robotstate[robotid] == "Charging" and currentpos in charging:
        if currentpos in charging:
            charging.remove(currentpos)
        new_end = currentpos
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end

    elif battery[robotid] >= 90 and robotstate[robotid] == "Charging":
        if currentpos not in charging:
            charging.append(currentpos)
        new_end = random.choice(pickup)
        robotstate[robotid] = "Pickup"
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end

    else:
        if robotstate[robotid] != "Charging":
            if robotstate.get(robotid) == "Pickup":
                new_end = random.choice(dropoff)
                robotstate[robotid] = "Dropoff"
                robot_destination[robotid] = {new_start, new_end}
                return new_start, new_end

            elif robotstate.get(robotid) == "Dropoff":
                new_end = random.choice(pickup)
                robotstate[robotid] = "Pickup"
                robot_destination[robotid] = {new_start, new_end}
                return new_start, new_end


# Check Collision by taking the current pos
def collisions(curpos, prevpos):
    collision_nodes = set()
    collision_crash = set()

    # Number of robots
    num_robots = len(curpos)

    # Check for robots occupying the same grid cell
    for i in range(num_robots):
        for j in range(i+1, num_robots):
            if curpos[i] == curpos[j]:
                collision_nodes.add(curpos[i])

    # Check for robots swapping places
    for i in range(num_robots):
        for j in range(num_robots):
            if i != j:
                if curpos[i] == prevpos[j] and prevpos[i] == curpos[j]:
                    collision_crash.add((curpos[i], prevpos[i]))

    #Report collisions
    if collision_nodes:
        print(f"Collision detected at nodes: {collision_nodes}")
    if collision_crash:
        print(f"Collision crash at nodes: {collision_crash}")

    return collision_nodes

# Token based concept change to : (Need to further solve)
"""
robot request for token first, success token request store in a list (its coordinate), the path robot can move is according to the stored list,
request until the path is empty. If already have the grid token, keep (skip the turn)
if the request list is empty, cannot move, stay at same place

"""
global framecount
global previous_positions
previous_positions = [None] * len(robotpath)
framecount = 0
def update(framecount):
    ax.clear()
    print("Global frame:", framecount)

    currentpos = []
  # Robots current position

    for robotid, path in enumerate(robotpath):

        if path:  # Check if the path is not empty

            token_acquired = False
            positions_to_check = min(4, len(path)) # Reserve at least 4 if the path is more than 4, else the length of the path

            # print(robotpath)

            for i in range(positions_to_check):
                if token_manager.request_token(path[i]):
                    # If token received for this position, move the robot
                    for j in range(i + 1):
                        current_position = path.pop(0)
                    currentpos.append(current_position)

                    # Release token for the previous position if it exists
                    if previous_positions[robotid] is not None:
                        token_manager.release_token(previous_positions[robotid])

                    # Update previous position
                    previous_positions[robotid] = current_position
                    token_acquired = True
                    break

            if not token_acquired:
                # If no tokens were acquired, stay in the current position
                if previous_positions[robotid] is not None:
                    currentpos.append(previous_positions[robotid])

                previous_positions[robotid] = previous_positions[robotid]

        elif robotstate[robotid] == "Charging":
            current_position = robot_destination[robotid][1]  # Assuming this is the charging position
            if current_position in charging and battery[robotid] < 90:
                battery[robotid] += CHARGE_AMOUNT_PER_FRAME
            elif current_position in charging and battery[robotid] >= 90:
                # Handle robot finishing charging
                new_start, new_end = allocator(robotid, current_position)
                robot_path_update(robotid, new_start, new_end)
                battery[robotid] -= random.randint(1, 3)
                print(f"New task assigned to Robot ID {robotid}: {new_start} to {new_end}")
            else:
                break

            currentpos.append(current_position)
        else:
            new_start, new_end = allocator(robotid, robot_destination[robotid][1])
            robot_path_update(robotid, new_start, new_end)
            battery[robotid] -= random.randint(1,3)
            currentpos.append(new_start)  # Add the start of the new path to current position
            print(f"New task assigned to Robot ID {robotid}: {new_start} to {new_end}")

            if previous_positions[robotid] is not None:
                token_manager.release_token(previous_positions[robotid])

    for i, pos in enumerate(currentpos):
        if previous_positions[i] is None:
            previous_positions[i] = pos
        else:
            previous_positions[i] = pos


    # Check for collisions
    collisions(currentpos, previous_positions)

    graph(currentpos)
    ax.set_aspect('equal')

print(robot_destination)
maxpath = max(len(path) for path in robotpath)
animation = FuncAnimation(fig, update, frames=9999, interval=300)
plt.show()



# Task Distribution



