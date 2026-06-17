"""
装饰器优点
├── 1. 不改原函数，直接加功能
│   └── 原函数代码零改动，加个@就行
│
├── 2. 代码复用
│   └── 100个函数要加日志，写一个装饰器
│       每个函数加@，不用重复写100次
│
├── 3. 职责分离
│   └── 原函数只做自己的事
│       日志、计时、验证这些交给装饰器
│       代码更清晰
│
├── 4. 常见使用场景
│   ├── 记录日志 @logger
│   ├── 计算运行时间 @timer
│   ├── 登录验证 @login_required
│   └── 权限验证 @permission_required
│
└── 本质
    └── 闭包的应用
        func传进去 → wrapper包裹 → 返回wrapper
        @decorator = say_hello = decorator(say_hello)
"""

def decorator(func):
    def wrapper():
        print("1. wrapper开始")
        func()
        print("3. wrapper结束")
    return wrapper

@decorator
def say_hello():
    print("2. hello")

say_hello()

# 如果不用语法糖：
def logger(func):
    def wrapper():
        print("开始执行")
        func()
        print("执行完毕")
    return wrapper

def say_hello():
    print("hello")

# 不用@语法糖——手动传进去
say_hello = logger(say_hello)

say_hello()
"""
def logger(func):
    def wrapper():
        print("开始")
        func()
        print("结束")
    return wrapper

def say_hello():
    print("hello")

# 这几种写法都行
say_hello = logger(say_hello)    # 覆盖原来的名字
new_func = logger(say_hello)     # 新名字
f = logger(say_hello)            # 随便起

# 用新名字——原函数还能单独调用，没有装饰效果
new_func = logger(say_hello)
say_hello()   # 没有装饰效果，只打印hello
new_func()    # 有装饰效果

# 用同名覆盖——原函数被替换，装饰效果统一
say_hello = logger(say_hello)
say_hello()   # 有装饰效果
"""
# 输出：
# 开始执行
# hello
# 执行完毕


# 语法糖让代码变得很简单