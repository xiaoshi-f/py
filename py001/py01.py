from dataclasses import replace

print(7)

print(10 / 5)

# 变量
a=1
b=2
print(a+b)

# 重新赋值 先运算在赋值
a =a + b
print(a)
a =a - b
print(a)

# 交换两个变量的值
a, b = b ,a
print(a)
print(b)

# 字符串格式化
# 说明: 在字符串中引用变量.
# 方式1: "xxxx{}xxxxxxxxxx{}xxxxxxxx{}xxxx".format(变量1,变量2,变量3)
# 方式2: f"xxxxx{变量1}xxxxxxxxxx{变量2}xxxxxxxxxxxx{变量3}xxxxxxxxxxxx"
name='小石'
sex = '男'
print(
    '你的名字'+name + '你的性别'+ sex +
     f'\n你的名字{name}你的性别{sex}'+
    '\n你的名字{}你的性别{}'.format(name,sex)
)


#        "q  w  e  q  r   q"
# 正下标:   0  1  2  3  4   5
# 负下标:  -6 -5 -4 -3 -2  -1
a = "明天中午12点放假,1.5天"
print(a[0])                         #打印第1个字符
print(a[-1])                        #打印倒数第1个字符
print(a[6])                         #打印第7个字符

# 1.定义一个学校的名字，老师的名字，学生的名字，用字符串拼接方法打印出来。
school = "灵兔学院"
teatcher = "阿萨姆老师"
student = "大兵"
print(school+teatcher+student)

# 2.定义一个姓名，爱好，喜欢的食物，爱看的电影，用f字符串格式化方法打印出来。
# 3.定义一个姓名，爱好，喜欢的食物，爱看的电影，用.format字符串格式化方法打印出来。
name = "大兵"
like = "上课看小说"
food = "版面"
movie = "赛尔号"
print(f"{name}同学喜欢{like},今天中午吃的{food},最喜欢看的电影是{movie}")
print("{}同学喜欢{},今天中午吃的{},最喜欢看的电影是{}".format(name,like,food,movie))

# 4.定义一个字符串“我想要出去玩，想去打麻将”，把‘打’这个字取出来
# 5.定义一个字符串“我想要出去玩，想去打麻将”，把‘玩’这个字取出来
play = "我想要出去玩，想去打麻将"
print(play[-3])
print(play[5])

# 6.定义一个字符串“今天是疯狂星期六”，把‘六’这个字取出来
# 7.定义一个字符串“今天是疯狂星期六”，把‘疯’这个字取出来
week = "今天是疯狂星期六"
print(week[-1])
print(week[3])

#整数是指不含小数点的数字，都是整数
a=1
print(a,type(a))

# 浮点型是指包含小数点的数字，都是浮点型
b=1.314
print(b,type(b))

# 说明：bool值只有两个，
# 一个是True代表真，数字 1
# 一个是False代表假，数字 0
c =True
print(c,type(c))
D=False
print(D,type(D))

# 说明：None指为空，空值
# 注意：None首字母大写
e=None
print(e,type(e))

# len()
# 说明：获取值的长度，对象不可以是数字和布尔值，然后字符串里的数字和字母和汉字和标点符号都算是1个长
f="你好我是小石，我加入了商丘学院"
print(len(f
))
#
# # input()
# # 说明：input可以接受用户在控制台输入的内容,默认为字符串类型.
# # 公式：input('提示信息')
# i = input("")
# print(f"{i}")
#
# name = input("姓名")
# address = input("住址")
# print(len(name),len(address))
# print(name,type(name))
# print(address,type(address))
# print(f"{name},{address}")

# count()
# 说明：统计某个元素出现的次数.
# 可以用于：字符串、元组、列表等
# 公式: 变量名.count("元素")
g ='123456789009876543210000012345678'
co = g.count('0')
print(co)

# h =input()
# co = h.count('0')
# print(co)

# index()
# 说明：统计某一个元素出现的下标位置，下标是从0开始数的。
# 公式: 变量名.index(元素)
i ='36482971462081512420109'
co = i.index('0')
print(co)




# 1.list列表[]
# 说明：.list列表是一个有序的数据集，可以存放任意的数据，可以对列表进行修改。
# 有序的数据类型，可以通过下标查找。
# 可以存放任意的数据，整数、浮点型、字符串、布尔, 空, 列表, 集合,元组,字典.
# 列表可以增删改查.
# 公式: 变量名 = [ 数据1,  数据2,  数据3........  ]
a = [1,23,4,5,6,True,False,None,3.14159265357,"hello"]              #定义a变量,存储一个列表​
print(a,type(a))                                                    #打印a变量和数据类型​
print(len(a))

# 查询数据
# 查询单个数据
# 说明：list因为是有序的，所有可以通过下标去查询信息，索引从0开始计数。
# 公式：
# 查询单个数据:  列表名[下标]
# 查询多个数据:  列表名[ 起始下标 : 结束位置 ]
# 查询多个数据:  列表名[ 起始下标 : 结束位置 : 步长]
# #下标是从0开始数的，每一个逗号相当于间隔，逗号是不参与计数的。找不到也会报错。

a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]                  #定义a变量,存储一个列表
print(a[0])                               #第一个数据
print(a[-1])                              #最后一个数据
print(a[0:8])                               #查询第1-8个数据
print(a[20:36])                             #查询第21-36个数据
print(a[15:46])                             #查询第16-46个数据
print(a[::3])                                 #打印a列表中的数据,跨度为3
print(a[::-1])                                #逆序打印a列表的内容,从最后一个开始打印到第一个

# 添加数据
# #列表里面可以在指定的位置添加数据内容
# 变量名.append( 数据1 )                                   #在末尾添加单个数据
# 变量名.extend([数据1, 数据2, 数据3])                       #在末尾添加多个数据
# 变量名.insert( 下标, 值 )                                 #在指定位置添加数据
a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#在列表的末尾添加一个数据内容
a.append(True)
a.append(False)
a.append(None)
a.append("12312")
print(a)
#在列表的末尾添加多个数据内容
a.extend(["唱","跳", "rap", "篮球","末尾"])
print(a)
#在列表的指定位置添加数据
a.insert(0,"嫂子开门,我是我哥")
print(a)
a.insert(-1,"我叫大兵")
print(a)
a.insert(len(a),"我叫小兵")                         #插入到哪个位置
print(a)
# 修改数据
# 说明: 对列表里面的某一个位置的数据进行重新赋值.
# 公式: 列表名[ 下标 ]  = 新值
a[0]='小石'
print(a)
# 删除数据
# 说明: 列表中的数据可以进行删除.
# 公式:
# 列表名.remove( 值 )                                           #根据值删除
# del  列表名[ 下标 ]                                             #根据位置删除
a = [1,12,12,12,12,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,5,5,5,5,9,"气温"]
#根据值删除
a.remove(1)                                  #删除值1
print(a)
a.remove("气温")
print(a)
#根据下标删除
del a[0]                                #删除第一个数据
del a[-1]                               #删除最后一个数据
print(a)
# 2.tuple 元组()                         #他pou
# 说明：元组是一个有序的集合，可以通过下标访问数据，元组里面可以存放任意的数据类型。
# 特点：
# 1.有序的数据类型，可以通过下标查找。
# 2.可以存放任意的数据，整数、浮点型、字符串、布尔等。
# 3.不可以修改、删除、新增、只能查询。
# 公式：变量名 = （数据1，数据2，数据3...）
# 公式：变量名 = 数据1，数据2，数据3...
E=(1,'电脑','屏幕','石',True,)
print(E,type(E))
# 查询数据
# 说明：tuple因为是有序的，所以可以通过下标去查询信息，索引从0开始计数。
# 公式：
# 查询单个数据:  元组名[下标]
# 查询多个数据:  元组名[ 起始下标 : 结束位置 ]
# 查询多个数据:  元组名[ 起始下标 : 结束位置 : 步长]
# #下标是从0开始数的，每一个逗号相当于间隔，逗号是不参与计数的。找不到也会报错。
a = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50)                  #定义a变量,存储一个列表
print(a[0])                               #第一个数据
print(a[-1])                              #最后一个数据
print(a[0:8])                               #查询第1-8个数据
print(a[20:36])                             #查询第21-36个数据
print(a[15:46])                             #查询第16-46个数据
print(a[::3])                                 #打印a列表中的数据,跨度为3
print(a[::-1])                                #逆序打印a列表的内容,从最后一个开始打印到第一个
# 3.set 集合{}
# 说明：set集合是一个无序的且不重复的数据集合。可以修改数据，数据会自动去重，会去掉重复数据。
# 特点：
# 1.无序的数据类型，不可以通过下标查找。
# 2.可以存放任意的数据，整数、浮点型、字符串、布尔等。
# 3.可以增、删、查询。但是不能修改单个元素。
# 4.元素唯一可以自动去重。f
# 公式：变量名={数据1，数据2，数据3....}
Q={1,'石','石',True,2,'你好'}
print(Q,type(Q))
# 添加数据
# .add 添加单个数据
# 公式：变量名.add（值）
# 说明：因为是无序的关系，所有添加后的数据，打印时会随机排序。
Q.add('小石')
print(Q)
# .update 添加多个数据
# 公式：变量名.update([数据1，数据2，数据3....])
Q.update('你','老弟','哈哈哈')
print(Q)
# 删除数据
# .remove 删除指定数据
# 公式：变量名.remove（值）
# 说明：根据值来删除，如果删除不存在的值，会导致报错。
Q.remove(2)
print(Q)
# .clear 删除所有数据
# 公式：变量名.clear()
Q.clear()
print(Q)
# pop()删除指定位置值，默认最后一个
# sort()排列
# reverse 反转


# 4,dict 字典
# 说明：字典是以键值对的方式进行储存的，相当于json字符串。
# 特点：
# 1.可以存放任意的数据，整数、浮点型、字符串、布尔等。
# 2.字典中key（键）不可以重复，value（值）可以重复。
# 3.可以通过key找到value
name = {
    'A':'小石小菜鸡',
    'B':'你好吗？'
}
print(name,type(name))

dict_name = {
    'name': '小明',
    'sex': '男',
    'hobby': 'ps5',
    'dizhi': '港区',
    'movie': '机器人总动员',
    'food': '麦当劳',
    'city': '郑州'
}
print(dict_name, type(dict_name))
# 查询数据
# 公式：变量名[key]
# 说明：通过key来找数据
print(dict_name['hobby'])
# 层级关系：不管有多少层级，必须要按照层级关系一层一层进行查找，每一层都要写。
dict_name = {
    'name': '小明',
    'sex': '男',
    'hobby': 'ps5',
    'dizhi': '港区',
    'movie': '机器人总动员',
    'food': '麦当劳',
    'city' :'郑州',
    'student':{
        'id':12,
        'maneid': 'xiaoshuai012',
        'class':{
            'classname':'2207',
            'classid':'2026'
        }
    }
}
print(dict_name['student']['class']['classid'])# 层级关系：不管有多少层级，必须要按照层级关系一层一层进行查找，每一层都要写。
# 添加数据
# 公式：变量名['新的key']=值
# 说明：添加数据必须是新的key，如果是已经存在的key会被认为是修改。
dict_name['a'] = 1
print(dict_name)
dict_name['b'] = 2
print(dict_name)

# 删除数据
# .pop(key)
# 公式：变量名.pop(key)
# 说明：通过key来进行删除
# del 变量名[key]
# 公式：del 变量名[key]
# 说明：通过key来进行删除。
dict_name.pop('a')
print(dict_name)
del dict_name['food']
print(dict_name)
# 遍历字典
# 公式：变量名.keys()
# 说明：只获取字典中所有的key
# 公式：变量名.values()
# 说明：只获取字典中所有的value
# 公式：变量名.items()
# 说明：只获取字典中所有的key和value
print(dict_name.keys())
print(dict_name.values())
print(dict_name.items())



# 5对象函数
# .count函数
# 公式：变量名.count('关键字')
# 说明：统计这个关键字出现的次数
# .index函数
# 公式：变量名.index('关键字')
# 说明：查找字符串、元组、列表在数据中的下标位置。
# .replace函数
# 公式：变量名.replace('替换之前的内容','新内容')
# 说明：将字符串内容进行替换，用于字符串str类型。
# 注意：当replace替换内容之后的结果，如果直接打印的话是不会有变化的，需要重新赋值给一个新的变量名，打印新的变量名才是最后修改之后的内容。
shi='今天是星期六'
y=shi.replace('今天是','星期五')
print(y)
# .isdigit函数
# 说明：isdigit函数判断字符串是不是纯数字，如果是纯数字返回True，如果不是纯数字返回False。
# 注意：判断对象内容必须是字符串。
# 字符串是纯数字，所以结果是True
str = '123'
print(str.isdigit())
# 不是纯数字，有中文，所以结果是False
str2 = '123你好'
print(str2.isdigit())
# 不是纯数字，有小数点，所以结果是False
str3 = '123.00'
print(str3.isdigit())
# .join函数
# 说明：join是用来做字符串拼接的，中间可以加符号拼接出结果。
# 公式：'输入你想要拼接的符号'.join(变量名)
a=('1234567','23456','5676','3456')
print(a)
print('-'.join(a))
# .split函数
# 说明：用来做字符串分割，使用某一个关键字作为分割符号。
# 公式：变量名.split('需要用来分割的内容')
a=('12345678765432167895043267843212')
print(a)
print(a.split('6'))


# 运算符 + —  *  /  %取余数  //取商   and和   or或者  not取反
# 说明：判断是不是在xx之内的。比如：a in b 判断a的值是不是在b中存在，如果存在则是True，不存在则是False

# 一、类型转换
# 说明：不同的数据类型之间是可以进行转换的。
# 1.基本数据类型转换
# 字符串str<------>整数int<------>浮点型float之间可以相互转换。
# 格式：转换后的变量名=转换后的类型（当前要转换的变量名）
# 注意：
# 1.字符串转换成int类型，要求字符串中本身就是整数才可以转换。
# 2.字符串转换成float类型，要求字符串中本身就是小数点类型才可以转换，如果是整数，转换完成之后，会补充小数点后1位。
name=('123')
print(name,type(name))
name01=int(name)
print(name01,type(name01))

# 复杂数据类型转换
# 列表list<------>元组tuple<------>集合set 之间也可以互相转换。
# 格式：转换后的变量名=转换后的类型（当前要转换的变量名）
# 当前列表list类型
list_name = [1, 2, 3]
print(list_name, type(list_name))
# 从列表list转换成元组tuple
tuple_name = tuple(list_name)
print(tuple_name, type(tuple_name))
# 从列表list转换成集合set
set_name = set(list_name)
print(set_name, type(set_name))
# 从元组tuple转换成集合set
set_name2 = set(tuple_name)
print(set_name2, type(set_name2))

# 二、内置函数
# input函数
# 说明：input函数在控制台提示输出内容，不管输入的是什么内容，最终数据类型都是字符串str类型。
# 公式：input('展示的内容')
# name = input('输入姓名')
# print(name, type(name))



# if判断
a=300
if a > 200:
    print('nihao')
else :
    print('buhao')

c = 20
# 2、定义1个变量b值为40
d = 40
# 3、判断下a是不是大于b，如果a大于b 则打印输出
# 4、如果a是小于b的则打印输出
if c > d:
    print('nihao')
else:
    print('buhao')
# 5、在控制台输入一串数字，判断这串输入的数字是不是大于100
# un = int(input('输入一串数字:'))
# # 6、如果大于100则打印
# # 7、如果小于100则打印
# if un > 100:
#     print('nihao')
# else:
#         print('buhao')
# 在此基础上再加一个校验规则，如果输入的内容是整数以外的，提示（您输入的不是数字噢）并且结束判断
# au=input('输入数字')
# if au.isdigit():
#     au=int(au)
#     if int(au)>100:
#         print('大于100')
#     else:
#         print('不到100')
# else:
#         print('不是数字')
# 多个条件判断
a = 23
b = 29
c = 33

if a >= b and a >= c:  # 如果条件1满足,打印条件1的内容,如果条件1不满足继续判断条件2
    print('a是最大的')
elif b >= a and b >= c:  # 如果条件2满足,打印条件2的内容,如果条件2不满足继续判断条件3
    print('b是最大的')
else:  # 以上条件都不满足的时候,就会执行else
    print('c是最大的')

# while 循环
a=0
while a<10:
    a=a+1
    print(a)
# b = int(input('输入钱包'))
# while b<100:
#     b=b+5
#     print('目前收款金额'+b)
# print('装不下了')
# break终止当前所在的循环
# 说明：break 是一个控制流语句，用于（立即终止当前所在的循环）比如（for循环或者while循环），跳出循环体，继续执行循环之后的代码。
# 关键点：
# 1.作用范围：break只能在循环内部（for/while），如果在循环外使用会报错。
# 2.立刻退出：一旦执行break，循环就会立刻结束，无论循环条件是否仍然满足。
# 3.只影响当前循环：如果存在嵌套循环，break只会退出最近的一层循环
a = 0
while a < 5:
    if a == 3:
        break
    a = a + 1
    print(f'a的值是{a}')
print('循环结束')

# 五、for 循环
# 格式：for 变量 in 可迭代对象
# range函数
# range函数生成一个列表
# range后面加的（）（）里面放的是数字几，代表生成的就是几个数字的列表
# range（n）
# 说明：从0开始计数，最后一个不要，然后总共计数6个数。
for i in range(1,9):
    print(i)
for i in range(1,9,2):
    print(i)

# 遍历集合
a = {'开开','心心',12,'你好',5,6,'下班'}
for i in a:
    print(i)

# 遍历元组
b = '西瓜', '香蕉', '苹果'
for i in b:
    print(i)

# 遍历列表
c = ['西瓜', '香蕉', '苹果']
for i in c:
    print(i)

# 遍历集合
a = {'开开', '心心', 12, '你好', 5, 6, '下班'}
for i in a:
    if i == '上班':
     print('这个列表中有上班')
else:
    print('没有上班')












