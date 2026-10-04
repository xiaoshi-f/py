# 05. if条件判断
# 知识点：if / else、elif 多条件分支、条件嵌套、账号登录与三角形判断案例

# 流程控制语句：条件判断，if 满足指定条件才执行
# 语法：
# if 判断条件:          # 布尔值
#     条件成立，执行操作

# if 判断
a = 300
if a > 200:
    print('nihao')
else:
    print('buhao')

# 练习：
# 2. 定义 1 个变量 d 值为 40
c = 20
d = 40
# 3. 判断 c 是否大于 d，如果 c 大于 d 则打印输出
# 4. 如果 c 小于 d 则打印输出
if c > d:
    print('nihao')
else:
    print('buhao')

# 5. 在控制台输入一串数字，判断这串输入的数字是否大于 100
# un = int(input('输入一串数字:'))
# 6. 如果大于 100 则打印
# 7. 如果小于 100 则打印
# if un > 100:
#     print('nihao')
# else:
#     print('buhao')

# 在此基础上再加一个校验规则：如果输入的内容是整数以外的，提示（您输入的不是数字噢）并且结束判断
# au = input('输入数字')
# if au.isdigit():
#     au = int(au)
#     if int(au) > 100:
#         print('大于100')
#     else:
#         print('不到100')
# else:
#     print('不是数字')

# ==================== 多个条件判断 ====================
a = 23
b = 29
c = 33
if a >= b and a >= c:          # 条件1满足就打印条件1的内容，不满足继续判断条件2
    print('a是最大的')
elif b >= a and b >= c:        # 条件2满足就打印条件2的内容，不满足继续判断条件3
    print('b是最大的')
else:                          # 以上条件都不满足时执行 else
    print('c是最大的')

# ==================== 案例：账号密码登录 ====================
# p = 188
# q = 6888
# a = int(input("请输入账号"))
# b = int(input("输入密码"))
# if a == p and b == q:
#     print("登入成功")
# else:
#     print("登入失败,账号密码错误")

# ==================== 案例：三角形判断 ====================
# a = int(input())
# b = int(input())
# c = int(input())
# if (a + c) > b and (a + b) > c and (b + c) > a:
#     if a == b and b == c:
#         print('等边三角形')
#     elif a == b or b == c or c == a:
#         print('等腰三角形')
#     else:
#         print('三角形')
# else:
#     print('不是三角形')

# ==================== if 语法示例 ====================
# a = 700
# if a > 680:
#     print("欢迎")
