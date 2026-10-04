def circle_area(r):
    pi = 3.14159
    return round(pi * r * r, 1)
def circle_len(r):
    pi = 3.14159
    return round(pi * r * 2, 1)

PI = 3.14159  # 定义常量 不会变化的数据  常量名称全大写
NAME = "小石小石"
def lod_separator1():
    print("- " * 30)
def lod_separator2():
    print("+ " * 30)
def lod_separator3():
    print("# " * 30)
def lod_separator4():
    print("* " * 30)


# 调用函数
# lod_separator1()  测试代码
# __name__内置变量运行值为__main__
# print(__name__) 测试代码写在if判断语句中
# 执行当前文件则执行下方代码,作为模块导入则不执行
if __name__ == '__main__':
    lod_separator1()