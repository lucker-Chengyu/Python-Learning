# 自定义一个从1数到n的迭代器
class Counter:
    def __init__(self, max):
        self.max = max
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        self.current += 1
        return self.current

# 使用
for i in Counter(5):
    print(i)
# 输出：1 2 3 4 5