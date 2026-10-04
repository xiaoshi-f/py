# -*- coding: utf-8 -*-
# 16. 函数-定义与返回值
# 知识点：def 定义与调用、命名规范、pass 空函数、文档字符串、
#        单返回值、多返回值（元组解包）、无 return 返回 None、return 提前结束、
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
# 圆的面积
def circle_area(r):
    d = 3.14 * r * r
    return d
print(circle_area(10))

# ===== 3. 空函数：函数体不能空着，用 pass 占位 =====

def todo():
    pass


print(todo())  # None


# ===== 4. 返回值：单个值 =====
# 长方形
def add(a, b):
    return a * b


print(add(3, 5))




# ===== 5. 多返回值：本质是返回一个元组，靠解包接收 =====

def calc(a, b):
    """返回和、差、积"""
    return a + b, a - b, a * b

result = calc(10, 4)
print(result)  # (14, 6, 40)  元组

s, d, p = calc(10, 4)  # 元组解包
print(s, d, p)
# round(3.141515926 * 2 * 2, 5)四舍五入 ,5位小数
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


# ===== 8. 参数传递：传的是对象引用 =====

def change(x, lst):
    x = x + 1  # 重新赋值 = 换绑新对象，外部不受影响
    lst.append(9)  # 调用方法原地修改，外部会变


n = 1
my_list = [1, 2]
change(n, my_list)
print(n)  # 1   没变
print(my_list)  # [1, 2, 9]  变了


# ===== 9. 命名规范与内省属性 =====

def get_user_info():  # snake_case，动词开头
    return "小石"


print(get_user_info.__name__)  # get_user_info
print(get_user_info.__doc__)  # None（没写文档字符串）
print(callable(get_user_info))  # True  判断能不能被调用


# 嵌套调用


# ===== 练习（取消注释运行）=====
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
