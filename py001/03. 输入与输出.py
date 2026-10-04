# 03. 输入与输出
# 知识点：input() 接收控制台输入、print() 输出、输入内容长度统计、ATM 取款案例

# input()
# 说明：input 可以接收用户在控制台输入的内容，默认为字符串类型
# 公式：input('提示信息')
# i = input("请输入")
# print(f"{i}")

# name = input("姓名")
# address = input("住址")
# print(len(name), len(address))
# print(name, type(name))
# print(address, type(address))
# print(f"{name},{address}")

# ==================== 案例：模拟 ATM 取款 ====================
# atm = 10000
# a01 = int(input('插入卡输入密码'))
# if a01 == 1234:
#     print("输入正确,输入取款金额")
#     a02 = int(input())
#     atm = atm - a02
#     if atm >= 0:
#         print('取款成功，剩余金额', atm)
#     else:
#         print('错误')
# else:
#     print('密码错误')
