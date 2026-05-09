def my_print(*args, **kwargs):
    print(args)
    print(kwargs)
my_print(1, 2, a=3, b=4, c=5)

def my_println(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
my_println(a=2, b=3, c=4, d=5)
