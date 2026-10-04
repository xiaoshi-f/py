# 动态存储语言 一个变量可以存储不同类型的数据（开发中只存储一种数据）
# num = 114.1
# print(num)
# num = num + 1
# print(num)
from ast import increment_lineno
from contextlib import nullcontext
from unittest import case

# base = 20.7 # 基础播放量
# incr = 50 #新增播放量
# print("未来一个月播放",base+incr)
# print("未来二个月播放",base+incr+incr)
#
# # 一次性定义多个变量
# a,b,c =1,2,3
# print(a,b,c)
#
# # 相互赋值 a赋值b b赋值a
# a = 10
# b = 20
# c = a
# a=b
# b =c
# print(a,b)

# 常见数据类型 int  float(浮点)  str（字符串）  bool  NoneType（空值）

# 查看数据类型
# a=1
# print(a,type(a))

# 字符串  单引号  双引号  多引号  转义字符

# 字符串拼接
# 1.定义一个学校的名字，老师的名字，学生的名字，用字符串拼接方法打印出来。
# school = "灵兔学院"
# teatcher = "阿萨姆老师"
# student = "大兵"
# print(school+teatcher+student)

# 2.定义一个姓名，爱好，喜欢的食物，爱看的电影，用f字符串格式化方法打印出来。
# 3.定义一个姓名，爱好，喜欢的食物，爱看的电影，用.format字符串格式化方法打印出来。
# name = "大兵"
# like = "上课看小说"
# food = "版面"
# movie = "赛尔号"
# print(f"{name}同学喜欢{like},今天中午吃的{food},最喜欢看的电影是{movie}")
# print("{}同学喜欢{},今天中午吃的{},最喜欢看的电影是{}".format(name,like,food,movie))



 # 说明：input可以接受用户在控制台输入的内容,默认为字符串类型.
 # 公式：input('提示信息')
# i = input("请输入")
# print(f"{i}")
# name = input("姓名")
# address = input("住址")
# print(len(name),len(address))
# print(name,type(name))
# print(address,type(address))
# print(f"{name},{address}")
# atm = 10000
# a01 =int(input('插入卡输入密码'))
# if a01 == 1234:
#     print("输入正确,输入取款金额")
#     a02 = int(input())
#     atm =atm-a02
#     if atm >= 0:
#         print('取款成功，剩余金额',atm)
#     else:
#         print('错误')
# else:
#     print('密码错误')


# # 运算符 + —  *  /  %取余数  //取商   and和   or或者  not取反
# 赋值运算符 =
# +=  a += 2 : a += 2
# 比较运算符  ==   ！=   >=    <   <=
# 逻辑运算符  and和    or或者    not取反
# num = int(input('输入一个整数'))

# print(f"{num}在10到20之间",num >= 10 and num <= 20)
# print(f"{num}在10到20之间",10 <= num <= 20)
# print(f"{num}不在10到20之间",num<10 or num>20)

# 逻辑处理  循环
# 流程控制语句  条件判断 if满足指定条件，才执行
# if  判断添加 ：    布尔值
#        条件成立，执行操作
# a= 700
# if a > 680:
#     print("欢迎")
# p =188
# q =6888
#
# a = int(input("请输入账号"))
# b =int(input("输入密码"))
# if a == p and b == q:
#     print("登入成功")
# else:print(
#     "登入失败,账号密码错误"
# )
# 三条边
# a = int(input())
# b = int(input())
# c = int(input())
# if (a+c)> b and (a+b)>c and (b+c)>a:
#     if a==b and b==c:
#         print('等边三角形')
#     elif a == b or b == c or c == a:
#         print('等腰三角形')
#     else:print('三角形')
# else:
#     print('不是三角形')

# 结构模式match   case 用一个清晰的模板去精准匹配数据结构和内容，匹配成功执行响应操作
# day = int(input('周几'))
# match day:
#     case 1:
#         print('上班')
#     case 2:
#         print('上班')
#     case 3:
#         print('上班')
#     case 4:
#         print()
#     case 5:
#         print()
#     case 6:
#         print()
#     case 7:
#         print()

# a= float(input('第一个数'))
# b= float(input('第二个数'))
# d=input('请输入+-*/')
# match d :
#     case "+":
#         print(a+b)
#     case "-":
#             print(a-b)
#     case "*":
#             print(a*b)
#     case "/" if b !=0:
#             print(a/b)
#     case "_":
#             print('不支持 ')

# while 条件标答：  条件表达式来控制是否进行下一次循环  布尔值
#        循环体语句1
#        循环体语句2
#  eles  循环结束
# a= 0
# while a<10:
#     print('人生苦短')
#     a+=1
#
# else:
#     print('结束')
# 1到100 偶数累加之和  数 % 2 ==0
# a =0
# # 循环开始
# i =1
# while i <=100:
#     if i %2==0:
#         a +=i
#     i +=1
# print(a)

# for 循环  本质是轮询遍历机制，对内容逐个处理
# for 元素 in 待处理元素集
#     循环体代码
# eles 循环结束
# mag = "hello-world"
# for i in mag:
#     print(i)
# else:
#     print("else")

# a = input("输入遍历的字符串")
# for s in a :#遍历出来的元素  a 需要遍历的数据
#     print(f"元素：{s}")
# else:
#     print('jieshu')
# for 与 while 循环场景
# while通过条件  开始和结束
# for已知数据集进行遍历，已知循环次数

# for  计算1到100奇数之和
# 计算100到500 所有3倍数字之和
# range根据指定规则生成数字序列
# range(end)获得一个从0开始到end 结束数字序列不包含本身
#  range(strat，end) 从哪开始到哪里结束 不含本身
# range(strat，end，step) step步长
# 计算1-100奇数累加之和
# a = 0
# for i in range(1,101):
#     if i % 2 == 0:# 奇数
#         a +=i
# # 简化for i in range(1,101,2):
# print(a)
# b =0
# for c in range(100,501):
#     if c % 3 == 0:
#         b +=c
# print(b)

# 嵌套循环
# for 元素 in 待处理数据集：
#      循环体
#      for 元素 in 待处理数据集
#       循环体
# 接受键盘录入
# m = int(input('输入长度'))
# n = int(input('输入宽度'))
#
# for j in range(n):
#     for i in range(m):
#     # print("*") 默认换行
#        print("*",end="  ")
#     print()

# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f"{j}x{i}={j*i}",end="\t")
#     print()
# 循环关键字break 循环中  结束跳出循环

# 循环while
# while True:
#     #     1.接受输入的用户名，密码
#     username = input("账号: ")
#     password = input("密码: ")
# #     2.校验账号密码是否为空
#     if username == "" or password == "":
#         print("不能为空")
# #     判断用户名密码是否正确
#     if username == "admin" and password == "666888":
#         print("登入成功")
#         break
#     elif username == "xiaoshi" and password == "123456":
#         print("登入成功")
#         break
#     elif username == "xiaofei" and password == "888666":
#         print("成功")
#         break
#     else:
#         print("错误，请重新输入")

# 随机数 import random
# import random
# a = random.randrange(1, 100)
#
# while True:
#     b =int(input('输入数字'))
#     if a > b:
#         print('小了')
#     elif a < b:
#         print('大了')
#     else:
#         print('对了')
#         break
# print("shuzishi",a)


# # 数据存储容器
# a = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50)                  #定义a变量,存储一个列表
# print(a[0])                               #第一个数据
# print(a[-1])                              #最后一个数据
# print(a[0:8])                               #查询第1-8个数据
# print(a[20:36])                             #查询第21-36个数据
# print(a[15:46])                             #查询第16-46个数据
# print(a[::3])                                 #打印a列表中的数据,跨度为3
# print(a[::-1])                                #逆序打印a列表的内容,从最后一个开始打印到第一个
# # 添加数据
# # #列表里面可以在指定的位置添加数据内容
# # 变量名.append( 数据1 )                                   #在末尾添加单个数据
# # 变量名.extend([数据1, 数据2, 数据3])                       #在末尾添加多个数据
# # 变量名.insert( 下标, 值 )                                 #在指定位置添加数据
# a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# #在列表的末尾添加一个数据内容
# a.append(True)
# a.append(False)
# a.append(None)
# a.append("12312")
# print(a)
# #在列表的末尾添加多个数据内容
# a.extend(["唱","跳", "rap", "篮球","末尾"])
# print(a)
# #在列表的指定位置添加数据
# a.insert(0,"嫂子开门,我是我哥")
# print(a)
# a.insert(-1,"我叫大兵")
# print(a)
# a.insert(len(a),"我叫小兵")                         #插入到哪个位置
# print(a)
# # 修改数据
# # 说明: 对列表里面的某一个位置的数据进行重新赋值.
# # 公式: 列表名[ 下标 ]  = 新值
# a[0]='小石'
# print(a)
# # 删除数据
# # 说明: 列表中的数据可以进行删除.
# # 公式:
# # 列表名.remove( 值 )                                           #根据值删除
# # del  列表名[ 下标 ]                                             #根据位置删除
# a = [1,12,12,12,12,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,5,5,5,5,9,"气温"]
# #根据值删除
# a.remove(1)                                  #删除值1
# print(a)
# a.remove("气温")
# print(a)
# #根据下标删除
# del a[0]                                #删除第一个数据
# del a[-1]                               #删除最后一个数据
# print(a)

# 输入10个数排序
# 定义列表
# 存入列表  排序  最大值  平均值  最小值
# sort()排序   len()获取个数，长度
# a=[]
# for i in range(10):
#     b = int(input('数字'))
#     a.append(b)
# print(a)
# a.sort()
# print(a)
# print('xiao',a[0])
# print('da',a[9])
# print('pingjun',sum(a)/len(a))

#合并去重
# a=[21,32,34,45,5676,7,8,9,12]
# b =[21,213,213,342,3532,7,8,765,9]
# for c in b:
#     a.append(c)
# print(a)  #合并
# s = []#去重后列表
# # 判断s里是否存在c里
# for c in a:
#     if c not in s :
#         s.append(c)
# print("去重",s)
# 解包操作  解开成一个一个独立的元素
# num_list1=[12,32,343,46,76,342,213]
# num_list2=[12,32,12312,34,3,4,46233,76,342,12321,112,213]
# num =[*num_list1,*num_list2]# 组包

 # 1-20平方
# num_list =[]
# for i in range(1,21):
#     num_list.append(i**2)
# print(num_list)
# # 列表推导式  按照规则快速生成列表-->语法格式for i in 序列/列表 条件判断
# num_list2 =[i**2 for i in range(1,21)]
# print(num_list2)


# 字符串 str   不可变 有序性
# a = "明天中午12点放假,1.5天"
# print(a[0])                         #打印第1个字符
# print(a[-1])                        #打印倒数第1个字符
# print(a[6])                         #打印第7个字符

# 元组tuple
