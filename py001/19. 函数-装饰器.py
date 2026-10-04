# -*- coding: utf-8 -*-
# 19. 函数-装饰器
# 知识点：装饰器本质、@ 语法糖、functools.wraps、带参装饰器、多个装饰器顺序、
#        类装饰器、内置装饰器（lru_cache / property / staticmethod / classmethod）、
#        实战：计时器 + 日志 + 重试

import time
from functools import wraps, lru_cache


# ===== 1. 装饰器本质：接收函数、返回函数的高阶函数 =====

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}，参数 {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] 返回 {result}")
        return result
    return wrapper


def add(a, b):
    """加法"""
    return a + b


# 不用 @ 的等价写法
decorated = logger(add)
print(decorated(1, 2))


# 用 @ 语法糖
@logger
def add2(a, b):
    return a + b


print(add2(3, 4))
print("-" * 40)


# ===== 2. 不加 wraps 会丢元信息 =====

def bad_deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def good_deco(func):
    @wraps(func)  # 把 __name__ / __doc__ 拷回来
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@bad_deco
def f1():
    """我是 f1"""


@good_deco
def f2():
    """我是 f2"""


print(f1.__name__, "|", f1.__doc__)  # wrapper | None
print(f2.__name__, "|", f2.__doc__)  # f2 | 我是 f2
print("-" * 40)


# ===== 3. 带参数的装饰器：三层嵌套 =====

def repeat(times):
    """让函数重复执行 times 次"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)
def hello():
    print("Hello")


hello()
print("-" * 40)


# ===== 4. 多个装饰器的执行顺序 =====

def deco_a(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("A 前")
        r = func(*args, **kwargs)
        print("A 后")
        return r
    return wrapper


def deco_b(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("B 前")
        r = func(*args, **kwargs)
        print("B 后")
        return r
    return wrapper


@deco_a
@deco_b
def target():
    print("  目标函数执行")


# 装饰时自下而上：target = deco_a(deco_b(target))
target()
print("-" * 40)


# ===== 5. 实战：计时装饰器 =====

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        cost = time.perf_counter() - start
        print(f"[TIME] {func.__name__} 耗时 {cost * 1000:.3f} ms")
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


print(slow_sum(1_000_000))
print("-" * 40)


# ===== 6. 实战：重试装饰器 =====

def retry(times=3, exc=Exception):
    """失败自动重试 times 次"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exc as e:
                    print(f"[RETRY] 第 {i} 次失败：{e}")
                    if i == times:
                        raise
        return wrapper
    return decorator


attempt = {'n': 0}


@retry(times=3)
def unstable():
    attempt['n'] += 1
    if attempt['n'] < 3:
        raise ValueError("网络抖动")
    return "成功了"


print(unstable())
print("-" * 40)


# ===== 7. lru_cache：结果缓存（记忆化）=====

@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(100))  # 不加缓存算到天荒地老
print(fib.cache_info())
fib.cache_clear()  # 清空缓存


# 注意：参数必须可哈希（能用 list -> 改 tuple）
@lru_cache
def calc_cached(a, b):
    print("  真的在计算...")
    return a + b


print(calc_cached(1, 2))
print(calc_cached(1, 2))  # 直接走缓存，不再打印
print("-" * 40)


# ===== 8. 类装饰器（用类实现装饰器）=====

class CountCalls:
    """统计函数被调用了多少次"""

    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[COUNT] 第 {self.count} 次调用")
        return self.func(*args, **kwargs)


@CountCalls
def say_hi():
    return "hi"


say_hi()
say_hi()
print("-" * 40)


# ===== 9. 内置装饰器：property / staticmethod / classmethod =====

class Circle:
    def __init__(self, r):
        self._r = r

    @property
    def area(self):
        """像属性一样访问：c.area"""
        return 3.14159 * self._r ** 2

    @staticmethod
    def describe():
        return "我是一个圆"

    @classmethod
    def unit(cls):
        return cls(1)


c = Circle(2)
print(c.area)  # 不用加括号
print(Circle.describe())
print(Circle.unit().area)


# ===== 练习（取消注释运行）=====
# 1. 写一个装饰器，在函数抛出异常时打印「出错了」并吞掉异常返回 None
# def safe(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print("出错了：", e)
#             return None
#     return wrapper
#
# @safe
# def div(a, b):
#     return a / b
# print(div(1, 0))
#
# 2. 写一个带参数装饰器 tag(msg)，在原函数返回值前面加上 msg
# def tag(msg):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             return msg + str(func(*args, **kwargs))
#         return wrapper
#     return decorator
#
# @tag("[结果] ")
# def get_name():
#     return "小石"
# print(get_name())
#
# 3. 用 @lru_cache 优化递归阶乘，算 factorial(500)
# @lru_cache
# def factorial(n):
#     return 1 if n <= 1 else n * factorial(n - 1)
# print(factorial(500))
