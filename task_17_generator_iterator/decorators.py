"""
多层装饰器运行像洋葱一样
decorator1 ← 最外层
    decorator2 ← 中间层
        say_hello ← 核心
    decorator2
decorator1
"""
def decorator1(func):
    def wrapper():
        print("decorator1 开始")
        func()
        print("decorator1 结束")
    return wrapper

def decorator2(func):
    def wrapper():
        print("decorator2 开始")
        func()
        print("decorator2 结束")
    return wrapper

@decorator1
@decorator2
def say_hello():
    print("hello")

say_hello()
# 输出：
# decorator1 开始
# decorator2 开始
# hello
# decorator2 结束
# decorator1 结束