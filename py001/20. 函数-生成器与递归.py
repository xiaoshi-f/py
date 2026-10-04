# -*- coding: utf-8 -*-
# 20. 函数-生成器与递归
# 知识点：yield、生成器是惰性迭代器、生成器只能遍历一次、生成器表达式、
#        yield from、send / throw / close、递归三要素、递归深度限制

import sys

# ===== 1. 第一个生成器：带 yield 的函数 =====


def countdown(n):
    while n > 0:
        yield n  # 产出一个值，函数在这里「暂停」
        n -= 1


g = countdown(3)
print(g)  # <generator object ...>  调用不会立即执行
print(next(g))  # 3
print(next(g))  # 2
print(next(g))  # 1
# print(next(g))  # StopIteration：已经产完了

for x in countdown(3):  # 重新创建一个生成器
    print(x)


# ===== 2. return 列表 vs yield：内存差别 =====

def get_list(n):
    result = []
    for i in range(n):
        result.append(i)
    return result


def get_gen(n):
    for i in range(n):
        yield i


big_list = get_list(10)
print("列表：", big_list)

gen = get_gen(10)
print("生成器前 3 个：", next(gen), next(gen), next(gen))

# 生成器表达式：和列表推导式只差一个括号
squares_gen = (x * x for x in range(10))
print("生成器表达式求和：", sum(squares_gen))

# 不建中间列表，省内存
print(sum(x * x for x in range(1_000_000)))


# ===== 3. 生成器只能遍历一次 =====

g2 = (x for x in range(3))
print(list(g2))  # [0, 1, 2]
print(list(g2))  # []  已经耗尽


# ===== 4. yield from：把产出委派给别的生成器 =====

def chain(*iterables):
    for it in iterables:
        yield from it  # 等价于 for x in it: yield x


print(list(chain([1, 2], [3, 4], 'ab')))  # [1, 2, 3, 4, 'a', 'b']


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


print(list(flatten([1, [2, [3, 4]], 5])))  # [1, 2, 3, 4, 5]


# ===== 5. 生成器进阶：send / throw / close =====

def echo():
    print("  启动")
    while True:
        received = yield  # yield 在右边：接收 send 进来的值
        print("  收到：", received)


e = echo()
next(e)  # 必须先启动（预激）到第一个 yield
e.send(10)
e.send("hello")
e.close()  # 关闭生成器


# ===== 6. 生成器实战：读大文件、无限序列 =====

def fibonacci_infinite():
    """无限斐波那契序列"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


f = fibonacci_infinite()
print([next(f) for _ in range(10)])


def take(n, iterable):
    """从 iterable 里取前 n 个"""
    count = 0
    for item in iterable:
        if count >= n:
            break
        yield item
        count += 1


print(list(take(5, fibonacci_infinite())))


# ===== 7. 递归：终止条件 + 递推关系 =====

def factorial(n):
    if n <= 1:  # 终止条件
        return 1
    return n * factorial(n - 1)  # 递推


print("5! =", factorial(5))


def rsum(n):
    """1 + 2 + ... + n"""
    return 1 if n == 1 else n + rsum(n - 1)


print("1..100 求和 =", rsum(100))


def reverse_str(s):
    return s if len(s) <= 1 else reverse_str(s[1:]) + s[0]


print(reverse_str("hello"))


# ===== 8. 递归深度限制 =====

print("递归上限：", sys.getrecursionlimit())  # 默认 1000


def deep(n):
    if n == 0:
        return 0
    return 1 + deep(n - 1)


print(deep(500))  # 没问题
# print(deep(2000))    # RecursionError：栈深度超了

# ⚠ 注意：lru_cache 只减少「重复计算」，不减少递归栈深度
# 下面这样写 2000 层照样 RecursionError
from functools import lru_cache


@lru_cache
def deep_cached(n):
    return 0 if n == 0 else 1 + deep_cached(n - 1)


print(deep_cached(500))  # 可以
# print(deep_cached(2000))   # 依然 RecursionError

# 方案一：临时调高上限（改太大可能直接崩溃）
sys.setrecursionlimit(3000)
print(deep(2000))
sys.setrecursionlimit(1000)


# 方案二（推荐）：能改循环就改循环，Python 没有尾递归优化
def deep_loop(n):
    total = 0
    for _ in range(n):
        total += 1
    return total


print(deep_loop(100000))  # 随便多大都没事


# ===== 练习（取消注释运行）=====
# 1. 写一个生成器 my_range(start, end, step=1)
# def my_range(start, end, step=1):
#     cur = start
#     while cur < end:
#         yield cur
#         cur += step
# print(list(my_range(1, 10, 2)))
#
# 2. 写一个生成器，产出某个目录下所有文件名（用 os.walk）
# import os
# def all_files(path):
#     for root, dirs, files in os.walk(path):
#         for name in files:
#             yield os.path.join(root, name)
# print(list(take(10, all_files('.'))))
#
# 3. 用递归实现：判断字符串是否是回文
# def is_palindrome(s):
#     if len(s) <= 1:
#         return True
#     if s[0] != s[-1]:
#         return False
#     return is_palindrome(s[1:-1])
# print(is_palindrome("level"), is_palindrome("hello"))
