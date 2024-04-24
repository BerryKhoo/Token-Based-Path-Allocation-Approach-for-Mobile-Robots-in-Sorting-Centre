import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from matplotlib.image import imread
import matplotlib.patches as mpatches
import cProfile
import pstats

# Start the profiler
profiler = cProfile.Profile()
profiler.enable()

## Plotting a Grid Layout for Robots to move
"""Nodes Label
   intersection, pickup, dropoff, charging, left, right, up, down
"""
fig, ax = plt.subplots()
grid_layout = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,0], #Pickup
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,0], #Pickup
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,0], #Pickup
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,0], #Charging
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,0], #Charging
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,5,5,5,5,25,35,0],
[0,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,4,4,4,4,24,34,0],
[0,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,8,8,8,8,2,3,0], #Dropoff
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,0], #Charging
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,0], #Charging
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,9,9,9,9,2,3,0], #Charging
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,0], #Pickup
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,0], #Pickup
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,7,2,3,0], #Pickup
[0,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,5,25,35,0],
[0,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,4,24,34,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

print(len(grid_layout[0]))
class TokenManager:
    def __init__(self, grid_layout):
        self.token_map = {(y, x): True for y, row in enumerate(grid_layout) for x, _ in enumerate(row)}
        self.reserved_cells = {}  # New dict to track cells reserved by robots
        self.occupancy_map = {}  # Track occupancy of special cells

    def request_token(self, robot_id, position):
        # Check if the cell is already reserved by another robot
        if position in self.reserved_cells and self.reserved_cells[position] != robot_id:
            return False  # The cell is reserved by another robot
        # Mark the cell as reserved for this robot
        self.reserved_cells[position] = robot_id
        # Mark special cells as occupied
        if position in [tuple(loc) for loc in charging + pickup + dropoff]:
            self.occupancy_map[position] = robot_id
        return True

    def release_token(self, robot_id, position):
        # Release the reservation and token if the robot moves into the reserved cell
        if position in self.reserved_cells and self.reserved_cells[position] == robot_id:
            del self.reserved_cells[position]  # Release the reservation
            self.token_map[position] = True  # Make the token available again
            if position in self.occupancy_map:
                self.occupancy_map[position] = None  # Mark special cell as unoccupied

    def pass_token(self, from_robot_id, to_robot_id, position):
        # Directly pass the token from one robot to another if applicable
        if position in self.reserved_cells and self.reserved_cells[position] == from_robot_id:
            self.reserved_cells[position] = to_robot_id
            if position in self.occupancy_map:
                self.occupancy_map[position] = to_robot_id
            return True
        return False

    def has_token(self, position):
        # Check if the cell is not reserved by any robot
        return position not in self.reserved_cells

    def cells_without_tokens(self):
        # List cells that are not reserved
        return [position for position in self.token_map.keys() if position not in self.reserved_cells]


token_manager = TokenManager(grid_layout)

# Draw the graph
Layout = nx.grid_2d_graph(len(grid_layout[0]), len(grid_layout))
pos = {(y, x): (x, -y) for y, x in Layout.nodes}  # Positioning nodes

### SINCE THE GRAPH IS DRAW IN A WAY OF (x, -y), thus at here we are assuming y as row and x as column

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
24. Up Left
25. Up Right
34. Down Left
35. Down Right
"""
startloc = []
pickup = []
dropoff = []
charging = []
def find_loc(grid):
    for row_idx, row in enumerate(grid_layout):
        for col_idx, value in enumerate(row):
            if value in [2,3,4,5,24,25,34,35]: # Random location on start (On the road)
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


def draw_static_layout():
    global fig, ax  # Define these as global if you need to access them outside this function
    fig, ax = plt.subplots()

    value_to_color = {
        0: 'black', 1: 'black', 2: 'none', 3: 'none',
        4: 'none', 5: 'none', 7: 'lime',
        8: 'teal', 9: 'gold', 24: 'grey', 25: 'grey', 34: 'grey', 35: 'grey'
    }
    node_colors = [value_to_color[val] for row in grid_layout for val in row]

    assert len(node_colors) == len(Layout.nodes)

    nx.draw(Layout, pos, node_size=10, node_color=node_colors, node_shape='s', font_size=8, font_color='black')

    # Drawing arrows or any other static elements
    arrow_data = {
        2: ('navy', 0, 0.1), 3: ('turquoise', 0, -0.1),
        4: ('coral', -0.1, 0), 5: ('violet', 0.1, 0),
    }
    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val in arrow_data:
                color, dx, dy = arrow_data[val]
                center_x, center_y = pos[(y, x)]
                ax.add_patch(
                    mpatches.FancyArrow(center_x, center_y, dx, dy, width=0.45, head_width=0.4, head_length=0.4,
                                        color=color))

    ax.set_aspect('equal')
    return fig, ax

def update_robot_positions(position):
    ax.clear()
    # Draw only robot positions as dynamic elements
    nx.draw_networkx_nodes(Layout, pos, nodelist=position, node_color='blue', node_size=70, node_shape='o')

    plt.gca().set_aspect('equal')
    plt.draw()  # Update the plot with the new robot positions


robot_artists = {}
def initialize_robots(positions):
    global robot_artists
    for robot_id, position in enumerate(positions):
        # Convert your position to coordinates, e.g., using your 'pos' mapping if using NetworkX
        x, y = position  # Assuming position is already in the form of coordinates
        robot_artists[robot_id] = ax.add_patch(patches.Circle((y, -x), 0.5, color='blue'))  # Adjust size and color as needed


## Creating Robots that will be moving on the grid
""" Assumptions of Robots:
    1. Battery Health of Robots (Needs to be initalized)
    2. Moves with the directions that is set on the grid
    3. Speed and Acceleration (TBC)
"""

# Function to create a graph from the grid layout
def robot_movement_graph(grid):

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
    24. Up Left
    25. Up Right
    34. Down Left
    35. Down Right
    """

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
                        if grid[y][x] in [7, 8, 9] and adj_val in [2, 3, 4, 5, 6, 24, 25, 34, 35]:
                            G.add_edge(node, (ey, ex), weight=1)


            if grid[y][x] in [1, 2, 3, 4, 5, 24, 25, 34, 35]:

                if grid[y][x] == 2:
                    G.add_edge(node, (y-1, x), weight=1) # UP
                elif grid[y][x] == 3:
                    G.add_edge(node, (y+1, x), weight=1) # DOWN
                elif grid[y][x] == 4:
                    G.add_edge(node, (y, x-1), weight=1) # LEFT
                elif grid[y][x] == 5:
                    G.add_edge(node, (y, x+1), weight=1) # RIGHT
                elif grid[y][x] == 24:
                    G.add_edge(node, (y-1, x), weight=1)
                    G.add_edge(node, (y, x-1), weight=1)   # UP, LEFT
                elif grid[y][x] == 25:
                    G.add_edge(node, (y-1, x), weight=1)
                    G.add_edge(node, (y, x+1), weight=1) # UP, RIGHT
                elif grid[y][x] == 34:
                    G.add_edge(node, (y + 1, x), weight=1)  # DOWN
                    G.add_edge(node, (y, x-1), weight=1) # DOWN, LEFT
                elif grid[y][x] == 35:
                    G.add_edge(node, (y + 1, x), weight=1)  # DOWN
                    G.add_edge(node, (y, x+1), weight=1) # DOWN, RIGHT

                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions: UP, DOWN, LEFT, RIGHT
                    ey, ex = y + dy, x + dx
                    if 0 <= ey < rows and 0 <= ex < cols:  # Check bounds
                        adj_val = grid[ey][ex]

                        # Add edges for destination nodes
                        if grid[y][x] in [2, 3, 4, 5, 24, 25, 34, 35] and adj_val in [7, 8, 9]:
                            G.add_edge(node, (ey, ex), weight=100)


    return G
## Path Updates

# To find out the path for robots to travel via dijkstra
# Assuming where their first task will be pickup.

robotamount = 1300
robotcurloc = [] # current location of the robots
robotpath = [] # Pathway of Robots to move
robot_destination = [] # Coordinates of the tasks
robotstate = {} # Determine if the robot is doing pickup(False) or dropoff(True)
prevstate = {} # Previous robot state
token_amount = [0] * robotamount

CHARGING_THRESHOLD = 30  # Battery threshold to go charging
CHARGE_AMOUNT_PER_FRAME = 5  # Amount of battery charged per frame at the charging station
battery = [random.randint(10,100) for _ in range(robotamount)]

def initial_robot_path():
    global robotpath
    global robot_destination
    global robotstate
    global robotamount
    global prevstate
    Grid = robot_movement_graph(grid_layout)
    for i in range(robotamount):
        start_point = random.choice(startloc)
        robotcurloc.append(start_point)
        startloc.remove(start_point)
        if battery[i] < CHARGING_THRESHOLD:
            go_point = random.choice(charging)
            try:
                path = nx.dijkstra_path(Grid, start_point, go_point, weight='weight')
                robotpath.append(path)

                # Update robot_tasks mapping
                robot_destination.append((start_point, go_point))
                robotstate[i] = "Charging"

            except nx.NetworkXNoPath:
                print(f"No starting path found from {start_point} to {go_point}")
        else:
            go_point = random.choice(pickup)

            try:
                path = nx.dijkstra_path(Grid, start_point, go_point, weight='weight')
                robotpath.append(path)

                # Update robot_tasks mapping
                robot_destination.append((start_point, go_point))
                robotstate[i] = "Pickup"

            except nx.NetworkXNoPath:
                print(f"No starting path found from {start_point} to {go_point}")

initial_robot_path()
# Update the path
def robot_path_update(robotid, new_start, new_end):

    Grid = robot_movement_graph(grid_layout)
    if new_start in Grid and new_end in Grid:
        try:
            path = nx.dijkstra_path(Grid, new_start, new_end, weight='weight')
            robot_destination[robotid] = (new_start, new_end)
            robotpath[robotid] = path

        except nx.NetworkXNoPath:
            print(f"No path found from {new_start} to {new_end}")

    else:
        print(f"Invalid path update for Robot ID {robotid}: {new_start} to {new_end}")



## Task Allocator

def allocator(robotid, currentpos):

    new_start = currentpos

    if battery[robotid] < CHARGING_THRESHOLD and robotstate[robotid] == "Pickup": # Persist to finish job even low battery
        new_end = random.choice(dropoff)
        update_robot_state(robotid)
        robotstate[robotid] = "Dropoff"
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end

    elif battery[robotid] < CHARGING_THRESHOLD and robotstate[robotid] == "Dropoff": # Only can go charge after dropoff
        update_throughput(robotid)
        update_robot_state(robotid)
        new_end = random.choice(charging)
        robotstate[robotid] = "Charging"
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end

    elif battery[robotid] < 90 and robotstate[robotid] == "Charging": # Continue Pickup
        new_end = random.choice(pickup)
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
        update_robot_state(robotid)
        robotstate[robotid] = "Pickup"
        robot_destination[robotid] = {new_start, new_end}
        return new_start, new_end


    else:
        if robotstate.get(robotid) == "Pickup":
            new_end = random.choice(dropoff)
            update_robot_state(robotid)
            robotstate[robotid] = "Dropoff"
            robot_destination[robotid] = {new_start, new_end}
            return new_start, new_end

        elif robotstate.get(robotid) == "Dropoff":
            update_throughput(robotid)
            new_end = random.choice(pickup)
            update_robot_state(robotid)
            robotstate[robotid] = "Pickup"
            robot_destination[robotid] = {new_start, new_end}
            return new_start, new_end

        print(robotid, "Not being allocated at the state of", robotstate[robotid], "at", currentpos)


def update_robot_state(robotid):
    # Update the previous state before changing the current state
    prevstate[robotid] = robotstate.get(robotid, None)


throughput = 0
def update_throughput(robotid):

    global throughput
    if robotcurloc[robotid] in dropoff:
        throughput += 1
        print(f"Robot {robotid} completed a cycle. Total throughput: {throughput}")


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

"""
robot request for token first, success token request store in a list (its coordinate), the path robot can move is according to the stored list,
request until the path is empty. If already have the grid token, keep (skip the turn)
if the request list is empty, cannot move, stay at same place

"""


def is_robot_behind(current_robot_id, current_position, robot_directions, robot_positions):
    """
    Check if there is a robot directly behind the current robot.

    :param current_robot_id: The ID of the current robot.
    :param current_position: The current position of the robot as a tuple (x, y).
    :param robot_directions: A dictionary mapping robot IDs to their current direction.
    :param robot_positions: A dictionary mapping robot IDs to their current positions.
    :return: Boolean indicating if there is a robot behind.
    """
    # Define the reverse direction vectors
    reverse_directions = {
        'up': (0, 1),  # Assuming 'up' is negative y-direction
        'down': (0, -1),
        'left': (1, 0),  # Assuming 'left' is negative x-direction
        'right': (-1, 0),
        # Add more directions if needed
    }

    # Get the reverse direction of the current robot
    if robot_directions[current_robot_id] in reverse_directions:
        reverse_dx, reverse_dy = reverse_directions[robot_directions[current_robot_id]]
        # Calculate the position behind the current robot
        behind_position = (current_position[0] + reverse_dx, current_position[1] + reverse_dy)

        # Check if any robot is at the behind position
        for robot_id, position in robot_positions.items():
            if robot_id != current_robot_id and position == behind_position:
                return True

    return False


def get_robot_directions(robot_paths):
    """
    Infer the directions of robots based on their paths.
    :param robot_paths: A list of paths for each robot where each path is a list of (x, y) tuples.
    :return: A dictionary with robot_ids as keys and direction strings as values.
    """
    directions = {}
    for robot_id, path in enumerate(robot_paths):
        if len(path) >= 2:
            # Compare the current position with the next position to determine direction
            current_pos = path[-2]
            next_pos = path[-1]
            dx = next_pos[0] - current_pos[0]
            dy = next_pos[1] - current_pos[1]

            if dx > 0:
                directions[robot_id] = 'right'
            elif dx < 0:
                directions[robot_id] = 'left'
            elif dy > 0:
                directions[robot_id] = 'up'  # Assuming positive y-direction is 'up' in your grid
            elif dy < 0:
                directions[robot_id] = 'down'
            else:
                directions[robot_id] = 'stationary'  # No movement
        else:
            # If there's no next position, the robot is stationary or its direction is unknown
            directions[robot_id] = 'stationary'
    return directions

def get_behind_robot_id(current_robotid, current_position):
    intersection_candidates = []
    other_candidates = []

    for robotid, path in enumerate(robotpath):
        if robotid != current_robotid and path:  # Ensure not checking the same robot and the path is not empty
            robot_next_position = path[0]  # Assuming the next position to move to is the first in the list
            if current_position == robot_next_position:
                # Determine the value of the robot's current grid cell
                current_robot_grid_value = grid_layout[robotcurloc[robotid][0]][robotcurloc[robotid][1]]
                if current_robot_grid_value in [24, 25, 34, 35]:
                    # This robot is on an intersection grid, prioritize
                    intersection_candidates.append(robotid)
                else:
                    # Not on an intersection, add to other candidates
                    other_candidates.append(robotid)

    # Prioritize robots on intersection grids, if any
    if intersection_candidates:
        return intersection_candidates[0]
    elif other_candidates:
        return other_candidates[0]

    return None



global framecount
collison_cp = [None] * len(robotpath) #Only for checking collision
previous_positions = [None] * len(robotpath)
framecount = 0
acquiredpos = {robotid: [] for robotid in range(len(robotpath))}
robotelements = []
def update(framecount):

    global previous_positions
    global collison_cp
    global acquiredpos

    for element in robotelements:
        element.remove()
    robotelements.clear()

    print("Global frame:", framecount)

    # Token Reservation
    for robotid, path in enumerate(robotpath):
        tokenamount = min(3, len(path))

        for position in path[:tokenamount]:
            if len(acquiredpos[robotid]) < tokenamount:
                if token_manager.request_token(robotid, position):
                    if position not in acquiredpos.get(robotid, []):
                        acquiredpos[robotid].append(position)
                        robotpath[robotid].pop(0)
                else:
                    break

    # Moving Robots
    for robotid in range(len(acquiredpos)):
        if acquiredpos[robotid]:
            currentloc = robotcurloc[robotid]
            previous_positions[robotid] = currentloc

            nextpos = acquiredpos[robotid].pop(0)
            robotcurloc[robotid] = nextpos

            behindrobotid = get_behind_robot_id(robotid, currentloc)
            if behindrobotid is not None:
                token_manager.pass_token(robotid, behindrobotid, currentloc)
                if currentloc not in acquiredpos.get(behindrobotid, []):
                    acquiredpos[behindrobotid].append(currentloc)
                    robotpath[behindrobotid].pop(0)
            else:
                 token_manager.release_token(robotid, currentloc)
        else:
            currentloc = robotcurloc[robotid]
            previous_positions[robotid] = currentloc
            robotcurloc[robotid] = currentloc

            behindrobotid = get_behind_robot_id(robotid, currentloc)
            if behindrobotid is not None:
                token_manager.pass_token(robotid, behindrobotid, currentloc)
                if currentloc not in acquiredpos.get(behindrobotid, []):
                    acquiredpos[behindrobotid].append(currentloc)
                    robotpath[behindrobotid].pop(0)



    # print(acquiredpos)
    # print(robotcurloc)
    # print(robotpath)


    for robotid, _ in enumerate(robotcurloc):
        if robotstate[robotid] == "Charging" and robotcurloc[robotid] in charging:
            if battery[robotid] < 90:
                battery[robotid] += CHARGE_AMOUNT_PER_FRAME
            elif battery[robotid] >= 90:
                # Handle robot finishing charging
                new_start, new_end = allocator(robotid, robotcurloc[robotid])
                robot_path_update(robotid, new_start, new_end)
                battery[robotid] -= random.randint(1, 3)
                # print(f"New task assigned to Robot ID {robotid}: {new_start} to {new_end}")

        elif robotcurloc[robotid] == robot_destination[robotid][1]:
            new_start, new_end = allocator(robotid, robotcurloc[robotid])
            robot_path_update(robotid, new_start, new_end)
            battery[robotid] -= random.randint(1, 3)
            robotcurloc[robotid] = new_start  # Add the start of the new path to current position
            # print(f"New task assigned to Robot ID {robotid}: {new_start} to {new_end}")

    # Check for collisions
    collisions(collison_cp, previous_positions)


    for robot_id, new_position in enumerate(robotcurloc):
        x, y = new_position  # Convert as needed
        robot_artists[robot_id].set_center((y, -x))  # Update the artist position directly

    if framecount == 5000:
        print(f"Stopping at frame {framecount}. Total Throughput: {throughput}")
        animation.event_source.stop()
        yes = input("Continue?(p): ")
        if yes == 'p':
            animation.event_source.start()

    return list(robot_artists.values())  # Return artists as a sequence for the animation framework

is_paused = False

def toggle_pause(event):
    global is_paused
    if event.key == 'p':  # Choose an appropriate key for pausing/resuming
        if is_paused:
            animation.event_source.start()  # Resume animation
        else:
            animation.event_source.stop()  # Pause animation
        is_paused = not is_paused

maxpath = max(len(path) for path in robotpath)
fig, ax = draw_static_layout()
initialize_robots(robotcurloc)
animation = FuncAnimation(fig, update, frames=9999, interval=1000, blit=True)
fig.canvas.mpl_connect('key_press_event', toggle_pause)
plt.show()

# Stop the profiler
profiler.disable()

# Create a Stats object from the profiler and sort the results by cumulative time
stats = pstats.Stats(profiler).sort_stats('cumulative')

# Dump the stats to a file
with open('profiler_stats.txt', 'w') as file:
    stats.stream = file
    stats.print_stats()
