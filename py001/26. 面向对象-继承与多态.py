# -*- coding: utf-8 -*-
# 26. 面向对象-继承与多态
# 知识点：单继承、方法重写、super()、多继承与 MRO、
#        isinstance / issubclass 类型判断、多态（鸭子类型）、
#        抽象基类 ABC + @abstractmethod、组合优于继承、
#        ⚠ 继承的常见坑
#
# 为什么要学：继承用来「复用 + 扩展」已有类的代码。
#             比如写了 Animal，Dog/Cat 直接继承，只写自己不一样的部分。

from abc import ABC, abstractmethod

# ==========================================================
# 1. 最基础的继承
# ==========================================================
print("--- 继承基础 ---")


class Animal:
    """父类（基类）：抽取所有动物共有的东西"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        return f"{self.name} 在吃东西"

    def sleep(self):
        return f"{self.name} 在睡觉"

    def speak(self):
        """父类只定义接口，具体叫声由子类实现"""
        return "（动物叫声）"


# class 子类(父类)：就继承了父类的所有属性和方法
class Dog(Animal):
    """子类（派生类）：继承 Animal，再加自己的东西"""

    def __init__(self, name, age, breed):
        # super() 拿到父类，调用父类的 __init__ 初始化共有属性
        # 不用 super 的话就得写 Animal.__init__(self, name, age)，不推荐
        super().__init__(name, age)
        self.breed = breed  # 子类自己的属性

    def speak(self):
        """方法重写（Override）：子类重新实现父类的方法"""
        return f"{self.name}：汪汪！"

    def fetch(self):
        """子类新增的方法，父类没有"""
        return f"{self.name} 去捡球了"


class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def speak(self):
        return f"{self.name}：喵喵~"


dog = Dog("旺财", 3, "金毛")
cat = Cat("咪咪", 2)

print(" ", dog.eat())       # 继承自父类，子类没写但能用
print(" ", dog.speak())     # 子类重写过的版本
print(" ", dog.fetch())     # 子类独有
print(" ", cat.speak())     # 另一个子类的实现
print("  类型：", type(dog).__name__, "| 是不是 Animal：", isinstance(dog, Animal))

# ==========================================================
# 2. 方法查找顺序：先看子类，再看父类
# ==========================================================
print("\n--- 查找顺序 ---")
# 调用 dog.speak() 时：
#   1. 在 Dog 类里找 speak -> 找到了，用 Dog 的
#   2. 如果 Dog 没有，去 Animal 里找
#   3. 再没有，去 object（所有类的祖宗）里找
#   4. 还没有 -> AttributeError
# 查看顺序：类名.__mro__ 或 类名.mro()
print("  Dog 的 MRO：", [c.__name__ for c in Dog.__mro__])

# 子类里想「扩展」而不是「完全替换」父类方法，用 super() 调父类版本
class LoudDog(Dog):
    def speak(self):
        base = super().speak()  # 拿到父类的结果
        return base.upper() + "!!!"  # 在父类基础上加工


print(" ", LoudDog("大嗓门", 2, "哈士奇").speak())

# ==========================================================
# 3. super() 详解
# ==========================================================
print("\n--- super() ---")


class Vehicle:
    def __init__(self, brand):
        self.brand = brand
        print(f"    Vehicle.__init__({brand})")

    def info(self):
        return f"品牌：{self.brand}"


class Car(Vehicle):
    def __init__(self, brand, doors):
        # super() 的完整写法其实是 super(Car, self)，Python 3 可以简写
        super().__init__(brand)   # 必须先初始化父类部分
        self.doors = doors
        print(f"    Car.__init__ 加了 doors={doors}")

    def info(self):
        # 复用父类的 info，再追加自己的信息
        return super().info() + f"，{self.doors} 门"


class ElectricCar(Car):
    def __init__(self, brand, doors, battery):
        super().__init__(brand, doors)  # 一层层往上传递
        self.battery = battery

    def info(self):
        return super().info() + f"，电池 {self.battery}kWh"


ecar = ElectricCar("比亚迪", 4, 60)
print("  ", ecar.info())
# super() 的好处：改父类名字时不用改子类代码；多继承时能按 MRO 正确协作

# ==========================================================
# 4. 多态：同一接口，不同实现
# ==========================================================
print("\n--- 多态 ---")
# 多态 = 调用方只管调用 speak()，不用管对方到底是狗还是猫
# Python 的多态是「鸭子类型」：
#   "如果它走起来像鸭子、叫起来像鸭子，那它就是鸭子"
#   不要求有共同父类，只要有同名方法就行！


def animal_concert(animals):
    """让所有动物依次叫一声：完全不关心具体类型"""
    for a in animals:
        print("   ", a.speak())  # 每个对象按自己的实现来


animal_concert([dog, cat, LoudDog("阿黄", 1, "土狗")])

# 鸭子类型演示：下面这几个类没有任何继承关系，但都有 speak()，就能一起用
class Robot:
    def speak(self):
        return "机器人：哔——"


class Speaker:
    def speak(self):
        return "音箱：播放音乐"


print("  鸭子类型（无继承也能多态）：")
animal_concert([dog, Robot(), Speaker()])  # 照样能跑

# ==========================================================
# 5. isinstance 与 issubclass
# ==========================================================
print("\n--- 类型判断 ---")
print("  isinstance(dog, Dog)：", isinstance(dog, Dog))      # True
print("  isinstance(dog, Animal)：", isinstance(dog, Animal))  # True，子类也是父类的实例
print("  isinstance(dog, Cat)：", isinstance(dog, Cat))      # False
print("  isinstance(dog, object)：", isinstance(dog, object))  # True，万物皆 object
print("  issubclass(Dog, Animal)：", issubclass(Dog, Animal))  # True
print("  type(dog) == Dog：", type(dog) == Dog)  # True，但 type 不认继承关系
# 判断类型优先用 isinstance（认继承），type() 只在严格比较时用

# ==========================================================
# 6. 抽象基类 ABC：强制子类必须实现某些方法
# ==========================================================
print("\n--- 抽象基类 ABC ---")


class Shape(ABC):
    """图形抽象基类：自己不能实例化，只定义「子类必须有哪些能力」"""

    @abstractmethod
    def area(self):
        """子类必须实现求面积"""
        pass

    @abstractmethod
    def perimeter(self):
        """子类必须实现求周长"""
        pass

    # 抽象类里也可以有普通方法，子类直接继承
    def describe(self):
        return f"这是一个面积为 {self.area():.2f} 的图形"


# shape = Shape()   # TypeError：抽象类不能实例化

class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14159 * self.r ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.r


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)


# 如果子类没实现所有 abstractmethod，实例化时会报错
class Triangle(Shape):
    def area(self):
        return 0  # 只实现了一个，perimeter 没有


try:
    Triangle()
except TypeError as e:
    print("  缺方法会被拦下：", str(e)[:60], "...")

shapes = [Circle(2), Rectangle(3, 4)]
for s in shapes:
    print(f"   {type(s).__name__}：面积 {s.area():.2f}，周长 {s.perimeter():.2f}，{s.describe()}")

# ==========================================================
# 7. 多继承与 MRO（菱形继承问题）
# ==========================================================
print("\n--- 多继承 ---")


class A:
    def hello(self):
        return "A 的 hello"


class B(A):
    def hello(self):
        return "B 的 hello"


class C(A):
    def hello(self):
        return "C 的 hello"


class D(B, C):
    # 同时继承 B 和 C，这叫菱形继承
    # D.hello 该用谁的？按 MRO（C3 线性化）来：D -> B -> C -> A -> object
    pass


d = D()
print("  D 的 hello：", d.hello())  # B 的 hello（B 写在前面，优先级高）
print("  D 的 MRO：", [c.__name__ for c in D.__mro__])

# 多继承里用 super() 能实现「协作式调用」，每个类都把请求往 MRO 下一级传
class LogMixin:
    """混入类（Mixin）：给别的类加日志能力，不单独使用"""

    def log(self, msg):
        print(f"   [LOG][{type(self).__name__}] {msg}")


class JsonMixin:
    """混入类：给别的类加 JSON 序列化能力"""

    def to_json(self):
        import json
        return json.dumps(vars(self), ensure_ascii=False)


class User(LogMixin, JsonMixin):
    """通过 Mixin 组合出功能，比深继承树灵活得多"""

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.log(f"创建用户 {name}")  # 来自 LogMixin


u = User("小石", 25)
print("  ", u.to_json())  # 来自 JsonMixin

# ==========================================================
# 8. ⚠ 继承的坑
# ==========================================================
print("\n--- 继承常见坑 ---")

# 坑1：子类忘了调 super().__init__，父类的属性就没初始化
class BadChild(Animal):
    def __init__(self, name):
        self.name = name  # 没调 super().__init__，age 属性没建


bc = BadChild("测试")
print("  没调 super 的后果：hasattr(age) =", hasattr(bc, "age"))
# print(bc.sleep())  # 能跑（只用 name），但 bc.age 不存在，迟早出错

# 坑2：可变类属性被所有子类共享（见 25 号文件）
class Base:
    items = []


class ChildA(Base):
    pass


class ChildB(Base):
    pass


ChildA.items.append("x")
print("  可变类属性共享：ChildB.items =", ChildB.items)  # 也被改了

# 坑3：继承层级太深（超过 3 层就该考虑用组合了）
# 深继承树的问题是：改一个父类，所有子类都受影响，牵一发动全身

# ==========================================================
# 9. 组合优于继承（重要设计原则）
# ==========================================================
print("\n--- 组合 vs 继承 ---")
# 继承表达 is-a：狗是一种动物
# 组合表达 has-a：车有一个发动机
# 经验法则：
#   - 子类真的「是」父类的一种，且要复用大部分行为 -> 用继承
#   - 只是想借用某些功能 -> 用组合或 Mixin
#   - 拿不准 -> 用组合，组合的耦合度低，改起来不容易炸


class Stack:
    """栈：用组合（内部装一个 list）而不是继承 list"""

    def __init__(self):
        self._items = []  # 组合：内部持有列表对象

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()

    def __len__(self):
        return len(self._items)


# 如果写成 class Stack(list)，用户就能调用 stack.insert/sort/reverse，
# 这些操作会破坏「栈只能从顶部操作」的约束 —— 这就是继承的副作用
st = Stack()
st.push(1)
st.push(2)
print("  栈顶：", st.pop(), "| 剩余长度：", len(st))

# ==========================================================
# 10. 实战：车载方向的继承示例（ECU 报文处理）
# ==========================================================
print("\n--- 实战：ECU 类体系 ---")


class ECU(ABC):
    """ECU 抽象基类（车载：IVI / DHU / CDC / BCM / ADCU / VCU 都是 ECU）"""

    def __init__(self, name, can_id):
        self.name = name
        self.can_id = can_id  # CAN 报文 ID
        self.online = False

    @abstractmethod
    def domain(self):
        """返回所属域，子类必须实现"""
        pass

    def power_on(self):
        self.online = True
        return f"{self.name}(0x{self.can_id:X}) 上电"

    def info(self):
        return f"[{self.domain()}] {self.name} CAN_ID=0x{self.can_id:X} 在线={self.online}"


class IVI(ECU):
    """车载信息娱乐"""

    def domain(self):
        return "座舱域"


class BCM(ECU):
    """车身控制模块"""

    def domain(self):
        return "车身域"


class VCU(ECU):
    """整车控制器"""

    def domain(self):
        return "动力域"


# 多态：统一处理不同域的 ECU
ecus = [IVI("中控屏", 0x123), BCM("车身控制器", 0x456), VCU("整车控制器", 0x789)]
for e in ecus:
    e.power_on()
    print("  ", e.info())

# 统计某个域有几个 ECU（多态带来的便利）
from collections import Counter
print("  各域数量：", dict(Counter(e.domain() for e in ecus)))


# ===== 练习（取消注释运行）=====
# 1. 写一个 Employee 基类，Manager / Developer 继承它，各自重写 work() 方法
# class Employee(ABC):
#     def __init__(self, name):
#         self.name = name
#     @abstractmethod
#     def work(self): ...
# class Manager(Employee):
#     def work(self): return f"{self.name} 在开会"
# class Developer(Employee):
#     def work(self): return f"{self.name} 在写代码"
# for e in [Manager("李"), Developer("小石")]:
#     print(e.work())
#
# 2. 用 ABC 定义一个 DataSource 抽象类（必须实现 read()），
#    再写 FileSource / MemorySource 两个子类
# class DataSource(ABC):
#     @abstractmethod
#     def read(self): ...
# class MemorySource(DataSource):
#     def __init__(self, data): self.data = data
#     def read(self): return self.data
# print(MemorySource("hello").read())
#
# 3. 写个 Mixin：给任意类加 __repr__，返回 "类名(属性=值)"
# class ReprMixin:
#     def __repr__(self):
#         args = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
#         return f"{type(self).__name__}({args})"
# class Point(ReprMixin):
#     def __init__(self, x, y): self.x, self.y = x, y
# print(repr(Point(1, 2)))
