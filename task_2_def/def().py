"""
定义了一个函数，如果想要用return，必须要用一个变量接住比如：result = calculate_bmi(70),否则会报错
如果不想用return则需要在函数内部打印，否则当函数运行完毕则会消散，没法传给下一个变量
num = 10 是全局变量
在函数内部如果想要修改全局变量则需要global声明一下否则报错
final_price = list(map(lambda x,y: x * y, prices, numbers))
prices.sort(key=lambda x: -x)这里是把列表倒过来
names = ["Alex", "Bob", "Catherine"]
names.sort(key=lambda x: len(x),reverse=True) 在做复杂运算的时候需要用到key=lambda,key必须要写，这里的True和False必须首字母大写

def test(a):
    def inner(b):
        return a + b
    return inner
func_a = test(10) # 第一次赋值
func_b = test(20) # 第二次赋值
print(func_a(5)) # 结果是多少？
print(func_b(5)) # 结果是多少？
"""

# 1. 基础与默认参数：BMI 计算器
#【场景】：医疗助手需要一个基础工具来计算病人的 BMI。
#【任务】：编写函数 calculate_bmi，接收 weight (kg) 和 height (m)。
# 给 height 设置默认值 1.7（假设平均身高）。返回计算结果（公式：$weight / height^2$）。
# 调用：分别测试“只传体重”和“同时传体重身高”的情况。
# 考核点：def 关键字、必选参数 vs 默认参数、return 返回值。
# def calculate_bmi(weight:float, height = 1.7)->float:
#     """
#         Calculate the Body Mass Index (BMI).
#     """
#     bmi_value = weight/height**2
#     return bmi_value
# patient_1_bmi = calculate_bmi(70)
# print(f"patient_1_bmi: {patient_1_bmi}")
# patient_2_bmi = calculate_bmi(85, 1.8)
# print(f"patient_2_bmi: {patient_2_bmi}")
# 2. 不定长参数：多症状分析
# 【场景】：病人可能会输入 1 个症状，也可能是 5 个。
# 【任务】：
#
# 编写函数 analyze_symptoms，接收一个必选参数 patient_name，以及不定长位置参数 *symptoms。
#
# 在函数内部，打印病人的名字，并用循环打印出所有的症状。
#
# 调用：传入 ("Alex", "Fever", "Cough", "Headache")。
#
# 考核点：*args 的接收与内部遍历。
# def analyse_symptoms(patient_name:str, *symptoms)->str:
#     """
#     show the symptoms
#     :param patient_name:
#     :param symptoms:
#     :return:
#     """
#     print("patient_name:", patient_name)
#     print("symptoms list:")
#     for i in symptoms:
#         print("-",i)
# analyse_symptoms("Alex", "Fever", "Cough", "Headache")


# 4. 匿名函数与高阶：药品价格快速调整
# 【场景】：医院药价全线上涨 10%。
# 【任务】：
#
# 给定一个价格列表 prices = [100, 200, 300, 400]。
#
# 使用内置函数 map() 配合 lambda 表达式，将所有价格乘以 1.1。
#
# 将结果转回列表并打印。
#
# 考核点：lambda 匿名函数、高阶函数的基础应用。
# prices = [100, 200, 300, 400]
# numbers = [1, 2, 3, 4, 5]
# final_price = list(map(lambda x,y: x * y, prices, numbers))
# numbers.sort(reverse=False)
# A = sorted(numbers, reverse=True)
# print(A)
# print(numbers)
# prices.sort(key=lambda x: -x)
# print(prices)
# print(final_price)
# names = ["Alex", "Bob", "Catherine"]
# names.sort(key=lambda x: len(x),reverse=True) # 结果：['Bob', 'Alex', 'Catherine']
# print(names)

# 定义函数 vital_signs_logger(*signs)，内部用 for 循环打印每一个体征。
#
# 创建一个列表 my_signs = ["体温38度", "心率90", "血压120"]。
#
# 关键动作：用 * 解包的方式，将 my_signs 传给 vital_signs_logger。
#
# 进阶动作：再定义一个函数 advanced_logger(name, *signs)，调用时传入 "Alex" 加上解包后的 *my_signs。

# def vital_signs_logger(*signs):
#     for sign in signs:
#         print(sign)
# my_signs = ["体温38度", "心率90", "血压120"]
# vital_signs_logger(*my_signs)
# def advanced_logger(name, *signs):
#     print(name, signs)
# advanced_logger("Alex",*my_signs)
# 函数名 get_even_squares，接收一个列表参数，用 return 返回结果，不用 print。
def get_even_squares(num):
    """
    define a function that returns even squares
    :param num:
    :return:
    """
#     even_squares = []
#     for i in num:
#         if i % 2 == 0:
#             even_squares.append(i**2)
#     return even_squares
# print(get_even_squares([1,2,3,4,5]))
# # 题2： 写一个函数 count_vowels(s)，接收一个英文字符串，返回其中元音字母（a e i o u，不区分大小写）的个数。
# def count_vowels(s):
#     """
#     define a function that counts vowels
#     :param s:
#     :return:
#     """
#     count = 0
#     for i in s.upper():
#         if i in 'AEIOU':
#             count += 1
#     return count
# print(count_vowels("jjdskhjaeicoucaeiouacceuo"))
# # 题3： 写一个函数 flatten(nested)，接收一个二维列表（列表里面套列表），返回一个一维列表。
# # 比如输入 [[1,2],[3,4],[5]]，输出 [1,2,3,4,5]。
# def flatten(nested):
#     """
#     define a function that flattens a nested list
#     :param nested:
#     :return:
#     """
#     new_list = []
#     for i in nested:
#         for j in i:
#             new_list.append(j)
#     return new_list
# print(flatten([[1,2],[3,4],[5]]))
# 3. 作用域挑战：医院全局设置
# 【场景】：医院有一个全局的“紧急程度阈值”。
# 【任务】：
#
# 定义全局变量 EMERGENCY_LEVEL = 80。
#
# 编写函数 update_threshold，在函数内部尝试修改这个全局变量的值。
#
# 在函数外部打印该变量，确认它真的被修改了。
#
# 考核点：局部变量 vs 全局变量、global 关键字的使用。
# EMERGENCY_LEVEL = 80
# def update_threshold(num):
#     """
#     define a function that updates threshold
#     :param num:
#     :return:
#     """
#     global EMERGENCY_LEVEL
#     EMERGENCY_LEVEL = EMERGENCY_LEVEL + 1
#     st = EMERGENCY_LEVEL + num
#     return st
# result = update_threshold(30)
# print(result)
# print(EMERGENCY_LEVEL)
# 闭包
# def create_bill(init_price):
#     print("--- 1. 外部函数开始跑：建立账单环境 ---")
#
#     def add_money(amount):
#         print(f"--- 3. 内部函数开始跑：处理金额 {amount} ---")
#         return init_price + amount
#
#     print("--- 2. 外部函数结束：把 add_money 打包寄出去 ---")
#     return add_money
#
#
# # --- 外部函数在这里就运行结束并“去世”了 ---
# my_bill = create_bill(100)
#
# print("--- 休息时间，还没开始算钱 ---")
#
# # --- 直到这一行，内部函数才第一次呼吸 ---
# result = my_bill(50)
# print(f"最终结果: {result}")

# def test(a):
#     def inner(b):
#         return a + b
#     return inner
#
# func_a = test(10) # 第一次赋值
# func_b = test(20) # 第二次赋值
#
# print(func_a(5)) # 结果是多少？
# print(func_b(5)) # 结果是多少？



