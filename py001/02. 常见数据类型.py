# 02. 常见数据类型
# 知识点：int 整数、float 浮点、bool 布尔、NoneType 空值、type() 查看类型、len() 获取长度

# 常见数据类型：int  int  float(浮点)  str(字符串)  bool  NoneType(空值)

# 整数：不含小数点的数字都是整数
a = 1
print(a, type(a))

# 浮点型：包含小数点的数字都是浮点型
b = 1.314
print(b, type(b))

# bool 值只有两个：
#   True  代表真，数字 1
#   False 代表假，数字 0
c = True
print(c, type(c))
D = False
print(D, type(D))

# None 表示为空，空值
# 注意：None 首字母大写
e = None
print(e, type(e))

# len()
# 说明：获取值的长度。对象不可以是数字和布尔值；
#       字符串里的数字、字母、汉字、标点符号都算 1 个长度
f = "你好我是小石，我加入了商丘学院"
print(len(f))
