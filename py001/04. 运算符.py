# 04. 运算符
# 知识点：算术运算符、赋值运算符、比较运算符、逻辑运算符、in、基本/复杂类型转换

# 运算符：+ - * /  %取余数  //取商  and和  or或者  not取反
# 赋值运算符 =
#   +=  a += 2 等价于 a = a + 2
# 比较运算符 ==  !=  >=  <=
# 逻辑运算符 and和  or或者  not取反
# in：判断是否在 xx 之内。a in b 判断 a 的值是否在 b 中存在，存在为 True，不存在为 False

# ==================== 一、类型转换 ====================
# 说明：不同的数据类型之间可以进行转换

# 1. 基本数据类型转换
# 字符串 str <------> 整数 int <------> 浮点型 float 之间可以相互转换
# 格式：转换后的变量名 = 转换后的类型（当前要转换的变量名）
# 注意：
#   1. 字符串转换成 int 类型，要求字符串中本身就是整数才可以转换
#   2. 字符串转换成 float 类型，要求字符串中本身就是小数点类型才可以转换；
#      如果是整数，转换完成之后会补充小数点后 1 位
name = ('123')
print(name, type(name))
name01 = int(name)
print(name01, type(name01))

# 2. 复杂数据类型转换
# 列表 list <------> 元组 tuple <------> 集合 set 之间也可以互相转换
# 格式：转换后的变量名 = 转换后的类型（当前要转换的变量名）
list_name = [1, 2, 3]
print(list_name, type(list_name))
tuple_name = tuple(list_name)       # 列表 -> 元组
print(tuple_name, type(tuple_name))
set_name = set(list_name)           # 列表 -> 集合
print(set_name, type(set_name))
set_name2 = set(tuple_name)         # 元组 -> 集合
print(set_name2, type(set_name2))

# ==================== 二、内置函数 ====================
# input 函数
# 说明：input 函数在控制台提示输出内容，不管输入的是什么内容，最终数据类型都是字符串 str 类型
# 公式：input('展示的内容')
# name = input('输入姓名')
# print(name, type(name))

# ==================== 三、运算符实操 ====================
# num = int(input('输入一个整数'))
# print(f"{num}在10到20之间", num >= 10 and num <= 20)
# print(f"{num}在10到20之间", 10 <= num <= 20)
# print(f"{num}不在10到20之间", num < 10 or num > 20)
