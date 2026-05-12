# 捕获多种异常
try:
    x = int(input("输入数字："))
    result = 10 / x
except ValueError:
    print("请输入数字，不要输入字母")
except ZeroDivisionError:
    print("不能除以0")
except Exception as e:
    # BaseException
    # └── Exception          ← 几乎所有异常的父类
    # ├── ValueError
    # ├── TypeError
    # ├── ZeroDivisionError
    # ├── IndexError
    # ├── KeyError
    # └── ...

    # 所以exception是用来兜底的
    print(f"其他错误：{e}")
