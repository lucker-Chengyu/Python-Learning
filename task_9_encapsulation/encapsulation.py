# class Student:
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#
#     def get_score(self):
#         return self.__score
#     @property
#     def score(self):
#         return self.__score
#     @score.setter
#     def score(self, value):
#         if 100 >= value >= 0:
#             self.__score = value
#         else:
#             print("分数不合法")
#             self.__score = 0
# d1 = Student("zhangshan", 26)
# print(d1.score)
# d2 = Student("zhangshan", 27)
# print(d2.get_score())
# d3 = Student("zhangshan", -3)
# print(d3.score)

# class Animal:
#     def __init__(self, name):
#         self.name = name
#     def speak(self):
#         print(f"{self.name}汪汪叫")
# class Dog(Animal):
#     def __init__(self, name, breed):
#         self.breed = breed
#         super().__init__(name)
# d1 = Dog("旺财", "拉布拉多")
# d1.speak()


class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        print(f"{self.name}汪汪叫")
class Dog(Animal):
    def __init__(self, name, breed):
        self.breed = breed
        super().__init__(name)
    def speak(self):  # override 父类的 speak
            print(f"小狗{self.name}汪汪叫")
d1 = Dog("旺财", "拉布拉多")
d1.speak()

