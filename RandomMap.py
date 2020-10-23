#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/8/19 16:31
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : RandomMap.py
@Software: PyCharm
"""

# import numpy as np
from PathFinder import PathFinder


class RandomMap:
    def __init__(self, size):
        self.obstacle_point = []
        self.size = size
        # self.obstacle = size // 2
        self.GenerateObstacle()

    def GenerateObstacle(self):
        self.obstacle_point.append(PathFinder.Point(self.size // 2, self.size // 2))
        self.obstacle_point.append(PathFinder.Point(self.size // 2, self.size // 2 - 1))

        # Generate an obstacle in the middle
        for i in range(self.size // 2 - self.size // 3, self.size // 2):
            self.obstacle_point.append(PathFinder.Point(i, self.size - i))
            self.obstacle_point.append(PathFinder.Point(i, self.size - i - 1))
            self.obstacle_point.append(PathFinder.Point(self.size - i, i))
            self.obstacle_point.append(PathFinder.Point(self.size - i, i - 1))

        # for i in range(self.obstacle - 1):
        #     x = np.random.randint(0, self.size)
        #     y = np.random.randint(0, self.size)
        #     self.obstacle_point.append(a_star.Point(x, y))
        #
        #     if np.random.rand() > 0.5:
        #         for j in range(self.size // 4):
        #             self.obstacle_point.append(a_star.Point(x, y + j))
        #             pass
        #     else:
        #         for j in range(self.size // 4):
        #             self.obstacle_point.append(a_star.Point(x + j, y))
        #             pass

    def IsObstacle(self, point):
        for p in self.obstacle_point:
            if point == p:
                return True
        return False
