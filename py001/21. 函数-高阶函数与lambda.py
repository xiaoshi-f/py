# -*- coding: utf-8 -*-
# 21. 函数-高阶函数与lambda
# 知识点：函数是一等公民（赋值/入参/返回/存容器）、lambda 语法与限制、延迟绑定坑、
#        map / filter / reduce / sorted / zip / enumerate / any / all、
#        functools.partial 偏函数、类型注解

from functools import reduce, partial

# ===== 1. 函数是一等公民 =====


def add(a, b):
    return a + b


f = add  # 赋值给变量（不加括号）
print(f(1, 2))  # 3

funcs = [add, len, max]  # 放进容器
print(funcs[0](1, 2), funcs[1]("hello"))


def apply(func, a, b):  # 函数作为参数（回调）
    return func(a, b)


print(apply(add, 3, 4))  # 7


def choose(op):  # 函数作为返回值
    if op == '+':
        return add
    return lambda a, b: a - b


print(choose('+')(5, 2), choose('-')(5, 2))


# ===== 2. lambda 匿名函数：lambda 参数: 单个表达式 =====

square = lambda x: x ** 2
print(square(5))  # 25

print((lambda a, b: a + b)(1, 2))  # 立即调用

# 只能写一个表达式，不能有语句
is_even = lambda x: "偶" if x % 2 == 0 else "奇"  # 三元可以
print(is_even(3))


# lambda 也能形成闭包
def make_incrementor(n):
    return lambda x: x + n


inc10 = make_incrementor(10)
print(inc10(5))  # 15


# ===== 3. ⚠ lambda 的延迟绑定坑 =====

funcs_bad = [lambda: i for i in range(3)]
print([f() for f in funcs_bad])  # [2, 2, 2]

funcs_ok = [lambda i=i: i for i in range(3)]  # 默认参数立刻绑定
print([f() for f in funcs_ok])  # [0, 1, 2]


# ===== 4. map：对每个元素做变换 =====

nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, nums)))  # [2, 4, 6, 8]
print(list(map(str, nums)))  # ['1', '2', '3', '4']
print(list(map(pow, [1, 2, 3], [2, 3, 4])))  # 多序列并行：1^2, 2^3, 3^4

# 列表推导式通常更直观
print([x * 2 for x in nums])


# ===== 5. filter：保留为真的元素 =====

print(list(filter(lambda x: x % 2 == 0, nums)))  # [2, 4]
print(list(filter(None, [0, 1, '', 'a', None])))  # [1, 'a']  去掉假值
print([x for x in nums if x % 2 == 0])


# ===== 6. reduce：累积成单个值 =====

print(reduce(lambda a, b: a + b, nums))  # 10
print(reduce(lambda a, b: a + b, nums, 100))  # 110  带初始值
print(reduce(lambda a, b: a if a > b else b, nums))  # 最大值 4


# ===== 7. sorted 与 sort：自定义排序 =====

words = ["banana", "apple", "cherry", "date"]
print(sorted(words))  # 默认字典序
print(sorted(words, key=len))  # 按长度
print(sorted(words, key=lambda w: (len(w), w)))  # 多级排序
print(sorted(words, key=len, reverse=True))

students = [("小石", 88), ("老张", 95), ("阿岩", 88)]
print(sorted(students, key=lambda s: (-s[1], s[0])))  # 分数降序，同分按名字

lst = [3, 1, 2]
lst.sort()  # 原地排序，改原列表，返回 None
print(lst)
print(sorted(lst))  # 返回新列表，不动原数据


# ===== 8. zip / enumerate =====

names = ["小石", "老张"]
scores = [88, 95]
print(list(zip(names, scores)))  # [('小石', 88), ('老张', 95)]
print(dict(zip(names, scores)))  # {'小石': 88, '老张': 95}
print(list(zip("abc", [1, 2])))  # 最短的为准：[('a', 1), ('b', 2)]

for i, v in enumerate(["a", "b", "c"], start=1):
    print(i, v)

# 用 zip 做矩阵转置
matrix = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*matrix)))  # [(1, 4), (2, 5), (3, 6)]


# ===== 9. any / all =====

print(any([0, "", 3]))  # True  有一个为真
print(all([1, "a", 3]))  # True
print(all([1, "", 3]))  # False


# ===== 10. functools.partial：固定部分参数 =====

pow2 = partial(pow, exp=2)
print(pow2(5))  # 25

int2 = partial(int, base=2)  # 把二进制字符串转整数
print(int2("1010"))  # 10


# ===== 11. 类型注解 =====

def greet(name: str) -> str:
    return f"你好，{name}"


def process(items: list[int]) -> dict[str, int]:  # 内置泛型，3.9+
    return {"sum": sum(items), "count": len(items)}


def parse(data: str | bytes) -> None:  # 联合类型，3.10+
    print(type(data))


print(greet("小石"))
print(process([1, 2, 3]))
print(greet.__annotations__)  # {'name': <class 'str'>, 'return': <class 'str'>}

# 注解只是标记，运行时不校验
print(greet(123))  # 传数字也不会报错（靠 mypy / pyright 静态检查）


def apply_typed(func, a: int, b: int) -> int:
    return func(a, b)


print(apply_typed(add, 1, 2))


# ===== 练习（取消注释运行）=====
# 1. 用 sorted + lambda 把字符串列表按「元音字母个数」降序排
# def count_vowel(s):
#     return sum(1 for ch in s.lower() if ch in 'aeiou')
# ws = ['banana', 'apple', 'sky', 'cherry']
# print(sorted(ws, key=count_vowel, reverse=True))
#
# 2. 用 map + filter 一句话：把 1~20 中 3 的倍数的平方算出来
# print(list(map(lambda x: x * x, filter(lambda x: x % 3 == 0, range(1, 21)))))
#
# 3. 用 reduce 把 ['a', 'b', 'c'] 拼成 'a-b-c'
# print(reduce(lambda a, b: f"{a}-{b}", ['a', 'b', 'c']))
