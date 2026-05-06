"""
写继承需要首先用super().__init__(子类里需要调用的父类参数)
"""
# 题1： 定义一个 Rectangle 类，有 width 和 height 两个属性，有一个 area() 方法返回面积，
# 有一个 perimeter() 方法返回周长。创建两个不同尺寸的矩形对象，打印它们各自的面积和周长。
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    def perimeter(self):
        return (self.width + self.height) * 2
rect1 = Rectangle(2, 3)
rect2 = Rectangle(4, 5)
print(rect1.area(), rect1.perimeter())
print(rect2.area(), rect2.perimeter())
# 题2： 定义一个 Student 类，属性有 name（姓名）和 scores（成绩列表）。
# 有一个 average() 方法返回平均分，有一个 is_pass() 方法返回是否及格（平均分60以上返回 True）。创建两个学生对象测试。
class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores
    def average(self):
        average_scores = sum(self.scores)/len(self.scores)
        return average_scores
    def is_pass(self):
        if self.average() > 60:
            return True
        else:
            return False
aver1 = Student('A', [1,7,2,3,4,5])
aver2 = Student('B', [1,2,3,5,5,2])
print(f"name:{aver1.name} average_scores:{aver1.average()} {aver1.is_pass()}")
print(f"name:{aver2.name} average_scores:{aver2.average()} {aver2.is_pass()}")
# 题3： 在题2的基础上，定义一个 GraduateStudent（研究生）类，继承 Student，
# 新增一个属性 supervisor（导师姓名），重写 is_pass() 方法，改为平均分75以上才及格。
class GraduateStudent(Student):
    def __init__(self, name, scores, supervisor):
        super().__init__(name, scores)
        self.supervisor = supervisor
    def is_pass(self):
        if self.average() >= 75:
            return True
        else:
            return False
grad_stu = GraduateStudent("老王", [80, 70, 90], "张教授")
print(f"name:{grad_stu.name} average_scores:{grad_stu.average()} {grad_stu.is_pass()}")


