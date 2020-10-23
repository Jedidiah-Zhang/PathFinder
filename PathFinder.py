#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/8/19 16:36
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : PathFinder.py
@Software: PyCharm
"""

import sys
import time

import numpy as np

from matplotlib.patches import Rectangle
from functools import total_ordering


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@total_ordering
class Node:
    heuristic = True

    def __init__(self, point, g=sys.maxsize, h=sys.maxsize):
        self.point = point
        self.parent = None
        self.g = g
        self.h = h

    def HeuristicCost(self, end_node):
        if Node.heuristic:
            dx = abs(end_node.point.x - self.point.x)
            dy = abs(end_node.point.y - self.point.y)
            self.h = dx + dy + (np.sqrt(2) - 2) * min(dx, dy)
        else:
            self.h = 0

    def setBaseCost(self, g):
        self.g = g

    def setParent(self, node):
        self.parent = node

    def get_cost(self):
        return self.g + self.h

    def __eq__(self, other):
        return self.get_cost() == other.get_cost()

    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    def __repr__(self):
        return "(" + str(self.point.x+1) + ", " + str(self.point.y+1) + ")"


class FindPath:
    def __init__(self, graph, heuristic=True):
        self.graph = graph
        Node.heuristic = heuristic
        self.open_list = []  # nodes to be evaluate
        self.close_list = []  # nodes already evaluated
        self.start_node = Node(Point(0, 0), g=0)
        self.end_node = Node(Point(self.graph.size-1, self.graph.size-1), h=0)
        self.start_node.HeuristicCost(self.end_node)

    def IsInOpenList(self, point):
        for each in self.open_list:
            if point == each.point:
                return True
        return False

    def IsInCloseList(self, point):
        for each in self.close_list:
            if point == each.point:
                return True
        return False

    def GetNodeInOpenList(self, node):
        for each in self.open_list:
            if node.point == each.point:
                return each
        return node

    def GetIndexInOpenList(self, node):
        for i in range(len(self.open_list)):
            if node.point == self.open_list[i].point:
                return i
        return -1

    def UpdateOpenList(self, node):
        for i in range(len(self.open_list)):
            if self.open_list[i].point == node.point:
                self.open_list[i] = node

    @staticmethod
    def Neighbours(node):
        point = node.point
        process_points = [Point(point.x-1, point.y+1),
                          Point(point.x-1, point.y),
                          Point(point.x-1, point.y-1),
                          Point(point.x, point.y+1),
                          Point(point.x, point.y-1),
                          Point(point.x+1, point.y+1),
                          Point(point.x+1, point.y),
                          Point(point.x+1, point.y-1)]
        return [Node(i) for i in process_points]

    def IsValidPoint(self, point):
        if point.x < 0 or point.y < 0:
            return False
        if point.x >= self.graph.size or point.y >= self.graph.size:
            return False
        return not self.graph.IsObstacle(point)

    @staticmethod
    def CalcBaseCost(node, parent):
        g = parent.g
        dx = abs(parent.point.x - node.point.x)
        dy = abs(parent.point.y - node.point.y)
        g += abs(dx-dy) + min(dx, dy) * np.sqrt(2)
        return g

    def SelectNode(self):
        min_node = min(self.open_list)
        for each in self.open_list:
            if each == min_node:
                if each.g < min_node.g:
                    min_node = each
        return min_node

    def Run(self, ax, plt):
        start_time = time.time_ns()
        self.open_list.append(self.start_node)

        while True:
            if not self.open_list:
                print("No path found")
                break
            current_node = self.SelectNode()
            if current_node.point == self.end_node.point:
                return self.BuildPath(current_node, start_time, ax, plt)

            del self.open_list[self.GetIndexInOpenList(current_node)]
            self.close_list.append(current_node)
            neighbours = self.Neighbours(current_node)

            for each in neighbours:
                if self.IsValidPoint(each.point) and not self.IsInCloseList(each.point):
                    rec = Rectangle((each.point.x, each.point.y), 1, 1, color='c')
                    ax.add_patch(rec)
                    g_cost = self.CalcBaseCost(each, current_node)
                    if self.IsInOpenList(each.point):
                        each = self.GetNodeInOpenList(each)
                    each.HeuristicCost(self.end_node)
                    if g_cost + each.h < each.get_cost() or not self.IsInOpenList(each.point):
                        each.setBaseCost(g_cost)
                        each.parent = current_node
                        if not self.IsInOpenList(each.point):
                            self.open_list.append(each)

    def BuildPath(self, last, start_time, ax, plt):
        path = []
        while True:
            path.append(last)
            if last.point == self.start_node.point:
                break
            else:
                last = last.parent
        path.reverse()
        end_time = time.time_ns()
        print("Shortest Distance:", path[-1].g)
        # print("Path:", path)
        print('===== Algorithm finish in', end_time - start_time, 'nanoseconds =====')
        for p in path[1:-1]:
            if Node.heuristic:
                rec = Rectangle((p.point.x, p.point.y), 1, 1, color='g')
            else:
                rec = Rectangle((p.point.x, p.point.y), 1, 1, color='y')
            ax.add_patch(rec)
            plt.draw()

