class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.__radius = radius
    def area(self):
        return 3.14 * self.__radius * self.__radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
    def area(self):
        return self.__width * self.__height
def print_area(shape):
    shape.area()
    print(shape.area())
print_area(Circle(3))
print_area(Rectangle(2,3))


