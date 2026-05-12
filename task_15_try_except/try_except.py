# 基础结构
try:

    result = 10 / 0
except ZeroDivisionError as e:
    print(f"出错了: {e}")
finally:
    # 无论有没有结束都会执行最后这个print
    print("结束")

