"""
生成器笔记
├── 是什么：省内存的迭代器，用一个算一个
├── 两种创建方式：
│   ├── (x for x in ...)  生成器表达式
│   └── 函数里用 yield
│
├── yield vs return
│   ├── return：函数结束，下次从头开始
│   └── yield：暂停记住位置，下次从这里继续
│
├── next() vs send()
│   ├── next(g)：取下一个值，不传值
│   └── g.send(值)：取下一个值，同时传值给当前yield
│   └── 注意：第一次必须用next()启动，不能send
│
├── 踩坑点
│   ├── return值塞进StopIteration，for循环会丢掉
│   ├── send只传给当前暂停的yield，不影响其他yield
│   └── () 是生成器不是元组，元组要用tuple()
│
└── 什么时候用
    └── 数据量大、无限序列、省内存时用生成器
"""
# send是进行传值操作
def gen():
    x = yield 1    # 第1个yield
    y = yield 2    # 第2个yield
    z = yield 3    # 第3个yield
    print(x, y, z)

g = gen()
next(g)          # 启动，停在第1个yield，返回1
g.send("a")      # 传给x，停在第2个yield，返回2
g.send("b")      # 传给y，停在第3个yield，返回3
g.send("c")      # 传给z，没有yield了，结束
# 输出：a b c