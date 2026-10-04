# 06. match模式匹配
# 知识点：结构模式 match ... case、字面量匹配、带条件的 case、简易计算器案例

# 结构模式 match ... case
# 用一个清晰的模板去精准匹配数据结构和内容，匹配成功执行相应操作

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

# ==================== 案例：简易计算器 ====================
# a = float(input('第一个数'))
# b = float(input('第二个数'))
# d = input('请输入+-*/')
# match d:
#     case "+":
#         print(a + b)
#     case "-":
#         print(a - b)
#     case "*":
#         print(a * b)
#     case "/" if b != 0:
#         print(a / b)
#     case "_":
#         print('不支持 ')
