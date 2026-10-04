# 01. 字面量与变量
# 知识点：print 输出、变量定义与重新赋值、变量交换、字符串格式化、下标取值

print(7)
print(10 / 5)

# 变量
a = 1
b = 2
print(a + b)

# 重新赋值：先运算再赋值
a = a + b
print(a)
a = a - b
print(a)

# 交换两个变量的值
a, b = b, a
print(a)
print(b)

# Python 是动态存储语言：一个变量可以存储不同类型的数据（开发中一般只存一种数据）
# num = 114.1
# print(num)
# num = num + 1
# print(num)

# 一次性定义多个变量
# a, b, c = 1, 2, 3
# print(a, b, c)

# 相互赋值：a 赋值 b，b 赋值 a（借助中间变量 c）
# a = 10
# b = 20
# c = a
# a = b
# b = c
# print(a, b)

# 播放量案例
# base = 20.7            # 基础播放量
# incr = 50              # 新增播放量
# print("未来一个月播放", base + incr)
# print("未来二个月播放", base + incr + incr)

# 字符串格式化
# 说明：在字符串中引用变量
# 方式1: "xxxx{}xxxxxxxxxx{}xxxxxxxx{}xxxx".format(变量1, 变量2, 变量3)
# 方式2: f"xxxxx{变量1}xxxxxxxxxx{变量2}xxxxxxxxxxxx{变量3}xxxxxxxxxxxx"
name = '小石'
sex = '男'
print(
    '你的名字' + name + '你的性别' + sex +
    f'\n你的名字{name}你的性别{sex}' +
    '\n你的名字{}你的性别{}'.format(name, sex)
)

# 下标（索引）
#        "q  w  e  q  r   q"
# 正下标:   0  1  2  3  4   5
# 负下标:  -6 -5 -4 -3 -2  -1
a = "明天中午12点放假,1.5天"
print(a[0])                         # 打印第1个字符
print(a[-1])                        # 打印倒数第1个字符
print(a[6])                         # 打印第7个字符

# ==================== 练习 ====================
# 1. 定义一个学校的名字、老师的名字、学生的名字，用字符串拼接方法打印出来
school = "灵兔学院"
teatcher = "阿萨姆老师"
student = "大兵"
print(school + teatcher + student)

# 2. 定义一个姓名、爱好、喜欢的食物、爱看的电影，用 f 字符串格式化方法打印出来
# 3. 定义一个姓名、爱好、喜欢的食物、爱看的电影，用 .format 字符串格式化方法打印出来
name = "大兵"
like = "上课看小说"
food = "版面"
movie = "赛尔号"
print(f"{name}同学喜欢{like},今天中午吃的{food},最喜欢看的电影是{movie}")
print("{}同学喜欢{},今天中午吃的{},最喜欢看的电影是{}".format(name, like, food, movie))

# 4. 定义一个字符串"我想要出去玩，想去打麻将"，把'打'这个字取出来
# 5. 定义一个字符串"我想要出去玩，想去打麻将"，把'玩'这个字取出来
play = "我想要出去玩，想去打麻将"
print(play[-3])
print(play[5])

# 6. 定义一个字符串"今天是疯狂星期六"，把'六'这个字取出来
# 7. 定义一个字符串"今天是疯狂星期六"，把'疯'这个字取出来
week = "今天是疯狂星期六"
print(week[-1])
print(week[3])
