import math
import random
import time
from functools import wraps


class Cylinder:
    # 构造方法
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

    # 输出信息
    def PrintInfo(self):
        print(f"Cylinder: (半径 = {self.radius}, 高 = {self.height})")

    # 计算体积
    def GetVolume(self):
        return math.pi * self.radius ** 2 * self.height

    # 重写__str__函数
    def __str__(self):
        return f"Cylinder: (半径 = {self.radius}, 高 = {self.height})"


# 装饰器
def cal_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        print("开始时间为：", start)
        result = func(*args, **kwargs)
        end = time.time()
        print("结束时间为：", end)
        print("使用时间为%f秒。" % (end - start))
        return result
    return inner


@cal_time
def delete_item(cylinders):
    # 记录已经删除的ID
    ids = []
    while len(cylinders) > 0:
        # 生成随机ID
        delete_id = random.randint(0, 9)
        while delete_id in ids:  # 如果ID已经生成过，则再次生成
            delete_id = random.randint(0, 9)
        ids.append(delete_id)

        for item in cylinders:  # 遍历列表，找到对应id的元素，根据该元素的索引删除该元素
            if item[0] == delete_id:
                print(f"删除元素----编号为：{item[0]}  对象为：{item[1]}")
                cylinders.pop(cylinders.index(item))


if __name__ == '__main__':
    cylinders = []
    # 添加10个元素
    for i in range(10):
        radius = random.randint(1, 20)  # 随机半径
        height = random.randint(1, 20)  # 随机高
        cylinders.append((i, Cylinder(radius, height)))  # 使用元组 （编号，对象）
    print(cylinders)

    # 执行删除
    delete_item(cylinders)

"""
输出结果为：

[(0, <__main__.Cylinder object at 0x000001F6C335ECA0>), (1, <__main__.Cylinder object at 0x000001F6C335EB20>), (2, <__main__.Cylinder object at 0x000001F6C335EA90>), (3, <__main__.Cylinder object at 0x000001F6C335EA30>), (4, <__main__.Cylinder object at 0x000001F6C335E9D0>), (5, <__main__.Cylinder object at 0x000001F6C335E970>), (6, <__main__.Cylinder object at 0x000001F6C335E910>), (7, <__main__.Cylinder object at 0x000001F6C335E8B0>), (8, <__main__.Cylinder object at 0x000001F6C335E850>), (9, <__main__.Cylinder object at 0x000001F6C335E7F0>)]
开始时间为： 1671955566.5412166
删除元素----编号为：4  对象为：Cylinder: (半径 = 9, 高 = 18)
删除元素----编号为：6  对象为：Cylinder: (半径 = 1, 高 = 12)
删除元素----编号为：2  对象为：Cylinder: (半径 = 16, 高 = 2)
删除元素----编号为：9  对象为：Cylinder: (半径 = 5, 高 = 17)
删除元素----编号为：0  对象为：Cylinder: (半径 = 1, 高 = 4)
删除元素----编号为：1  对象为：Cylinder: (半径 = 4, 高 = 9)
删除元素----编号为：7  对象为：Cylinder: (半径 = 16, 高 = 5)
删除元素----编号为：8  对象为：Cylinder: (半径 = 20, 高 = 8)
删除元素----编号为：5  对象为：Cylinder: (半径 = 12, 高 = 3)
删除元素----编号为：3  对象为：Cylinder: (半径 = 11, 高 = 14)
结束时间为： 1671955566.5422137
使用时间为0.000997秒。
"""