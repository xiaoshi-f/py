# -*- coding: utf-8 -*-
# 25. 面向对象-类与对象
# 知识点：类与对象的关系、class 定义、__init__ 构造方法、self 是什么、
#        实例属性 vs 类属性（大坑）、实例方法/类方法/静态方法、
#        私有约定 _x 与 __x（名称改写）、封装思想、
#        对象的生命周期 __init__ / __del__、组合（一个类里装另一个类）
#
# 为什么要学：函数适合「一步一步做事情」，类适合「描述一个东西」。
#             写项目时，用类把数据和操作数据的行为打包在一起，代码才不会散。

# ==========================================================
# 1. 类与对象：类是图纸，对象是按图纸造出来的东西
# ==========================================================
# 类（Class）：抽象的模板，定义了「有什么属性、能做什么事」
# 对象（Object / 实例）：具体的个体，占内存，有自己的数据
# 举例：类 = 汽车设计图，对象 = 你那辆具体的车

print("--- 第一个类 ---")


class Dog:
    """狗类：演示最基本的类结构"""

    # 类属性：属于「类」本身，所有对象共享一份（下面第 4 节专门讲坑）
    species = "犬科动物"

    # __init__ 是构造方法：创建对象时自动调用，用来初始化属性
    # self 代表「当前这个对象」，必须写在第一个参数位（名字可以改但不建议）
    def __init__(self, name, age):
        # 实例属性：每个对象各自一份，用 self.xxx 定义
        self.name = name
        self.age = age
        print(f"  一只叫 {name} 的狗被创建出来了")

    # 实例方法：第一个参数必须是 self，调用时 Python 自动传入对象本身
    def bark(self):
        return f"{self.name}：汪汪！"

    def get_info(self):
        return f"{self.name}，{self.age} 岁，是{self.species}"


# 创建对象（实例化）：类名(参数)，不需要传 self
dog1 = Dog("旺财", 3)
dog2 = Dog("小黑", 5)

print(" ", dog1.bark())       # 调用方法：对象.方法名()
print(" ", dog2.get_info())
print("  访问属性：", dog1.name, dog1.age)
print("  类属性：", Dog.species)

# dog1 和 dog2 是不同对象，属性互不影响
dog1.age = 4
print("  改 dog1 年龄后：", dog1.age, dog2.age)  # 4 5，互不影响

# ==========================================================
# 2. self 到底是什么
# ==========================================================
print("\n--- self 的本质 ---")
# dog1.bark() 等价于 Dog.bark(dog1)
# Python 只是把「对象.方法()」自动翻译成「类.方法(对象)」
print("  两种调用等价：", dog1.bark(), "|", Dog.bark(dog1))

# self 就是对象自己在内存里的地址
print("  dog1 的 id：", id(dog1))
print("  self 就是对象本身，只是 Python 帮你自动传了")

# ==========================================================
# 3. 属性可以动态增删改（Python 很灵活，但也容易出事）
# ==========================================================
print("\n--- 动态属性 ---")
dog1.color = "黄色"  # 随时给对象加新属性（类里没定义也行）
print("  新增属性 color：", dog1.color)
# dog2.color   # AttributeError：dog2 没有这个属性

del dog1.color  # 删除属性
print("  删除后 hasattr：", hasattr(dog1, "color"))

# ⚠ 灵活是双刃剑：拼错属性名不会报错，而是悄悄创建了一个新属性
dog1.nmae = "拼错了"  # 本来想改 name，结果多了个 nmae
print("  name 没变：", dog1.name, "，但多了个 nmae：", dog1.nmae)
# 解决办法：用 __slots__ 限制能有哪些属性（见 27 号文件）

# ==========================================================
# 4. ⚠ 实例属性 vs 类属性（经典大坑）
# ==========================================================
print("\n--- 类属性的共享陷阱 ---")


class Student:
    school = "灵兔学院"      # 类属性：所有学生共享
    count = 0                # 类属性当计数器用

    def __init__(self, name, scores=None):
        self.name = name                 # 实例属性
        # ⚠ 这里如果写 self.scores = [] 当默认值就踩了可变默认值的坑（见 17 号文件）
        self.scores = list(scores) if scores else []
        Student.count += 1               # 注意用「类名.count」改，不要用 self.count


s1 = Student("小石", [88, 92])
s2 = Student("老张")
print("  学校（类属性）：", s1.school, s2.school)
print("  学生总数（类属性计数）：", Student.count)  # 2

# 坑1：通过对象给类属性赋值，只会给这个对象创建同名实例属性，类属性不变
s1.school = "北大"
print("  s1.school =", s1.school)      # 北大（实例属性，遮住了类属性）
print("  s2.school =", s2.school)      # 灵兔学院（类属性没变）
print("  Student.school =", Student.school)  # 灵兔学院

# 坑2：类属性如果是可变对象，通过对象修改它会影响所有人
class Team:
    members = []  # ⚠ 类属性是个列表，所有实例共享同一个列表！

    def __init__(self, name):
        self.name = name


t1 = Team("一组")
t2 = Team("二组")
t1.members.append("小石")  # 改的是类属性那个共享列表
print("\n  t1.members =", t1.members)  # ['小石']
print("  t2.members =", t2.members)  # ['小石']  ← 二组莫名多了一个人！
print("  Team.members =", Team.members)
# ✅ 正确做法：可变数据放到 __init__ 里做成实例属性

# ==========================================================
# 5. 三种方法：实例方法 / 类方法 / 静态方法
# ==========================================================
print("\n--- 三种方法 ---")


class Person:
    species = "人类"
    population = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.population += 1

    # ① 实例方法：第一个参数 self，可以读写实例属性，最常用
    def introduce(self):
        return f"我叫 {self.name}，{self.age} 岁"

    # ② 类方法：@classmethod 装饰，第一个参数 cls（代表类本身）
    #    用途：操作类属性、做「替代构造器」（用不同方式创建对象）
    @classmethod
    def get_population(cls):
        return f"当前总人数：{cls.population}"

    @classmethod
    def from_birth_year(cls, name, birth_year):
        """替代构造器：直接传出生年份创建对象"""
        import datetime
        age = datetime.date.today().year - birth_year
        return cls(name, age)  # cls(...) == Person(...)，子类调用时会自动变成子类

    # ③ 静态方法：@staticmethod 装饰，不接收 self 也不接收 cls
    #    用途：跟类有点关系、但不需要访问类/实例状态的工具函数
    @staticmethod
    def is_adult(age):
        return age >= 18


p = Person("小石", 25)
print(" ", p.introduce())                      # 实例方法：对象调用
print(" ", Person.get_population())            # 类方法：类名调用（对象也能调）
print(" ", Person.from_birth_year("老张", 1990).introduce())
print("  是否成年：", Person.is_adult(20))      # 静态方法：像普通函数

# 静态方法本质上就是「放在类里面的普通函数」，只是逻辑上归这个类管

# ==========================================================
# 6. 私有属性与方法（约定 + 名称改写）
# ==========================================================
print("\n--- 私有：约定与名称改写 ---")


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner          # 公开属性
        self._bank = "某银行"        # 单下划线：约定上是内部用（不强制，只是提醒）
        self.__balance = balance    # 双下划线：触发名称改写，外部不好直接访问

    def deposit(self, amount):
        """存款：通过方法来改私有属性，可以在这里做校验"""
        if amount <= 0:
            raise ValueError("存款金额必须大于 0")
        self.__balance += amount
        return self.__balance

    def get_balance(self):
        """查询余额：只读，不暴露修改入口"""
        return self.__balance

    def __risk_check(self):   # 私有方法，外部调不到
        return self.__balance > 10000


acc = BankAccount("小石", 100)
acc.deposit(500)
print("  余额：", acc.get_balance())
print("  _bank（约定私有，其实能访问）：", acc._bank)

# 双下划线触发「名称改写」：__balance 实际名字变成了 _BankAccount__balance
print("  改写后的真实名字：", [a for a in vars(acc) if "balance" in a])
# print(acc.__balance)              # AttributeError
print("  硬要访问也行（但不该这么做）：", acc._BankAccount__balance)

# 为什么这么设计：不是真安全，是防止「子类不小心覆盖父类属性」和误操作
# Python 的哲学：我们相信你会守规矩（We're all consenting adults here）

# ==========================================================
# 7. 封装：用方法保护数据（getter/setter 的 Python 写法）
# ==========================================================
print("\n--- 封装：属性校验 ---")


class Temperature:
    """温度类：摄氏度不能低于绝对零度"""

    def __init__(self, celsius=0):
        # 注意：这里调用的是下面的 setter，构造时就做了校验
        self.celsius = celsius

    # Python 里别写 Java 那种 getXxx/setXxx，用 @property（见 27 号文件）
    # 这里先用普通方法演示校验逻辑
    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度 -273.15℃")
        self._celsius = value

    def get_celsius(self):
        return self._celsius

    def to_fahrenheit(self):
        return self._celsius * 9 / 5 + 32


# 上面这个版本的 __init__ 直接赋值绕过了校验，下面 27 号文件用 @property 修正

# ==========================================================
# 8. 对象的生命周期
# ==========================================================
print("\n--- 生命周期 ---")


class Resource:
    def __init__(self, name):
        self.name = name
        print(f"  __init__：{name} 被创建")

    def __del__(self):
        # 析构方法：对象被垃圾回收时调用
        # ⚠ 不要依赖它做重要清理（调用时机不确定），用 with/close 更靠谱
        print(f"  __del__：{self.name} 被销毁")


r = Resource("临时对象")
del r  # 手动删除引用，触发 __del__
print("  （程序结束时剩下的对象也会自动销毁）")

# ==========================================================
# 9. 组合：一个类里装另一个类的对象（比继承更常用）
# ==========================================================
print("\n--- 组合：has-a 关系 ---")


class Engine:
    """发动机（车载方向很直观：车 has-a 发动机）"""

    def __init__(self, power):
        self.power = power

    def start(self):
        return f"{self.power}kW 发动机启动"


class Wheel:
    def __init__(self, size):
        self.size = size


class Car:
    """汽车：由发动机、轮子组合而成"""

    def __init__(self, brand, power, wheel_size):
        self.brand = brand
        self.engine = Engine(power)                    # 组合：车里装了个发动机对象
        self.wheels = [Wheel(wheel_size) for _ in range(4)]

    def start(self):
        # 车自己不实现启动细节，交给发动机（委托）
        return f"{self.brand}：{self.engine.start()}"


car = Car("测试车", 150, 18)
print(" ", car.start())
print("  轮子数量：", len(car.wheels))
# 设计原则：优先用组合（has-a），别动不动就继承（is-a）

# ==========================================================
# 10. 实战：用类改写之前用函数写的「学生管理」
# ==========================================================
print("\n--- 实战：学生类 ---")


class Student2:
    """学生：把数据（name/scores）和操作（add_score/average）打包在一起"""

    school = "灵兔学院"

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.scores = {}  # 实例属性：每个学生的成绩字典

    def add_score(self, subject, score):
        """添加一门成绩"""
        if not 0 <= score <= 100:
            raise ValueError("分数必须在 0~100 之间")
        self.scores[subject] = score

    def average(self):
        """平均分，没成绩返回 0"""
        if not self.scores:
            return 0
        return sum(self.scores.values()) / len(self.scores)

    def rank(self):
        """等级"""
        avg = self.average()
        if avg >= 90:
            return "优秀"
        if avg >= 80:
            return "良好"
        if avg >= 60:
            return "及格"
        return "不及格"

    def __str__(self):
        # __str__ 决定 print(对象) 显示什么（27 号文件详讲）
        return f"{self.name}({self.student_id}) 平均分 {self.average():.1f} [{self.rank()}]"


stu = Student2("小石", "2608001")
stu.add_score("Python", 88)
stu.add_score("CANoe", 92)
stu.add_score("车载网络", 85)
print(" ", stu)  # 自动调用 __str__
print("  成绩明细：", stu.scores)

# 多个对象各自独立，这就是类的价值：一份代码管很多个体
students = [stu, Student2("老张", "2608002")]
students[1].add_score("Python", 95)
for s in students:
    print(" ", s)


# ===== 练习（取消注释运行）=====
# 1. 写一个 Rectangle 类，有宽高属性，能算面积和周长
# class Rectangle:
#     def __init__(self, w, h):
#         self.w = w
#         self.h = h
#     def area(self):
#         return self.w * self.h
#     def perimeter(self):
#         return 2 * (self.w + self.h)
# r = Rectangle(3, 4)
# print(r.area(), r.perimeter())
#
# 2. 写一个 Counter 类，用类属性统计一共创建了多少个实例
# class Counter:
#     total = 0
#     def __init__(self):
#         Counter.total += 1
# a, b, c = Counter(), Counter(), Counter()
# print(Counter.total)
#
# 3. 用组合写：Computer 类里装 CPU、Memory、Disk 三个类的对象，
#    实现 computer.boot() 依次调用各部件的启动方法
# class CPU:
#     def boot(self): return "CPU 启动"
# class Memory:
#     def boot(self): return "内存自检"
# class Disk:
#     def boot(self): return "磁盘就绪"
# class Computer:
#     def __init__(self):
#         self.parts = [CPU(), Memory(), Disk()]
#     def boot(self):
#         return " -> ".join(p.boot() for p in self.parts)
# print(Computer().boot())
