# -*- coding: utf-8 -*-
# 27. 面向对象-特殊方法与 property
# 知识点：魔术方法（__xx__）总览、__str__ 与 __repr__ 的区别、
#        __len__ / __getitem__ / __setitem__ / __contains__（让对象像容器）、
#        __eq__ / __lt__（比较与排序）、__call__（对象当函数）、
#        __enter__ / __exit__（with 的原理，22 号文件用过）、
#        @property 把方法变属性 + 数据校验、@dataclass 数据类、__slots__
#
# 为什么要学：特殊方法让你自定义的类「长得像内置类型」，
#             能用 len(obj)、obj[0]、for x in obj、sorted(obj) 这些语法。

from dataclasses import dataclass, field

# ==========================================================
# 1. 特殊方法（魔术方法 / dunder methods）是什么
# ==========================================================
# 名字前后各两个下划线的方法，Python 在特定语法下自动调用它们
# 你不需要手动调用，比如：
#   len(obj)      -> 自动调用 obj.__len__()
#   str(obj)      -> obj.__str__()
#   obj[key]      -> obj.__getitem__(key)
#   obj + other   -> obj.__add__(other)
#   for x in obj  -> obj.__iter__()
#   with obj      -> obj.__enter__() / __exit__()
# 这就是「鸭子类型」的底层：有对应方法，就支持对应语法

print("--- 没有特殊方法的类，打印出来很丑 ---")


class PlainPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


p0 = PlainPoint(1, 2)
print("  默认打印：", p0)  # <__main__.PlainPoint object at 0x...>

# ==========================================================
# 2. __str__ 与 __repr__（最常用，必会）
# ==========================================================
print("\n--- __str__ / __repr__ ---")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        # str(obj) 和 print(obj) 时调用
        # 目标：给用户看的，友好、可读
        return f"点({self.x}, {self.y})"

    def __repr__(self):
        # repr(obj) 时调用，交互式环境直接回车、列表里打印对象时也用它
        # 目标：给开发者看的，最好能「复制回代码里重新创建对象」
        return f"Point({self.x}, {self.y})"


p = Point(3, 4)
print("  print/str：", str(p))    # 点(3, 4)
print("  repr：", repr(p))        # Point(3, 4)
print("  在列表里（用 repr）：", [p, p])  # [Point(3, 4), Point(3, 4)]
# 只写 __repr__ 时，__str__ 会默认用它；只写 __str__ 的话 repr 还是丑的
# 经验：至少一个 __repr__，两个都写更好

# ==========================================================
# 3. __len__ / __getitem__ / __setitem__：让对象像容器
# ==========================================================
print("\n--- 容器化方法 ---")


class Playlist:
    """播放列表：自己实现的容器类"""

    def __init__(self, songs=None):
        self._songs = list(songs) if songs else []

    def __len__(self):
        """len(playlist)"""
        return len(self._songs)

    def __getitem__(self, index):
        """playlist[0]、playlist[1:3]"""
        # index 可能是 int，也可能是 slice 对象，都交给底层 list 处理
        return self._songs[index]

    def __setitem__(self, index, value):
        """playlist[0] = '新歌'"""
        self._songs[index] = value

    def __delitem__(self, index):
        """del playlist[0]"""
        del self._songs[index]

    def __contains__(self, item):
        """'歌名' in playlist"""
        return item in self._songs

    def __iter__(self):
        """for song in playlist"""
        return iter(self._songs)  # 直接把迭代权交给内部列表

    def append(self, song):
        self._songs.append(song)

    def __repr__(self):
        return f"Playlist({self._songs!r})"


pl = Playlist(["一路向北", "晴天", "稻香"])
print("  长度 len()：", len(pl))          # __len__
print("  下标 [0]：", pl[0])              # __getitem__
print("  切片 [1:]：", pl[1:])            # __getitem__ + slice
pl[0] = "七里香"                          # __setitem__
print("  改完：", pl)
print("  in 判断：", "晴天" in pl)         # __contains__
print("  遍历：", [s for s in pl])        # __iter__
del pl[2]                                 # __delitem__
print("  删完：", pl)

# ==========================================================
# 4. 算术运算符重载：__add__ / __sub__ / __mul__
# ==========================================================
print("\n--- 运算符重载 ---")


class Vector:
    """二维向量：支持 + - * 和比较"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """v1 + v2"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """v * 3（数乘）"""
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self):
        """abs(v) 返回模长"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


v1, v2 = Vector(1, 2), Vector(3, 4)
print("  加法：", v1 + v2)
print("  减法：", v1 - v2)
print("  数乘：", v1 * 3)
print("  模长：", abs(v1))

# ==========================================================
# 5. __eq__ / __lt__：比较与排序
# ==========================================================
print("\n--- 比较方法 ---")


class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __eq__(self, other):
        """== 比较：这里定义成「分数相同就是同一个水平」"""
        if not isinstance(other, Student):
            return NotImplemented  # 交给 Python 尝试反向运算，最后返回 False
        return self.score == other.score

    def __lt__(self, other):
        """< 比较：按分数排序"""
        return self.score < other.score

    def __hash__(self):
        # ⚠ 定义了 __eq__ 后，__hash__ 会变成 None，对象就不可哈希了
        # 想继续放进 set / 当 dict 的键，必须同时定义 __hash__
        return hash((self.name, self.score))

    def __repr__(self):
        return f"{self.name}({self.score})"


s1, s2, s3 = Student("小石", 88), Student("老张", 95), Student("阿岩", 88)
print("  s1 == s3（同分）：", s1 == s3)
print("  排序：", sorted([s1, s2, s3], reverse=True))  # sorted 用 __lt__
print("  放进 set（需要 __hash__）：", {s1, s2, s3})

# functools.total_ordering 可以只定义 __eq__ + __lt__，自动生成 <= > >=
from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, v):
        self.v = tuple(int(x) for x in v.split("."))

    def __eq__(self, other):
        return self.v == other.v

    def __lt__(self, other):
        return self.v < other.v

    def __repr__(self):
        return ".".join(map(str, self.v))


print("  版本号比较：", Version("1.2.0") > Version("1.10.0"))  # False，1.10 更大

# ==========================================================
# 6. __call__：让对象可以像函数一样被调用
# ==========================================================
print("\n--- __call__ ---")


class Multiplier:
    """可调用对象：比闭包更灵活，因为还能带状态和方法"""

    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        """m(5) 就执行这里"""
        return x * self.factor


double = Multiplier(2)
print("  double(5) =", double(5))  # 对象后面直接加括号
print("  是不是可调用的：", callable(double))  # True


# 带状态的计数器：函数做不到，可调用对象能
class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"   第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)


@CallCounter
def greet(name):
    return f"你好 {name}"


print("  ", greet("小石"))
print("  ", greet("老张"))
print("  总调用次数：", greet.count)

# ==========================================================
# 7. __enter__ / __exit__：with 语句的原理
# ==========================================================
print("\n--- 上下文管理器 ---")


class Timer:
    """计时器：用 with 语句包住一段代码，自动统计耗时
    这就是 22 号文件里 with open(...) 能自动关文件的原理"""

    def __init__(self, label="代码块"):
        self.label = label

    def __enter__(self):
        # 进入 with 块时执行，返回值赋给 as 后面的变量
        import time
        self.start = time.perf_counter()
        return self  # 可以返回自己，也可以返回别的资源对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 离开 with 块时【必定】执行（哪怕中间抛异常）
        import time
        self.cost = time.perf_counter() - self.start
        print(f"   [{self.label}] 耗时 {self.cost * 1000:.3f} ms")
        # 返回 True 表示「异常我已经处理了，别往外抛」；返回 None/False 则继续抛
        if exc_type:
            print(f"   捕获到异常：{exc_type.__name__}: {exc_val}")
        return False  # 不吞异常


with Timer("求和 100 万") as t:
    total = sum(range(1_000_000))

# 标准库简化写法：contextlib.contextmanager 用生成器写，不用写两个方法
from contextlib import contextmanager


@contextmanager
def tag(name):
    print(f"   <{name}>")
    yield  # yield 前面是 __enter__，后面是 __exit__
    print(f"   </{name}>")


with tag("div"):
    print("    内容")

# ==========================================================
# 8. @property：把方法伪装成属性（Python 式的 getter/setter）
# ==========================================================
print("\n--- @property ---")


class Temperature:
    """温度：celsius 是可读写的属性，fahrenheit 是只读的计算属性"""

    def __init__(self, celsius=0):
        # 注意这里赋值会走下面的 setter，自动触发校验
        self.celsius = celsius

    @property
    def celsius(self):
        """读：obj.celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """写：obj.celsius = 25，可以在这里做校验"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度 -273.15℃")
        self._celsius = value

    @property
    def fahrenheit(self):
        """只读属性：没有 setter，就不能赋值"""
        return self._celsius * 9 / 5 + 32


t = Temperature(25)
print("  摄氏度：", t.celsius)        # 像属性一样访问，实际调用了方法
print("  华氏度：", t.fahrenheit)     # 只读计算属性
t.celsius = 100
print("  改成 100 度后华氏度：", t.fahrenheit)
try:
    t.celsius = -300  # 触发 setter 的校验
except ValueError as e:
    print("  校验生效：", e)
# t.fahrenheit = 100  # AttributeError：只读属性不能赋值

# @property 的价值：
#   1. 外部用起来像属性（简洁），内部可以做校验/计算（安全）
#   2. 一开始用普通属性，后来要加校验时改成 property，外部代码不用改


# ==========================================================
# 9. @dataclass：自动生成样板代码（3.7+，写数据类必备）
# ==========================================================
print("\n--- @dataclass ---")


@dataclass
class Product:
    """商品数据类：不用手写 __init__ / __repr__ / __eq__"""

    name: str                      # 类型注解在这里是必须的
    price: float
    quantity: int = 0              # 带默认值

    def total(self):
        """dataclass 里照样能写普通方法"""
        return self.price * self.quantity


# 自动获得的：__init__、__repr__、__eq__
p1 = Product("螺丝", 0.5, 100)
p2 = Product("螺丝", 0.5, 100)
print("  自动 __repr__：", p1)
print("  自动 __eq__：", p1 == p2)  # 值相等就 True（普通类默认比地址）
print("  总价：", p1.total())

# 常用参数：
@dataclass(order=True)      # order=True：自动生成 __lt__ 等，可直接排序
class Task:
    priority: int
    name: str = field(default="未命名")  # field() 可以做更精细的配置
    done: bool = False


tasks = [Task(2, "写文档"), Task(1, "修 BUG"), Task(3, "开会")]
print("  排序：", sorted(tasks))


@dataclass(frozen=True)     # frozen=True：不可变对象（属性只读，可哈希）
class Config:
    host: str
    port: int


cfg = Config("localhost", 8080)
print("  冻结对象：", cfg)
# cfg.port = 90   # FrozenInstanceError
print("  可哈希（能当 dict 键）：", hash(cfg) is not None)


# ==========================================================
# 10. __slots__：限制属性 + 省内存
# ==========================================================
print("\n--- __slots__ ---")


class NormalPoint:
    """普通类：每个对象有一个 __dict__ 字典存属性，灵活但占内存"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SlotPoint:
    """用 __slots__ 声明只能有哪些属性：不生成 __dict__，省内存且防拼错"""
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


sp = SlotPoint(1, 2)
print("  有 __slots__ 的对象没有 __dict__：", not hasattr(sp, "__dict__"))
try:
    sp.z = 3  # AttributeError：z 不在 slots 里
except AttributeError as e:
    print("  拼错属性会被拦下：", e)

# 内存对比（属性越多、对象越多，差别越大）
import sys
n1, n2 = NormalPoint(1, 2), SlotPoint(1, 2)
print(f"  普通对象 {sys.getsizeof(n1) + sys.getsizeof(n1.__dict__)} 字节 "
      f"vs slots 对象 {sys.getsizeof(n2)} 字节")
# 场景：要创建几十万个对象时用 __slots__（比如解析几万条 CAN 报文）

# ==========================================================
# 11. 特殊方法速查表
# ==========================================================
print("\n--- 特殊方法速查 ---")
print("""  创建销毁   __init__  __new__  __del__
  字符串     __str__   __repr__  __format__
  容器       __len__   __getitem__  __setitem__  __delitem__  __contains__  __iter__  __next__
  比较       __eq__  __ne__  __lt__  __le__  __gt__  __ge__  __hash__
  算术       __add__  __sub__  __mul__  __truediv__  __floordiv__  __mod__  __pow__
  反向算术   __radd__（当左操作数不支持时调用）
  调用       __call__
  上下文     __enter__  __exit__
  属性       __getattr__  __setattr__  __getattribute__
  迭代器     __iter__  __next__（生成器见 20 号文件）
""")


# ===== 练习（取消注释运行）=====
# 1. 给 25 号文件的 Student 类加 __str__ 和 __lt__，让它能打印、能排序
# class Student:
#     def __init__(self, name, score):
#         self.name, self.score = name, score
#     def __str__(self): return f"{self.name}:{self.score}"
#     def __lt__(self, other): return self.score < other.score
# print(sorted([Student("b", 90), Student("a", 80)]))
#
# 2. 用 @property 写一个 Circle 类：radius 可读可写（校验 > 0），
#    area / perimeter 只读
# class Circle:
#     def __init__(self, r): self.radius = r
#     @property
#     def radius(self): return self._r
#     @radius.setter
#     def radius(self, v):
#         if v <= 0: raise ValueError("半径必须大于 0")
#         self._r = v
#     @property
#     def area(self): return 3.14159 * self._r ** 2
# c = Circle(2); print(c.area); c.radius = 5; print(c.area)
#
# 3. 写一个 __enter__/__exit__ 的 FileLogger 类，
#    with FileLogger('a.log') as log: log.write('xxx') 自动开关文件
# class FileLogger:
#     def __init__(self, path): self.path = path
#     def __enter__(self):
#         self.f = open(self.path, 'a', encoding='utf-8')
#         return self.f
#     def __exit__(self, *args):
#         self.f.close()
# with FileLogger('test.log') as f:
#     f.write('一行日志\\n')
