# -*- coding: utf-8 -*-
# 30. 标准库 - json（配置文件与数据交换）
# 知识点：JSON 是什么、四个核心函数 dumps/loads/dump/load 的区别、
#        Python 类型与 JSON 类型的对应关系、ensure_ascii 中文问题、
#        indent 美化、嵌套结构读写、default 处理不可序列化对象、
#        配置文件读写实战、⚠ JSON 的坑（元组变列表、键变字符串、不能存对象）
#
# 为什么要学：JSON 是数据交换的事实标准。配置文件、接口返回、
#             前后端通信、CAN 报文的测试用例——存成 JSON 最方便。

import json
import tempfile
from pathlib import Path

# ==========================================================
# 1. JSON 是什么
# ==========================================================
# JSON（JavaScript Object Notation）：一种轻量级的数据交换格式
# 长得跟 Python 的字典几乎一样，但它是个「字符串」，不是对象
# 支持的类型只有 6 种：
#   对象 {}      -> Python dict
#   数组 []      -> Python list
#   字符串 "x"   -> Python str
#   数字 123     -> Python int / float
#   布尔 true    -> True / False（JSON 是小写）
#   null         -> None（JSON 是 null）

# ==========================================================
# 2. 四个核心函数（最容易搞混，记住口诀）
# ==========================================================
#   dumps  dump string   Python对象 -> JSON字符串   （s = string）
#   loads  load string   JSON字符串 -> Python对象
#   dump   写文件        Python对象 -> 文件
#   load   读文件        文件       -> Python对象
# 带 s 的跟「字符串」打交道，不带的跟「文件」打交道

print("--- dumps：Python 对象 -> JSON 字符串 ---")
data = {
    "name": "小石",
    "age": 25,
    "scores": [88, 92, 85],
    "vip": True,
    "car": None,
}
json_str = json.dumps(data)
print("  默认（中文被转义）：", json_str)

# ensure_ascii=False：让中文正常显示（写文件/返回给前端时必须加）
json_str_cn = json.dumps(data, ensure_ascii=False)
print("  ensure_ascii=False：", json_str_cn)
print("  类型：", type(json_str_cn).__name__)  # str

# indent：缩进美化，给人看的（配置文件用）
print("\n  indent=4 美化输出：")
print(json.dumps(data, ensure_ascii=False, indent=4))

# ==========================================================
# 3. loads：JSON 字符串 -> Python 对象
# ==========================================================
print("\n--- loads：JSON 字符串 -> Python 对象 ---")
s = '{"name": "老张", "age": 30, "tags": ["Python", "CANoe"]}'
obj = json.loads(s)
print("  解析结果：", obj)
print("  类型：", type(obj).__name__)  # dict
print("  取值：", obj["name"], obj["tags"][0])

# 解析失败 -> json.JSONDecodeError（继承自 ValueError）
try:
    json.loads("{不是合法JSON}")
except json.JSONDecodeError as e:
    print("  解析失败：", str(e)[:50])

# ==========================================================
# 4. 类型对应关系（⚠ 有坑）
# ==========================================================
print("\n--- 类型转换对照 ---")
print("""  Python          ->  JSON          ->  Python（转回来）
  dict               object {}          dict
  list, tuple        array []           list（⚠ 元组变列表！）
  str                string             str
  int, float         number             int / float
  True / False       true / false       True / False
  None               null               None
""")

# 坑1：元组会被转成数组，转回来变成列表
t = (1, 2, 3)
print("  元组进去：", json.dumps(t))
print("  转回来：", json.loads(json.dumps(t)), type(json.loads(json.dumps(t))).__name__)  # list

# 坑2：字典的键必须是字符串，非字符串键会被强转
d = {1: "一", 2: "二"}
print("  数字键：", json.dumps(d))  # {"1": "一", "2": "二"}
print("  转回来键是字符串：", list(json.loads(json.dumps(d)).keys()))

# 坑3：JSON 里不能有 Python 特有对象（set、datetime、自定义对象）
try:
    json.dumps({"s": {1, 2}})  # set 不能序列化
except TypeError as e:
    print("  set 序列化失败：", str(e)[:50])

# 坑4：NaN / Infinity 不是标准 JSON（Python 会输出 NaN，别的语言解析不了）
print("  特殊浮点：", json.dumps({"a": float("nan")}))

# ==========================================================
# 5. dump / load：直接读写文件
# ==========================================================
print("\n--- 文件读写 ---")
tmp = Path(tempfile.gettempdir()) / "config_demo.json"

# 写文件：dump(对象, 文件对象)
with open(tmp, "w", encoding="utf-8") as f:
    # ⚠ 两个参数必加：ensure_ascii=False（中文）、indent=4（好看）
    json.dump(data, f, ensure_ascii=False, indent=4)
print("  写入完成，文件大小：", tmp.stat().st_size, "字节")

# 读文件：load(文件对象)
with open(tmp, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("  读回：", loaded)
print("  和原数据相等：", loaded == data)

print("\n  文件内容：")
print(tmp.read_text(encoding="utf-8"))

# ==========================================================
# 6. 处理不可序列化的对象：default 参数
# ==========================================================
print("\n--- default：自定义序列化 ---")
import datetime


class User:
    def __init__(self, name, created):
        self.name = name
        self.created = created


u = User("小石", datetime.datetime(2026, 9, 21))

# 自定义对象默认不能序列化
try:
    json.dumps(u.__dict__, ensure_ascii=False)
    print("  用 __dict__ 可以：", json.dumps(u.__dict__, ensure_ascii=False, default=str))
except TypeError as e:
    print("  失败：", e)


def json_default(obj):
    """遇到不认识的类型时，json 会调用这个函数"""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()      # datetime -> ISO 字符串
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, set):
        return sorted(obj)          # set -> 排序后的列表
    if hasattr(obj, "__dict__"):
        return obj.__dict__         # 自定义对象 -> 属性字典
    raise TypeError(f"无法序列化的类型：{type(obj)}")


payload = {
    "user": u,
    "time": datetime.datetime(2026, 9, 21, 12, 0),
    "tags": {"python", "canoe"},
}
print("  用 default 处理：", json.dumps(payload, ensure_ascii=False, default=json_default))

# ==========================================================
# 7. 实战：配置文件读写（最常见的用途）
# ==========================================================
print("\n--- 实战：配置管理 ---")

DEFAULT_CONFIG = {
    "app": {
        "name": "CAN 分析工具",
        "version": "1.0.0",
        "debug": True,
    },
    "can": {
        "channel": 0,
        "bitrate": 500000,
        "interface": "zhoulgong",  # 周立功
    },
    "log": {
        "level": "INFO",
        "file": "can.log",
    },
}


class Config:
    """配置管理类：自动创建、读取、修改、保存"""

    def __init__(self, path):
        self.path = Path(path)
        # 文件不存在就用默认配置创建一份
        if not self.path.exists():
            self.data = DEFAULT_CONFIG.copy()
            self.save()
            print(f"  配置文件不存在，已创建默认配置：{self.path}")
        else:
            self.data = self.load()

    def load(self):
        """读配置：文件损坏时回退到默认值，保证程序不崩"""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return DEFAULT_CONFIG.copy()
        except json.JSONDecodeError as e:
            print(f"  配置损坏（{e}），使用默认配置")
            return DEFAULT_CONFIG.copy()

    def save(self):
        """写配置"""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get(self, *keys, default=None):
        """按路径取值：get('can', 'bitrate')"""
        cur = self.data
        for k in keys:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return default
        return cur

    def set(self, value, *keys):
        """按路径设值并保存"""
        cur = self.data
        for k in keys[:-1]:
            cur = cur.setdefault(k, {})
        cur[keys[-1]] = value
        self.save()

    def __repr__(self):
        return f"Config({self.path})"


cfg_path = Path(tempfile.gettempdir()) / "can_tool_config.json"
if cfg_path.exists():
    cfg_path.unlink()  # 删掉重来，保证演示从「创建」开始

cfg = Config(cfg_path)
print("  读配置：bitrate =", cfg.get("can", "bitrate"))
print("  读配置：app.name =", cfg.get("app", "name"))
print("  读不存在的键：", cfg.get("can", "not_exist", default="默认值"))

cfg.set(250000, "can", "bitrate")  # 改配置并自动保存
print("  改完后：bitrate =", cfg.get("can", "bitrate"))

# ==========================================================
# 8. 实战：用 JSON 存结构化数据（测试用例）
# ==========================================================
print("\n--- 实战：CAN 测试用例 ---")

test_cases = [
    {
        "case_id": "TC001",
        "name": "车速信号校验",
        "can_id": "0x123",
        "data": "11 22 33 44 55 66 77 88",
        "expect": {"speed": 80, "unit": "km/h"},
    },
    {
        "case_id": "TC002",
        "name": "转速信号校验",
        "can_id": "0x456",
        "data": "AA BB CC DD",
        "expect": {"rpm": 3000},
    },
]

case_file = Path(tempfile.gettempdir()) / "test_cases.json"
# 写入测试用例（sort_keys=True 让键按字母排序，方便 diff 比对）
case_file.write_text(json.dumps(test_cases, ensure_ascii=False, indent=2, sort_keys=True),
                     encoding="utf-8")
print("  已写入", len(test_cases), "条用例")

# 读回来执行
loaded_cases = json.loads(case_file.read_text(encoding="utf-8"))
for c in loaded_cases:
    print(f"   执行 {c['case_id']} {c['name']}：期望 {c['expect']}")

# ==========================================================
# 9. 嵌套数据的增删改查
# ==========================================================
print("\n--- 嵌套数据操作 ---")
db = {
    "students": [
        {"id": 1, "name": "小石", "scores": {"python": 88, "canoe": 92}},
        {"id": 2, "name": "老张", "scores": {"python": 95, "canoe": 87}},
    ]
}

# 改：找到 id=1 的学生，把 python 分改成 90
for stu in db["students"]:
    if stu["id"] == 1:
        stu["scores"]["python"] = 90
print("  改完：", db["students"][0]["scores"])

# 查：所有人的 python 平均分
avg = sum(s["scores"].get("python", 0) for s in db["students"]) / len(db["students"])
print("  python 平均分：", avg)

# 增：给所有学生加一门课
for stu in db["students"]:
    stu["scores"]["ota"] = 0
print("  加课后：", db["students"][0]["scores"])

# 删：移除 canoe 成绩
for stu in db["students"]:
    stu["scores"].pop("canoe", None)  # 用 pop(k, None) 避免键不存在时报错
print("  删课后：", db["students"][0]["scores"])

# ==========================================================
# 10. 深拷贝：JSON 的另类用法
# ==========================================================
print("\n--- 用 JSON 做深拷贝 ---")
import copy

nested = {"a": [1, 2, {"b": 3}]}
# 浅拷贝只复制一层，嵌套的还是同一个对象
shallow = nested.copy()
shallow["a"][2]["b"] = 999
print("  浅拷贝改了嵌套，原对象也变：", nested["a"][2]["b"])  # 999

nested2 = {"a": [1, 2, {"b": 3}]}
# 深拷贝：json 转一圈（只适用于纯 JSON 数据）
deep1 = json.loads(json.dumps(nested2))
# 正规做法：copy.deepcopy（支持任意对象）
deep2 = copy.deepcopy(nested2)
deep1["a"][2]["b"] = 111
print("  深拷贝互不影响，原对象：", nested2["a"][2]["b"])  # 3

# ==========================================================
# 11. 其他数据格式（知道有这些就行）
# ==========================================================
print("\n--- 其他序列化格式 ---")
print("""  json     通用、可读、跨语言        -> 配置文件、接口（首选）
  pickle   Python 专用，能存任意对象  -> 只在本机用，⚠ 别反序列化陌生文件（有安全风险）
  csv      表格                      -> Excel 能直接打开（22 号文件讲过）
  yaml     比 JSON 更可读，支持注释   -> 配置文件（需要装 pyyaml）
  toml     现代配置格式              -> pyproject.toml（Python 3.11+ 内置 tomllib）
  sqlite   带查询能力的存储          -> 数据量大时用
""")

# tomllib 是 3.11+ 内置的（只读）
try:
    import tomllib
    print("  tomllib 可用（3.11+）")
except ImportError:
    print("  tomllib 不可用")

# pickle 简单演示
import pickle
obj_to_save = {"a": [1, 2, 3], "b": (4, 5)}  # 元组 pickle 能存，json 不行
pickled = pickle.dumps(obj_to_save)
print("  pickle 序列化：", pickled[:30], "...")
print("  反序列化（元组保住了）：", pickle.loads(pickled))

# ==========================================================
# 清理
# ==========================================================
for f in [tmp, cfg_path, case_file]:
    if f.exists():
        f.unlink()
print("\n临时文件已清理")


# ===== 练习（取消注释运行）=====
# 1. 写个函数 save_json(path, data) 和 load_json(path)，带异常处理
# def save_json(path, data):
#     with open(path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
# def load_json(path):
#     try:
#         with open(path, encoding='utf-8') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}
#
# 2. 把学生成绩字典存成 JSON，再读回来算平均分
# scores = {"小石": 88, "老张": 95}
# save_json('scores.json', scores)
# data = load_json('scores.json')
# print(sum(data.values()) / len(data))
#
# 3. 用 json 存一个待办清单，支持 add / list / done 三个操作
# todos = []
# def add(title): todos.append({"title": title, "done": False})
# def done(i): todos[i]["done"] = True
# def show():
#     for i, t in enumerate(todos):
#         print(("[x]" if t["done"] else "[ ]"), t["title"])
# add("学 Python 函数"); add("学文件操作"); done(0); show()
