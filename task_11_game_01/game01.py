class Birds:
    def __init__(self, name, color, skill_description, damage):  # 加 damage
        self.name = name
        self.color = color
        self.skill_description = skill_description
        self.damage = damage  # 每种鸟自己持有伤害值
    def fly(self): pass
    def call(self): pass
    def use_skill(self):
        print(f"{self.name} 使用了 {self.skill_description}进行了攻击")
class RedBirds(Birds):
    def __init__(self):
        super().__init__("红火", "红色", "撞击前方障碍物，造成大量伤害", damage=80)
    # fly / call 不变...
class YellowBirds(Birds):
    def __init__(self):
        super().__init__("黄蜂", "黄色", "瞬间加速, 穿透障碍物", damage=50)
class BlueBirds(Birds):
    def __init__(self):
        super().__init__("蓝冰", "蓝色", "分裂成三只小鸟，分散攻击", damage=90)
class Obstacle:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
    def be_attacked(self, bird):
        print(f"{bird.name}向{self.name}发起了攻击")
        bird.use_skill()
        self.strength -= bird.damage  # ✅ 直接问鸟要，不用 isinstance
        if self.strength <= 0:
            print(f"{self.name}已经被摧毁")
        else:
            print(f"当前障碍物{self.name}还剩{self.strength}点坚固值")

b1 = RedBirds()
b2 = YellowBirds()
b3 = BlueBirds()
o1 = Obstacle("木头堡垒", 100)
o2 = Obstacle("石头塔楼", 200)

o1.be_attacked(b1)
o1.be_attacked(b2)
o1.be_attacked(b3)