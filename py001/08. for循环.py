# 08. for循环
# 知识点：for 遍历、range 三种用法、for ... else、遍历字符串/列表/元组/集合、奇数和与倍数和

# for 循环：本质是轮询遍历机制，对内容逐个处理
# 格式：
# for 元素 in 待处理元素集:
#     循环体代码
# else:                  # 循环结束
#
# for 与 while 的使用场景：
#   while 通过条件控制开始和结束
#   for 对已知数据集进行遍历，已知循环次数

# ==================== range 函数 ====================
# range 根据指定规则生成数字序列
#   range(end)               从 0 开始到 end 结束，不包含 end 本身
#   range(start, end)        从哪开始到哪里结束，不含本身
#   range(start, end, step)  step 步长
for i in range(1, 9):
    print(i)
for i in range(1, 9, 2):
    print(i)

# 遍历集合
a = {'开开', '心心', 12, '你好', 5, 6, '下班'}
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

# for ... else
a = {'开开', '心心', 12, '你好', 5, 6, '下班'}
for i in a:
    if i == '上班':
        print('这个列表中有上班')
else:
    print('没有上班')

# 遍历字符串
# mag = "hello-world"
# for i in mag:
#     print(i)
# else:
#     print("else")

# a = input("输入遍历的字符串")
# for s in a:                # 遍历出来的元素；a 是需要遍历的数据
#     print(f"元素：{s}")
# else:
#     print('jieshu')

# ==================== 案例：计算 1-100 奇数累加之和 ====================
# a = 0
# for i in range(1, 101):
#     if i % 2 != 0:         # 奇数
#         a += i
# # 简化写法：for i in range(1, 101, 2):
# print(a)

# ==================== 案例：计算 100 到 500 所有 3 的倍数之和 ====================
# b = 0
# for c in range(100, 501):
#     if c % 3 == 0:
#         b += c
# print(b)
