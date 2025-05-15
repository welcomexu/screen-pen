from PyQt6.QtCore import QPoint, QRect, QLine
from PyQt6.QtGui import QPainter

class DrawingTool:
    def __init__(self):
        self.start_point = QPoint()
        self.end_point = QPoint()
        
    def start(self, point):
        self.start_point = point
        self.end_point = point
        
    def update(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        
    def draw(self, painter):
        pass


class FreeDraw(DrawingTool):
    def draw(self, painter):
        painter.drawLine(self.start_point, self.end_point)


class Line(DrawingTool):
    def draw(self, painter):
        painter.drawLine(self.start_point, self.end_point)


class Rectangle(DrawingTool):
    def draw(self, painter):
        rect = QRect(self.start_point, self.end_point).normalized()
        painter.drawRect(rect)


class Ellipse(DrawingTool):
    def draw(self, painter):
        rect = QRect(self.start_point, self.end_point).normalized()
        painter.drawEllipse(rect)


class Eraser(FreeDraw):
    # 橡皮擦实际上就是使用透明色的画笔
    pass
