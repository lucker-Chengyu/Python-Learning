"""
x.append(a)是原地修改所以不会返回值，如果打印会返回none
x.split()默认返回的是一个列表
"""

# 1. 列表与切片：病历记录仪 (Lists & Slicing)
# 【场景】：你获取了一个病人在过去 7 小时的实时心率列表：
# heart_rates = [72, 75, 82, 90, 110, 120, 105]
# 【任务】：
#
# 使用切片获取“最后 3 小时”的心率数据。
#
# 使用切片将列表倒序打印（模拟查看从新到旧的记录）。
#
# 在列表末尾添加一个新的心率值 98。
#
# 将索引为 2 的心率值修改为 85。
#
# 考核点：append(), indexing, slicing [start:end:step]。
# task1
heart_rates = [72, 75, 82, 90, 110, 120, 105]
final_data1 = heart_rates[4::]
flash_back = heart_rates[::-1]
heart_rates.append(98)
heart_rates.insert(8,99)
heart_rates[2] = 85
print(final_data1)
print(flash_back)
print(heart_rates)
# 2. 字典与键值对：智能挂号系统 (Dictionaries)
# 【场景】：你需要管理诊室的医生排班，创建一个字典 doctor_schedule：
#
# 键（Key）是医生姓名，值（Value）是科室。
#
# 初始数据："Dr. Zhang": "Cardiology", "Dr. Wang": "Pediatrics"
# 【任务】：
#
# 新增一名医生 "Dr. Li" 到 "Neurology"。
#
# 修改 "Dr. Zhang" 的科室为 "General Medicine"。
#
# 使用 get() 方法安全地查询 "Dr. Smith" 的科室（如果不存在，返回 "Not Found"）。
#
# 分别获取并打印出所有的医生名字（keys）和所有的科室（values）。
#
# 考核点：dict 的增删改查、get() 方法、keys() 与 values()。
# task2
doctor_schedule = {"Dr. Zhang": "Cardiology", "Dr. Wang": "Pediatrics"}
doctor_schedule["Dr. Li"] = "Neurology"
doctor_schedule["Dr. Zhang"] = "General Medicine"
final_result = doctor_schedule.get("Dr.Smith","Not Found")
print(doctor_schedule)
print(final_result)
# 3. 元组与集合：病人 ID 库 (Tuples & Sets)
# 【场景】：医院系统导入了两批病人 ID 列表，其中包含重复项：
# batch_1 = ["P001", "P002", "P003", "P002"]
# batch_2 = ["P003", "P004", "P005"]
# 【任务】：
#
# 定义一个元组 hospital_info，存储医院名称 "Monash Health" 和 成立年份 1848，并尝试修改它（观察报错）。
#
# 利用**集合（Set）**自动去重的特性，求出 batch_1 中不重复的病人 ID。
#
# 求出 batch_1 和 batch_2 两个序列的并集（所有出现过的病人）。
#
# 考核点：tuple 的不可变性、set() 去重、集合运算（并集）。
# task3
batch_1 = ["P001", "P002", "P003", "P002"]
batch_2 = ["P003", "P004", "P005"]
hospital_info = ("Monash Health", 1848)
# hospital_info.append(1949) I have observe the error that the tuple can not be modified
set1 = set(batch_1)
set2 = set(batch_2)
set3 = set1|set2
set4 = set1 & set2
print(set1)
print(set2)
print(set3)
print(set4)
#  “序列（Sequence）”。
#
# 这章非常关键，它是 Python 处理大模型语料（列表、元组、字符串、字典、集合）的生命线。如果序列玩不转，后面的大模型分词（Tokenization）和数据预处理你根本无法下手。
#
# 为了实现你说的“做完就代表掌握全章”，我为你设计了 4 道覆盖全知识点的综合实战题。这些题会把索引、切片、常用方法、字典映射、集合去重全部揉进医疗场景里。
#
# 1. 列表与切片：病历记录仪 (Lists & Slicing)
# 【场景】：你获取了一个病人在过去 7 小时的实时心率列表：
# heart_rates = [72, 75, 82, 90, 110, 120, 105]
# 【任务】：
#
# 使用切片获取“最后 3 小时”的心率数据。
#
# 使用切片将列表倒序打印（模拟查看从新到旧的记录）。
#
# 在列表末尾添加一个新的心率值 98。
#
# 将索引为 2 的心率值修改为 85。
#
# 考核点：append(), indexing, slicing [start:end:step]。
#
# 2. 字典与键值对：智能挂号系统 (Dictionaries)
# 【场景】：你需要管理诊室的医生排班，创建一个字典 doctor_schedule：
#
# 键（Key）是医生姓名，值（Value）是科室。
#
# 初始数据："Dr. Zhang": "Cardiology", "Dr. Wang": "Pediatrics"
# 【任务】：
#
# 新增一名医生 "Dr. Li" 到 "Neurology"。
#
# 修改 "Dr. Zhang" 的科室为 "General Medicine"。
#
# 使用 get() 方法安全地查询 "Dr. Smith" 的科室（如果不存在，返回 "Not Found"）。
#
# 分别获取并打印出所有的医生名字（keys）和所有的科室（values）。
#
# 考核点：dict 的增删改查、get() 方法、keys() 与 values()。
#
# 3. 元组与集合：病人 ID 库 (Tuples & Sets)
# 【场景】：医院系统导入了两批病人 ID 列表，其中包含重复项：
# batch_1 = ["P001", "P002", "P003", "P002"]
# batch_2 = ["P003", "P004", "P005"]
# 【任务】：
#
# 定义一个元组 hospital_info，存储医院名称 "Monash Health" 和 成立年份 1848，并尝试修改它（观察报错）。
#
# 利用**集合（Set）**自动去重的特性，求出 batch_1 中不重复的病人 ID。
#
# 求出 batch_1 和 batch_2 两个序列的并集（所有出现过的病人）。
#
# 考核点：tuple 的不可变性、set() 去重、集合运算（并集）。
#
# 4. 字符串处理：诊断报告清洗 (String Methods)
# 【场景】：AI 提取了一段非常乱的诊断文本：
# raw_report = "  DIAGNOSIS: Fever and Cough; Treatment: Rest   "
# 【任务】：
#
# 去掉首尾多余的空格。
#
# 将整段文字转为全大写。
#
# 使用 replace() 将 "FEVER" 替换为 "INFLUENZA"。
#
# 使用 split() 按照 ";" 将字符串拆分成两部分。
#
# 考核点：strip(), upper(), replace(), split()。
# task4
raw_report = "  DIAGNOSIS: Fever and Cough; Treatment: Rest   "
new_report1 = raw_report.strip(" ")
print(new_report1)
new_report2 = new_report1.upper()
print(new_report2)
new_report3 = new_report2.replace("FEVER", "INFLUENZE")
print(new_report3)
new_report4 = new_report3.split(";")
print(new_report4)