"""模块
from my_module.circle import circle_area  链接其他包
使用模块需导入   模块名.功能名
模块名as模块别名
"""

# import random as rd  #  导入模块
# for i in range(100):
#     print(rd.randint(1,100))

# 导入模块中功能  from...import....
from random import randint
from random import randint as rnd  # 模块名.功能名as功能别名
from random import * # 整个模块
for i in range(100):
    print(randint(0,100))

# 自定义莫模块

# 自定义模块
# import module
#
#
# s_radius =10
# m_radius =15
# l_radius =20
#
# small_area=module.circle_area(s_radius)
# print(small_area)
# module.lod_separator1()
# print(module.PI)
# module.lod_separator2()
# print(module.NAME)
# module.lod_separator3()
#
# module.lod_separator3()

# 导入模块中功能
# from module import lod_separator1,lod_separator2,PI,NAME,lod_separator3
# print(PI)
# lod_separator2()
# print(NAME)
# lod_separator3()
# lod_separator3()

# 导入全部功能
# from module import *
# print(PI)
# lod_separator2()
# print(NAME)
# lod_separator3()
# lod_separator3()
# __all__模块的特使变量 模块统配的功能
