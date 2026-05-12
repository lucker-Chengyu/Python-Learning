# *args是tripe，而**kwargs是字典类型，print中如果加*args则是解包出来常数，**kwargs则会报错，因为系统无法识别出自定义的变量，如果想用则可以使用sep=", ", end="!\n" 进行分割
# 如果想传一个列表则可以，先把列表转成tripe形式，如list = [1, 2, 3, 4, 5] *list则为tripe
def my_print(*args, **kwargs):
    print(args)
    print(kwargs)
my_print(1, 2, a=3, b=4, c=5)

def my_println(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
my_println(a=2, b=3, c=4, d=5)


def my_print(*args, **kwargs):
    print(*args, **kwargs)  # 这样可以

my_print(1, 2, sep=", ", end="!\n")  # kwargs 只传 print 认识的参数
# 输出：1, 2!