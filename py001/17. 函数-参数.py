# -*- coding: utf-8 -*-
# 17. 函数-参数
# 知识点：位置参数、关键字参数、默认参数、可变默认值陷阱、
#        *args 收集位置参数、**kwargs 收集关键字参数、
#        仅位置参数 / 、仅关键字参数 * 、参数解包 * 和 **
from functools import total_ordering
from itertools import count

import args


# ===== 1. 位置参数与关键字参数 =====

def parrot(voltage, state='僵硬的', action='voom'):
    print(f"电压 {voltage}，状态 {state}，动作 {action}")


parrot(1000)  # 全位置
parrot(voltage=1000)  # 全关键字传参
parrot(action='VOOOOM', voltage=1000)  # 关键字顺序随意
parrot(1000, action='VOOOOM')  # 位置在前，关键字在后



# ===== 2. 默认参数 =====

def ask_ok(prompt, retries=4, reminder='请重新输入'):
    print(f"提示：{prompt}（剩余次数 {retries}，失败提示：{reminder}）")


ask_ok("确定退出吗？")
ask_ok("确定覆盖文件吗？", 2)
ask_ok("确定覆盖文件吗？", 2, "只能输入 yes / no")


# ===== 3. ⚠ 可变默认值陷阱 =====
# 默认值在函数「定义时」求值一次，之后所有调用共享同一个对象

def bad(a, L=[]):  # 错误写法
    L.append(a)
    return L


print(bad(1))  # [1]
print(bad(2))  # [1, 2]   列表被复用了！


def good(a, L=None):  # 正确写法
    if L is None:
        L = []
    L.append(a)
    return L


print(good(1))  # [1]
print(good(2))  # [2]


# ===== 4. 默认值在定义处求值 =====

i = 5


def f(arg=i):
    print(arg)


i = 6
f()  # 打印 5，不是 6


# ===== 5. *args：收集多余的位置参数（元组）不定长参数 =====

def my_sum(*args):
    print("args 是元组：", args)
    return sum(args)


print(my_sum(1, 2, 3))
print(my_sum(1, 2, 3, 4, 5))


# *args 后面还能跟别的参数，但那些参数必须用关键字传
def concat(*args, sep='/'):
    return sep.join(args)


print(concat("地球", "火星", "金星"))  # 地球/火星/金星
print(concat("地球", "火星", "金星", sep='.'))  # 地球.火星.金星


# ===== 6. **kwargs：收集多余的关键字参数（字典）不定长参数 =====

def cheeseshop(kind, *arguments, **keywords):
    print("种类：", kind)
    print("额外位置参数：", arguments)
    print("额外关键字参数：", keywords)


cheeseshop("切达干酪", "很稀", "非常稀",
           shopkeeper="老张", client="小石")


#函数的参数类型   普通参数   特殊:函数
def add(a, b):
  return a + b    # 函数
def subtract(a, b,per):
    return per(a,b)
print(subtract(1, 2,add))# 调用add函数

#匿名函数  lambda 参数列表 ：函数体     简单的函数
out = lambda : print("---------------")
add =lambda a , b  : a+b
out()
print(add(1, 2))

# 打印分割线
def o():
    print('--------------')
o()# 调用这个函数
a = lambda : print('----------------------')
a()  #调用匿名函数
# 计算两个数之和
s= lambda x, y: x+y #  s定义变量 才可调用
print(s(100,200))

# 排序.sort  kiy    reveres正序倒序排序
d = ["ccfghdhgfsdgfgdf","ADADA","adaawdqw","Adsahgfcshjka"]
print(d)
d.sort(key=lambda item: len(item))# 长度排序
print(d)
# 定义函数的阶乘  计算结果  计算n的阶乘    一定要有终结点
def jc(n):
    if n == 1:
        return 1
    else:
        return n*jc(n-1)

a=jc(int(input()))
print(a)


 # 电商订单计算器功能（商品信息，数量，价格）（优惠，优惠券，积分抵扣）运费信息
 # 优惠券满5000以后用,优惠券价格不超过商品总价
 # 积分满5000以后用,100积分抵扣1元(整百抵扣)抵扣金额不超过商品总价
def jisun(coupon,score,espress,*args):
    # 设置默认值 无传输不报错
    """
    :param args: （商品名称，数量goods[1]，价格goods[2]）args  goods[1] * goods[2]
    :param coupon:优惠券
    :param score:积分
    :param espress:运费
    :return:订单总金额
    订单用金额=商品总金额-优惠券-积分+运费
    """
    # 1,商品总金额每一个商品 价格*数量,定义一个列表
    total_price = [goods[1] * goods[2] for goods in args]
    total_cost = sum(total_price)# 总金额
    # 2,扣减优惠券
    if total_cost >= 5000 and coupon <= total_cost:
        total_cost -= coupon
# 3,扣减积分抵扣
    if total_cost >= 5000 and score //100 <= total_cost:
        total_cost -= score // 100
# 4,添加运费
    total_cost += espress

    return total_cost
shi=jisun(100,1000,10000,("鼠标",188,2),("键盘",128,6),("电脑",1999,10))
print('JIAG',shi)


# ===== 7. 通用包装写法：*args + **kwargs 一起用（写装饰器必备） =====

def wrapper_demo(func, *args, **kwargs):
    print("调用前")
    result = func(*args, **kwargs)
    print("调用后")
    return result


print(wrapper_demo(pow, 2, 10))  # 1024


# ===== 8. 仅位置参数 / 与 仅关键字参数 * =====

def standard(a):  # 位置或关键字都行
    return a


def pos_only(a, /):  # / 左边：只能按位置传
    return a


def kwd_only(*, a):  # * 右边：只能按关键字传
    return a


def combined(pos_only_arg, /, standard_arg, *, kwd_only_arg):
    return pos_only_arg, standard_arg, kwd_only_arg


print(standard(1), standard(a=1))
print(pos_only(1))
# print(pos_only(a=1))        # 报错：仅位置参数
# print(kwd_only(1))          # 报错：仅关键字参数
print(kwd_only(a=1))
print(combined(1, 2, kwd_only_arg=3))
print(combined(1, standard_arg=2, kwd_only_arg=3))


# 参数名和 **kwargs 撞车时，用 / 把参数变成仅位置
def foo(name, /, **kwds):
    return 'name' in kwds


print(foo(1, **{'name': 2}))  # True


# ===== 9. 参数解包 =====

def add_three(a, b, c):
    return a + b + c


args_list = [1, 2, 3]
print(add_three(*args_list))  # * 解列表/元组

kwargs_dict = {'a': 1, 'b': 2, 'c': 3}
print(add_three(**kwargs_dict))  # ** 解字典

print(list(range(*[3, 6])))  # [3, 4, 5]

# 混合解包
print(add_three(*[1, 2], **{'c': 3}))


# ===== 10. 参数顺序速记 =====
# 位置参数 -> 默认参数 -> *args -> 仅关键字参数 -> **kwargs
def full(a, b=2, *args, c, d=4, **kwargs):
    print(a, b, args, c, d, kwargs)


full(1, 2, 3, 4, c=5, e=6)


# ===== 练习（取消注释运行）=====
# 1. 写一个函数，接收任意个数字，返回最大值与最小值的元组
# def min_max(*nums):
#     return max(nums), min(nums)
# print(min_max(3, 1, 7, 2))
#
# 2. 写一个函数 build_url(host, *, path='/', scheme='http')，只能用关键字传 path 和 scheme
# def build_url(host, *, path='/', scheme='http'):
#     return f"{scheme}://{host}{path}"
# print(build_url('example.com', path='/api', scheme='https'))
#
# 3. 用参数解包调用 print：print(*[1, 2, 3], sep='-')
# print(*[1, 2, 3], sep='-')
