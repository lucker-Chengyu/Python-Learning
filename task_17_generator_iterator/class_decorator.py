"""
类装饰器
"""
class Logger:
    def __init__(self, func):
        self.func = func        # 把原函数保存起来

    def __call__(self, *args, **kwargs):   # 调用时执行这里
        print("开始执行")
        self.func(*args, **kwargs)
        print("执行完毕")

@Logger
def say_hello():
    print("hello")

say_hello()
# 输出：
# 开始执行
# hello
# 执行完毕