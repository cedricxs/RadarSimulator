import numpy as np
import random
class TargetGenertor():
    __instance = None
    def getInstance():
        if TargetGenertor.__instance is not None:
            return TargetGenertor.__instance
    def __init__(self):
        TargetGenertor.__instance = self
        self.m = 0
        self.n = 0
        self.x = self.m
        self.y = self.n
        self.v_count = 2
        self.sig_magnitude = 10
    
    def generateTarget(self, Plan):
        theta = random.randint(1, 20) * np.pi / 3
        step_x = int(self.v_count * np.cos(theta))                           # 距离向每次移动步长（像素个数）
        step_y = int(self.v_count * np.sin(theta))                           # 方位向每次移动步长（像素个数）
        self.x += step_x
        self.y += step_y
        if self.x>=len(Plan) or self.x < 0:
            self.x = self.m
        if self.y>=len(Plan[0]) or self.y < 0:
            self.y = self.n
        Plan[self.x , self.y] += self.sig_magnitude
           