import types
class Dog:
    pass
def bark(self):
    print(f"{self.name}在叫")
d1 = Dog()
d1.name = "旺财"
d1.bark = types.MethodType(bark, d1)
d1.bark()

class Dog:

    def __init__(self, name):
        self.name = name
    def bark(self):
        print(f"{self.name}在叫")
d1 = Dog("旺财")
d1.bark()
