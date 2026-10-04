# -*- coding: utf-8 -*-
# 15. 数据容器-dict
# 知识点：字典键值对、key/value 特点、按 key 查询与层级查询、增删、keys/values/items 遍历

# ==================== dict 字典 ====================
# 说明：字典是以键值对的方式进行储存的，相当于 json 字符串
# 特点：
#   1. 可以存放任意的数据：整数、浮点型、字符串、布尔等
#   2. 字典中 key（键）不可以重复，value（值）可以重复
#   3. 可以通过 key 找到 value
name = {
    'A': '小石小菜鸡',
    'B': '你好吗？'
}
print(name, type(name))

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

# ==================== 查询数据 ====================
# 公式：变量名[key]
# 说明：通过 key 来找数据
print(dict_name['hobby'])
# 层级关系：不管有多少层级，必须要按照层级关系一层一层进行查找，每一层都要写
dict_name = {
    'name': '小明',
    'sex': '男',
    'hobby': 'ps5',
    'dizhi': '港区',
    'movie': '机器人总动员',
    'food': '麦当劳',
    'city': '郑州',
    'student': {
        'id': 12,
        'maneid': 'xiaoshuai012',
        'class': {
            'classname': '2207',
            'classid': '2026'
        }
    }
}
print(dict_name['student']['class']['classid'])

# ==================== 添加数据 ====================
# 公式：变量名['新的key'] = 值
# 说明：添加数据必须是新的 key，如果是已经存在的 key 会被认为是修改
dict_name['a'] = 1
print(dict_name)
dict_name['b'] = 2
print(dict_name)

# ==================== 删除数据 ====================
# .pop(key)
# 公式：变量名.pop(key)
# 说明：通过 key 来进行删除
# del 变量名[key]
# 公式：del 变量名[key]
# 说明：通过 key 来进行删除
dict_name.pop('a')
print(dict_name)
del dict_name['food']
print(dict_name)

# ==================== 遍历字典 ====================
# 公式：变量名.keys()     只获取字典中所有的 key
# 公式：变量名.values()   只获取字典中所有的 value
# 公式：变量名.items()    只获取字典中所有的 key 和 value
print(dict_name.keys())
print(dict_name.values())
print(dict_name.items())
