"""
带参数的装饰器
"""
def times(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@times(2)
def say_hello():
    print("hello")

say_hello()