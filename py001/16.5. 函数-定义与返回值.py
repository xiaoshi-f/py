# -*- coding: utf-8 -*-
# 16. 函数-定义与返回值
# 知识点：def 定义与调用、命名规范、pass 空函数、文档字符串、
#        单返回值、多返回值（元组解包）、无 return 返回 None、return 提前结束、
#        函数的嵌套调用（函数里调函数、多层调用链、调用栈、函数里定义函数）、
#        传参是「传对象引用」（不可变不受影响 / 可变会被原地修改）

# ===== 1. 最简单的函数 =====

def say_hello():
    print("Hello Python")


say_hello()  # 调用要加括号


# ===== 2. 带参数的函数 =====

def greet(name):
    """向某人打招呼：函数体第一行的字符串就是文档字符串"""
    return f"你好，{name}！"


print(greet("小石"))
print(greet.__doc__)  # 查看文档字符串


# ===== 3. 空函数：函数体不能空着，用 pass 占位 =====

def todo():
    pass


print(todo())  # None


# ===== 4. 返回值：单个值 =====

def add(a, b):
    return a + b


print(add(3, 5))


# ===== 5. 多返回值：本质是返回一个元组，靠解包接收 =====

def calc(a, b):
    """返回和、差、积"""
    return a + b, a - b, a * b


result = calc(10, 4)
print(result)  # (14, 6, 40)  元组

s, d, p = calc(10, 4)  # 元组解包
print(s, d, p)

# 只关心部分结果用 _ 占位
_, _, p2 = calc(10, 4)
print(p2)


# ===== 6. 没有 return / 只有 return：都返回 None =====

def no_return():
    print("我只是打印，没有返回值")


print(no_return())  # None


def empty_return():
    return


print(empty_return())  # None


# ===== 7. return 会立即结束函数 =====

def find_first_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n  # 找到就返回，后面的代码不再执行
    return None  # 循环走完都没找到


print(find_first_even([1, 3, 4, 6]))  # 4
print(find_first_even([1, 3, 5]))  # None


# ===== 8. 函数的嵌套调用：在一个函数内部调用另一个函数 =====
# 这是把大问题拆成小问题的核心手段：每个函数只干一件事，上层负责串起来。


def add_one(x):
    """最底层：只做一件事"""
    return x + 1


def calc_series(nums):
    """中层：调用底层函数"""
    return [add_one(n) for n in nums]  # 在列表推导式里调用 add_one


def report(nums):
    """最上层：调用中层函数"""
    result = calc_series(nums)  # 函数里调函数
    print("加工结果：", result)
    return result


report([1, 2, 3])  # 加工结果：[2, 3, 4]


# 执行顺序：调用 report -> 遇到 calc_series 暂停 -> 进去执行 calc_series
#           -> 遇到 add_one 暂停 -> 进去执行 add_one -> 返回
#           -> 回到 calc_series 继续 -> 返回 -> 回到 report 继续 -> 结束
# 一句话：**遇到函数调用就跳进去，执行完带着返回值回到断点继续往下走。**


# --- 8.1 用 print 把调用过程打出来看清楚 ---

def step_a(n):
    print("    step_a 进入，n =", n)
    r = n * 2
    print("    step_a 返回", r)
    return r


def step_b(n):
    print("  step_b 进入，n =", n)
    r = step_a(n) + 10  # 嵌套调用
    print("  step_b 返回", r)
    return r


def step_c(n):
    print("step_c 进入，n =", n)
    r = step_b(n)  # 嵌套调用
    print("step_c 返回", r)
    return r


step_c(5)
# 输出顺序：
#   step_c 进入，n = 5
#     step_b 进入，n = 5
#       step_a 进入，n = 5
#       step_a 返回 10
#     step_b 返回 20
#   step_c 返回 20
# 注意缩进对应的层级：先进后出，这就是「调用栈」的直观样子。


# --- 8.2 调用栈（call stack）与深度 ---
# Python 每调用一次函数就压一个「栈帧」（frame），返回时弹出。
# 用 sys._getframe() 能看到自己在第几层调用里。

import sys


def level_three():
    # f_back 就是「谁调用了我」，一层层往上找
    depth = 0
    f = sys._getframe()
    while f:
        depth += 1
        f = f.f_back
    print("  level_three 时调用栈深度：", depth)  # 含模块层，一般 = 层数 + 1


def level_two():
    level_three()


def level_one():
    level_two()


level_one()

# 栈深度有上限（默认约 1000 层），嵌套调用太多会 RecursionError。
# 想知道上限：print(sys.getrecursionlimit())   # 1000
# 别改这个数字当作「解决方案」，深嵌套应该改写成循环。


# --- 8.3 嵌套定义：函数里面还能 def 一个函数 ---
# 注意区分两个概念：
#   ① 嵌套「调用」：在函数里调用别的函数（上面的例子）
#   ② 嵌套「定义」：在函数里 def 一个新函数（下面这个）
# 嵌套定义出来的叫「内部函数」，它只在外部函数体内可见，外面直接调会 NameError。

def outer():
    print("outer 开始")

    def inner():  # 定义在 outer 内部
        print("  inner 被调用")

    inner()  # 外层函数内部可以调用它
    inner()
    return "outer 结束"


print(outer())

# inner()  # ❌ 取消注释会报 NameError: name 'inner' is not defined
# 内部函数的作用域只在 outer 的函数体里，外面看不见。
# 想让外面也能用，就把 inner 作为返回值交出去 —— 那就是「闭包」（见 18 号文件）。


# --- 8.4 嵌套调用实战：把一个大任务拆成小函数 ---
# 需求：算一个班级的平均分，并输出最高分学生的名字。

def get_scores():
    """模拟数据源"""
    return {"张三": 88, "李四": 95, "王五": 72}


def calc_average(scores):
    """算平均分：只负责算"""
    return sum(scores.values()) / len(scores)


def find_top(scores):
    """找最高分：只负责找"""
    return max(scores, key=scores.get)  # key 指定比较依据


def make_report(scores):
    """总成：把上面几个串起来"""
    avg = calc_average(scores)          # 嵌套调用 1
    top = find_top(scores)              # 嵌套调用 2
    return f"平均分 {avg:.1f}，最高分是 {top}（{scores[top]}分）"


print(make_report(get_scores()))
# 这种写法的价值：calc_average / find_top 都能单独测试和复用；
# 将来要换数据源，只改 get_scores 一个函数就够。


# ===== 9. 参数传递：传的是对象引用 =====

def change(x, lst):
    x = x + 1  # 重新赋值 = 换绑新对象，外部不受影响
    lst.append(9)  # 调用方法原地修改，外部会变


n = 1
my_list = [1, 2]
change(n, my_list)
print(n)  # 1   没变
print(my_list)  # [1, 2, 9]  变了


# ===== 10. 命名规范与内省属性 =====

def get_user_info():  # snake_case，动词开头
    return "小石"


print(get_user_info.__name__)  # get_user_info
print(get_user_info.__doc__)  # None（没写文档字符串）
print(callable(get_user_info))  # True  判断能不能被调用


# ===== 练习（取消注释运行）=====
# 4. 用嵌套调用写：三个函数 is_even(n) / filter_even(nums) / show(nums)，
#    show 调用 filter_even，filter_even 调用 is_even，最后打印偶数列表
# def is_even(n):
#     return n % 2 == 0
# def filter_even(nums):
#     return [n for n in nums if is_even(n)]
# def show(nums):
#     print("偶数有：", filter_even(nums))
# show(list(range(1, 11)))
#
# 1. 写一个函数 area(r)，返回半径 r 的圆面积（3.14159 * r * r）
# def area(r):
#     return 3.14159 * r * r
# print(area(2))
#
# 2. 写一个函数 swap(a, b)，返回交换后的两个值
# def swap(a, b):
#     return b, a
# x, y = swap(1, 2)
# print(x, y)
#
# 3. 写一个函数 is_prime(n)，判断 n 是不是质数，返回 True / False
# def is_prime(n):
#     if n < 2:
#         return False
#     for i in range(2, int(n ** 0.5) + 1):
#         if n % i == 0:
#             return False
#     return True
# print([i for i in range(20) if is_prime(i)])

# 案例 ====计算传入字符串元音字母个数
def count_aeiou(s):
    num=0
    for i in s:
        if i in "aeiouAEIOU":
            num += 1
    return num
print(count_aeiou("nihaowoshishijianing"))
