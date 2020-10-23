#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/8/19 16:44
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : main.py
@Software: PyCharm
"""

import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from PathFinder import RandomMap, PathFinder

plt.figure(figsize=(6, 6))

graph = RandomMap.RandomMap(size=50)

ax = plt.gca()
ax.set_xlim([0, graph.size])
ax.set_ylim([0, graph.size])

for i in range(graph.size):
    for j in range(graph.size):
        if graph.IsObstacle(PathFinder.Point(i, j)):
            rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
        else:
            rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
            ax.add_patch(rec)

rec = Rectangle((0, 0), width=1, height=1, facecolor='b')
ax.add_patch(rec)

rec = Rectangle((graph.size - 1, graph.size - 1), width=1, height=1, facecolor='r')
ax.add_patch(rec)

plt.axis('equal')
plt.axis('off')
plt.tight_layout()
# plt.show()


# print("Dijkstra: ")
# Dijkstra = PathFinder.FindPath(graph, heuristic=False)
# Dijkstra.Run(ax, plt)
print("A star: ")
aStar = PathFinder.FindPath(graph)
aStar.Run(ax, plt)
print("====================================================================")

plt.show()
