# -*- coding: utf-8 -*-
# 18. 函数-作用域与闭包
# 知识点：LEGB 查找规则、global、nonlocal、
#        闭包三要素、__closure__ 查看闭包变量、闭包实战（计数器、函数工厂）

# ===== 1. LEGB：Local -> Enclosing -> Global -> Built-in =====
# 变量的作用范围  全局变量  局部变量

# 局部变量只能在函数内使用
x = "全局 G"


def outer():
    x = "外层 E"

    def inner():
        x = "局部 L"
        print("inner 里：", x)  # 局部

    inner()
    print("outer 里：", x)  # 外层


outer()
print("模块里：", x)  # 全局

# Built-in：局部、外层、全局都没有时，去内置命名空间找
print(len("abc"))  # len 就是 B 层


# ==== 2. 函数内给全局变量赋值要加 global 函数内部可以修改全局变量，赋值全局变量  ====

count = 0


def inc_global():
    global count  # 声明：下面这个 count 是模块级的
    count += 1


inc_global()
inc_global()
print("global 计数：", count)  # 2


# 只读取全局变量不需要 global，修改（重新绑定）才需要
PI = 3.14


def area(r):
    return PI * r * r  # 只读，不需要 global


print(area(2))


# 不加 global 又想改，会报 UnboundLocalError
# def wrong():
#     count = count + 1   # 取消注释会报错
# wrong()


# ===== 3. nonlocal：修改外层（非全局）函数的变量 =====

def outer_counter():
    n = 0

    def inner():
        nonlocal n  # 声明：改的是外层函数的 n
        n += 1
        return n

    inner()
    inner()
    return n


print("nonlocal 计数：", outer_counter())  # 2


# ===== 4. 闭包：内层函数 + 引用外层变量 + 外层返回内层函数 =====

def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter  # 返回函数对象（不加括号）


c1 = make_counter()
print(c1(), c1(), c1())  # 1 2 3
c2 = make_counter()  # 新闭包，独立状态
print(c2())  # 1

# 查看闭包捕获的变量
print(c1.__closure__)
print(c1.__closure__[0].cell_contents)  # 3


# ===== 5. 闭包实战：函数工厂 =====

def make_power(n):
    """生成求 n 次方的函数"""
    def power(x):
        return x ** n
    return power


square = make_power(2)
cube = make_power(3)
print(square(4), cube(2))  # 16 8


def make_adder(n):
    return lambda x: x + n


add10 = make_adder(10)
print(add10(5))  # 15


# ===== 6. 闭包实战：带缓存的计算器 =====

def make_calc():
    history = []  # 被闭包记住的列表

    def calc(a, b, op='+'):
        if op == '+':
            r = a + b
        elif op == '-':
            r = a - b
        elif op == '*':
            r = a * b
        else:
            r = a / b
        history.append(f"{a} {op} {b} = {r}")
        return r

    def get_history():
        return history

    return calc, get_history


calc, get_history = make_calc()
calc(1, 2)
calc(5, 3, '-')
calc(4, 6, '*')
print(get_history())


# ===== 7. 嵌套函数不返回出去，就不算闭包 =====

def outer2():
    msg = "只在内部用"

    def inner2():
        print(msg)

    inner2()  # 直接在里面调用，没有返回


outer2()


# ===== 8. ⚠ 循环里创建函数（闭包延迟绑定）=====

funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2]  运行时才去取 i

funcs_ok = [lambda i=i: i for i in range(3)]  # 用默认参数立刻绑定
print([f() for f in funcs_ok])  # [0, 1, 2]


# ===== 练习（取消注释运行）=====
# 1. 用闭包写一个「累加器」：acc(1) -> 1，acc(2) -> 3，acc(3) -> 6
# def make_acc():
#     total = 0
#     def acc(n):
#         nonlocal total
#         total += n
#         return total
#     return acc
# a = make_acc()
# print(a(1), a(2), a(3))
#
# 2. 用闭包写一个 make_multiplier(n)，返回一个把参数乘 n 的函数
# def make_multiplier(n):
#     def mul(x):
#         return x * n
#     return mul
# triple = make_multiplier(3)
# print(triple(7))
#
# 3. 用 global 写一个全局开关 turn_on / turn_off / is_on
# state = False
# def turn_on():
#     global state
#     state = True
# def turn_off():
#     global state
#     state = False
# def is_on():
#     return state
# turn_on(); print(is_on()); turn_off(); print(is_on())
