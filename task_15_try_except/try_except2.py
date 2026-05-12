# 自定义异常
class AgeError(Exception):
    def __init__(self, age):
        self.age = age
        super().__init__(f"年龄不合法: {age}")
def set_age(age):
    if age < 0 or age > 150:
        raise AgeError(age)
    print(f"年龄: {age}")
try:
    set_age(200)
except AgeError as e:
    print(e)

