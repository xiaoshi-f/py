# 09. 循环案例1
# 知识点：嵌套循环（打印矩形、99 乘法表）、while True + break 账号密码登录校验

# 嵌套循环
# for 元素 in 待处理数据集:
#     循环体
#     for 元素 in 待处理数据集:
#         循环体

# ==================== 案例一：接受键盘录入，打印矩形 ====================
# m = int(input('输入长度'))
# n = int(input('输入宽度'))
# for j in range(n):
#     for i in range(m):
#         # print("*") 默认换行
#         print("*", end="  ")
#     print()

# ==================== 案例二：打印 99 乘法表 ====================
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print(f"{j}x{i}={j*i}", end="\t")
#     print()

# ==================== 案例三：循环关键字 break + while True 登录 ====================
# while True:
#     # 1. 接受输入的用户名、密码
#     username = input("账号: ")
#     password = input("密码: ")
#     # 2. 校验账号密码是否为空
#     if username == "" or password == "":
#         print("不能为空")
#     # 3. 判断用户名密码是否正确
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
