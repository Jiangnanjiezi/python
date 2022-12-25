
from enum import Enum, unique
from math import sqrt
from random import randint

import pygame


# 颜色枚举
# @unique装饰器检查保证没有重复值
@unique
class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    # 随机颜色
    @staticmethod
    def random_color():
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)


# 定义球对象
class Ball(object):

    # 初始化
    def __init__(self, x, y, radius, mx, my, color=Color.RED):
        self.x = x
        self.y = y
        self.radius = radius
        self.mx = mx
        self.my = my
        self.color = color

    # 移动
    def move(self, screen):
        self.x += self.mx
        self.y += self.my
        # 下一次的位置
        next_x = self.x + self.mx
        next_y = self.y + self.my
        # 如果现在x的坐标小于等于半径，并且下次会更小
        # 或者如果现在x的坐标加上半径大于等于宽度，并且下次会更大
        # 此时需改变移动的方向
        if (self.radius >= self.x >= next_x) or \
                (screen.get_width() <= self.radius + self.x and self.x <= next_x):
            self.mx = -self.mx
        # 如果现在y的坐标小于等于半径，并且下次会更小
        # 或者如果现在y的坐标加上半径大于等于高度，并且下次会更大
        # 此时需改变移动的方向
        if (self.radius >= self.y >= next_y) or \
                (screen.get_height() <= self.radius + self.y and self.y <= next_y):
            self.my = -self.my

    # 碰撞
    def crash(self, other):
        if self != other:
            # 当前距离
            dx, dy = self.x - other.x, self.y - other.y
            distance = sqrt(dx ** 2 + dy ** 2)
            # 下一次距离
            next_dx = (self.x + self.mx) - (other.x + other.mx)
            next_dy = (self.y + self.my) - (other.y + other.my)
            next_distance = sqrt(next_dx ** 2 + next_dy ** 2)
            # 如果当前距离小于等于两圆半径之和，并且下一次不会变远的时候，需要修改两圆运动的方法
            # 如果下一次变得更远，则不变化运动方向
            if self.radius + other.radius >= distance \
                    and self.radius > other.radius:
                if next_distance <= distance:
                    self.mx, self.my = -self.mx, -self.my
                    other.mx, other.my = -other.mx, -other.my

    # 绘制球
    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.radius, 0)


def main():
    # 定义用来装所有球的容器
    balls = []
    # 初始化
    pygame.init()
    # 初始化窗口并设置窗口尺寸
    window = pygame.display.set_mode((800, 600))

    running = True
    # 开启一个事件循环处理发生的事件
    while running:
        # 从消息队列中获取事件,并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 处理鼠标事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos  # 获得点击鼠标的位置
                radius = randint(10, 100)
                mx, my = randint(-10, 10), randint(-10, 10)
                color = Color.random_color()
                # 在点击鼠标的位置创建一个球,球的大小、速度和颜色随机
                ball = Ball(x, y, radius, mx, my, color)
                balls.append(ball) # 将球添加到列表容器中
        window.fill((255, 255, 255))
        # 把所有球画出来
        for ball in balls:
            ball.draw(window)
        pygame.display.flip()
        # 每隔50毫秒就改变球的位置，再刷新窗口
        pygame.time.delay(50)
        for ball in balls:
            ball.move(window)
            # 检查球有没有碰到其他的球
            for other in balls:
                ball.crash(other)


if __name__ == '__main__':
    main()
