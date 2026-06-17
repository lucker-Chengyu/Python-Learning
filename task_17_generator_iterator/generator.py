"""
return 像看书看到一半合上书，下次重新从第一页看。
yield 像看书看到一半夹书签，下次从书签的地方继续看。
"""
# return——每次调用从头开始，执行到return就结束
def counter_return(max):
    current = 0
    while current < max:
        return current     # 第一次就结束了，current永远是0
        current += 1       # 永远不会执行到

g = counter_return(3)
print(g)   # 0
print(g)   # 0  ← 每次都是0，因为每次都从头开始
print(g)   # 0






# yield——记住上次位置，下次从那里继续
def counter_yield(max):
    current = 0
    while current < max:
        yield current      # 返回值，但不结束，记住位置
        current += 1       # 下次next()从这里继续

g = counter_yield(3)
print(next(g))   # 0  ← 第一次
print(next(g))   # 1  ← 从上次继续
print(next(g))   # 2  ← 再继续



# 创建方式
"""
# 这不是元组推导式，是生成器表达式
g = (x for x in range(5))
print(type(g))   # <class 'generator'>

# 元组是这样创建的，不能推导
t = tuple(x for x in range(5))
print(type(t))   # <class 'tuple'>

# 生成器结束时，"done"会被塞进StopIteration里
def fibo():
    ...
    while counter < 10:
        yield b
        ...
    return "done"    
"""
# 方式1：生成器表达式（小括号）
g = (x for x in range(5))

# 方式2：yield函数
def counter(max):
    for i in range(max):
        yield i

g = counter(5)


# 例子
# 斐波那数列
def fibonacci():
    a, b = 0, 1
    while True:          # 无限生成
        yield b
        a, b = b, a + b

g = fibonacci()
for _ in range(8):
    print(next(g))
# 输出：1 1 2 3 5 8 13 21