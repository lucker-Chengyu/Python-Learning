# 写一个函数 make_robot(robot_id, battery, max_load, zone)，返回一个字典，包含这四个字段。然后创建三个机器人，存进一个列表，遍历打印每个机器人的 id 和 zone。
def make_robot(robot_id, battery, max_load, zone):
    robot = {
        'id': robot_id,
        'battery': battery,
        'max_load': max_load,
        'zone': zone
    }
    return robot
robots = [make_robot('robot1', 100, 50,'A'),
          make_robot('robot2', 40, 20,'B'),
          make_robot('robot3', 20, 700, 'C'),]
for robot in robots:
    print(f"robot_id:{robot["id"]}, zone:{robot["zone"]}")