# -*- coding: utf-8 -*-
# 31. 正则表达式
# 知识点：正则是什么、re 模块四大函数 match/search/findall/sub、
#        元字符 . * + ? [] () ^ $ \d \w \s、
#        量词与贪婪/非贪婪、分组与反向引用、预编译 compile、
#        常用 flag（IGNORECASE / MULTILINE / DOTALL）、
#        ⚠ 原生字符串 r"" 必须加、split / finditer、实战（提取/校验/替换）
#
# 为什么要学：从一堆文本里「按规则」找东西。
#             解析日志、校验手机号邮箱、提取 CAN 报文数据，全靠它。

import re

# ==========================================================
# 1. 正则是什么：用一串特殊字符描述「字符串的模式」
# ==========================================================
# 比如：找出所有手机号 -> 1 开头 + 后面 10 位数字 -> 正则写 1\d{10}
# ⚠ 关键习惯：正则字符串前面一定要加 r（raw string）
#   r"\d+"   正确：\d 原样传给正则引擎
#   "\d+"    也能用，但 "\n" "\t" 会被 Python 先转义，坑很多
print("--- 为什么要用原生字符串 r'' ---")
print(r"  r'\d' =", repr(r"\d"), "（两个字符：反斜杠 + d）")
print("  '\\d' =", repr("\\d"), "（Python 里 \\d 不是转义序列，刚好也行）")
print(r"  但 '\n' 会被 Python 当换行，r'\n' 才是正则的换行符")

# ==========================================================
# 2. 四个核心函数（先记住这张表）
# ==========================================================
#   re.match(pattern, s)     从【开头】匹配，只找第一个 -> Match 对象或 None
#   re.search(pattern, s)    扫【整个字符串】，找第一个  -> Match 对象或 None
#   re.findall(pattern, s)   找出【所有】匹配           -> 列表
#   re.sub(pattern, repl, s) 替换所有匹配              -> 新字符串
#   re.split(pattern, s)     按匹配切分                -> 列表
#   re.finditer(pattern, s)  找出所有（迭代器，省内存） -> 迭代器

text = "我的电话是 13812345678，备用号码 13900001111"
print("\n--- match vs search ---")
print("  原文：", text)

# match 只从开头找：开头是"我的"，不是数字，所以 None
m1 = re.match(r"\d+", text)
print("  match(r'\\d+')：", m1)  # None

# search 扫全文，找到第一个数字串
m2 = re.search(r"\d+", text)
print("  search(r'\\d+')：", m2.group() if m2 else None)  # 13812345678

# findall 找全部
print("  findall(r'\\d+')：", re.findall(r"\d+", text))

# ==========================================================
# 3. 常用元字符（正则的字母表）
# ==========================================================
print("\n--- 元字符速查 ---")
print("""  .        任意字符（除换行）
  \\d       数字 0-9          \\D  非数字
  \\w       字母数字下划线      \\W  非单词字符
  \\s       空白符（空格/tab/换行）  \\S  非空白
  \\b       单词边界
  ^        字符串开头         $   字符串结尾
  [abc]    字符集合：a 或 b 或 c
  [a-z]    范围：a 到 z
  [^abc]   取反：除了 a/b/c
  a|b      或者：a 或 b
  ()       分组，可以单独取出
""")

# ==========================================================
# 4. 量词（控制前面那个字符出现几次）
# ==========================================================
print("\n--- 量词 ---")
print("""  *        0 次或多次
  +        1 次或多次
  ?        0 次或 1 次
  {n}      恰好 n 次
  {n,}     至少 n 次
  {n,m}    n 到 m 次
""")

samples = ["a", "abc", "abbc", "abbbc", "ac"]
pattern = r"ab*c"  # a + 0个或多个b + c
print(f"  模式 {pattern} 匹配情况：")
for s in samples:
    print(f"    {s:8} -> {bool(re.match(pattern, s))}")

# ? 的两种身份：
#   跟在字符后面 = 量词（0或1次）
#   跟在量词后面 = 非贪婪标记（见下文）
print("\n  ab?c（b 可有可无）：", [s for s in samples if re.match(r"ab?c", s)])

# ==========================================================
# 5. ⚠ 贪婪 vs 非贪婪（经典坑）
# ==========================================================
print("\n--- 贪婪 vs 非贪婪 ---")
html = "<div>标题</div><div>内容</div>"

# 默认贪婪：* 和 + 会尽可能多地吃字符
greedy = re.search(r"<div>.*</div>", html)
print("  贪婪 .*：", greedy.group())  # 一整串都吃进去了

# 非贪婪：量词后面加 ?，尽可能少地吃
lazy = re.search(r"<div>.*?</div>", html)
print("  非贪婪 .*?：", lazy.group())  # 只匹配第一个 div

# 提取所有 div 内容
print("  所有 div 内容：", re.findall(r"<div>(.*?)</div>", html))

# ==========================================================
# 6. 分组 ()：提取子串
# ==========================================================
print("\n--- 分组提取 ---")
# 用 () 把想要的部分括起来，findall 会只返回括号里的内容
text2 = "张三 25岁，李四 30岁，王五 28岁"
print("  原文：", text2)
print("  提取姓名和年龄：", re.findall(r"(\w+)\s(\d+)岁", text2))

# Match 对象的取法
m = re.search(r"(\w+)\s(\d+)岁", text2)
if m:
    print("  group(0)（整个匹配）：", m.group(0))
    print("  group(1)（第一个分组）：", m.group(1))
    print("  group(2)（第二个分组）：", m.group(2))
    print("  groups()（所有分组）：", m.groups())
    print("  位置 span()：", m.span())

# 命名分组：(?P<名字>...) 让代码可读性更高
m3 = re.search(r"(?P<name>\w+)\s(?P<age>\d+)岁", text2)
if m3:
    print("  命名分组取值：", m3.group("name"), m3.group("age"))

# 非捕获分组 (?:...)：只用来分组，不占编号
print("  非捕获分组：", re.findall(r"(?:\w+)\s(\d+)岁", text2))

# ==========================================================
# 7. 字符类 [] 与取反
# ==========================================================
print("\n--- 字符类 ---")
mixed = "abc123 XYZ!@#"
print("  所有字母：", re.findall(r"[a-zA-Z]+", mixed))
print("  所有数字：", re.findall(r"[0-9]+", mixed))
print("  非字母数字：", re.findall(r"[^a-zA-Z0-9\s]+", mixed))
print("  元音字母：", re.findall(r"[aeiou]", "hello world"))

# ==========================================================
# 8. 锚点 ^ 和 $
# ==========================================================
print("\n--- 锚点 ---")
# ^ 开头，$ 结尾。用来做「完整匹配校验」
print("  ^abc 匹配 'abcdef'：", bool(re.match(r"^abc", "abcdef")))
print("  ^abc 匹配 'xabc'：", bool(re.search(r"^abc", "xabc")))
print("  abc$ 匹配 'xxabc'：", bool(re.search(r"abc$", "xxabc")))
# fullmatch：整个字符串必须完全匹配（3.4+）
print("  fullmatch(r'\\d+', '123')：", bool(re.fullmatch(r"\d+", "123")))
print("  fullmatch(r'\\d+', '123a')：", bool(re.fullmatch(r"\d+", "123a")))

# ==========================================================
# 9. sub：替换
# ==========================================================
print("\n--- sub 替换 ---")
s = "2026-09-21 是我入学的日子"
print("  原文：", s)
print("  日期改成斜杠：", re.sub(r"-", "/", s))
print("  隐藏所有数字：", re.sub(r"\d", "*", s))
print("  只替换前 2 个：", re.sub(r"\d", "*", s, count=2))

# 用函数做替换（repl 可以是函数，接收 Match 对象）
def double_num(m):
    """把匹配到的数字翻倍"""
    return str(int(m.group()) * 2)


print("  数字翻倍：", re.sub(r"\d+", double_num, "我有 3 个苹果和 5 个梨"))

# 反向引用：\1 \2 引用前面的分组
print("  交换年月日：", re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\2/\3/\1", "2026-09-21"))
print("  去重叠字：", re.sub(r"(.)\1+", r"\1", "好好好好学习"))  # 好好学习

# ==========================================================
# 10. split：按模式切分
# ==========================================================
print("\n--- split ---")
line = "小石, 老张;  阿岩|李工"
print("  按多种分隔符切：", re.split(r"[,;|\s]+", line))
# 普通 str.split 只能按一种分隔符，正则可以按「一类字符」切

# ==========================================================
# 11. 预编译 compile：重复使用时提速
# ==========================================================
print("\n--- 预编译 ---")
# 如果一个正则要用很多次（比如循环里处理几万条日志），先编译
pattern_obj = re.compile(r"\d{4}-\d{2}-\d{2}")
# 编译后直接调用对象的方法，省掉每次解析正则的开销
print("  pattern.search：", pattern_obj.search("日期 2026-09-21").group())
print("  pattern.findall：", pattern_obj.findall("2026-09-21 和 2026-10-01"))
# 只在循环里大量使用才需要，偶尔用一次直接 re.xxx 就行

# ==========================================================
# 12. flag 标志位
# ==========================================================
print("\n--- flag ---")
# re.IGNORECASE (re.I)  忽略大小写
print("  忽略大小写：", re.findall(r"python", "Python PYTHON python", re.I))
# re.MULTILINE (re.M)   ^ 和 $ 匹配每行的开头结尾（而不是整个字符串）
multi = "第一行\n第二行\n第三行"
print("  多行模式找行首：", re.findall(r"^第.", multi, re.M))
# re.DOTALL (re.S)  让 . 也能匹配换行符
print("  DOTALL 跨行匹配：", re.search(r"第一行.*第三行", multi, re.S).group()[:10])
# re.VERBOSE (re.X)  允许在正则里写注释和空白，方便写复杂正则
complex_pattern = re.compile(r"""
    \d{3}      # 区号 3 位
    -          # 分隔符
    \d{4}      # 号码 4 位
""", re.VERBOSE)
print("  VERBOSE 模式：", complex_pattern.search("电话 010-1234").group())

# ==========================================================
# 13. 实战1：校验（手机号 / 邮箱 / IP / 车牌）
# ==========================================================
print("\n--- 实战：格式校验 ---")

validators = {
    "手机号": r"^1[3-9]\d{9}$",
    "邮箱": r"^[\w.+-]+@[\w-]+\.[\w.]+$",
    "IPv4": r"^(\d{1,3}\.){3}\d{1,3}$",
    "日期": r"^\d{4}-\d{2}-\d{2}$",
    "车牌": r"^[京沪粤浙苏鲁豫冀川渝]{1}[A-Z]{1}[A-Z0-9]{5}$",
    "纯数字": r"^\d+$",
    "强密码": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$",  # 前瞻断言：必须含大小写和数字
}

tests = [
    ("手机号", "13812345678"),
    ("手机号", "23812345678"),
    ("邮箱", "xiaoshi@example.com"),
    ("邮箱", "不是邮箱"),
    ("日期", "2026-09-21"),
    ("车牌", "豫A12345"),
    ("强密码", "Abc12345"),
    ("强密码", "weak"),
]

for category, value in tests:
    ok = bool(re.match(validators[category], value))
    print(f"   {category:8} {value:22} -> {'✅ 合法' if ok else '❌ 不合法'}")

# 前瞻断言 (?=...) 解释：
#   (?=.*[a-z])  后面必须存在一个小写字母（但不消耗字符）
#   (?!...)      后面必须不是...
print("\n  前瞻断言 (?=.*\\d)：必须包含数字 ->",
      bool(re.match(r"^(?=.*\d).{6,}$", "abcdef1")))

# ==========================================================
# 14. 实战2：解析日志（最常见的用途）
# ==========================================================
print("\n--- 实战：日志解析 ---")

log_lines = [
    "2026-09-21 10:23:15 [INFO] 连接 ECU 成功",
    "2026-09-21 10:23:16 [WARN] CAN 总线负载 78%",
    "2026-09-21 10:23:20 [ERROR] 报文 0x123 超时",
    "2026-09-21 10:23:25 [ERROR] 报文 0x456 校验失败",
]

# 一行拆成：时间、级别、内容
log_pattern = re.compile(
    r"(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"\[(?P<level>\w+)\]\s+"
    r"(?P<msg>.+)"
)

parsed = []
for line in log_lines:
    m = log_pattern.match(line)
    if m:
        parsed.append(m.groupdict())  # 命名分组 -> 字典，非常方便
        print(f"   [{m.group('level'):5}] {m.group('time')}  {m.group('msg')}")

# 统计各级别数量
from collections import Counter
print("  级别统计：", dict(Counter(p["level"] for p in parsed)))
# 只看 ERROR
errors = [p for p in parsed if p["level"] == "ERROR"]
print("  错误条数：", len(errors))

# ==========================================================
# 15. 实战3：提取 CAN 报文（你的方向）
# ==========================================================
print("\n--- 实战：CAN 报文解析 ---")

can_log = """
  (1695283395.123456)  vcan0  123#1122334455667788
  (1695283395.223456)  vcan0  456#AABBCCDD
  (1695283396.023456)  can1   7E0#022110
"""
# candump 格式：  (时间戳) 接口 ID#数据
can_pattern = re.compile(
    r"\((?P<ts>[\d.]+)\)\s+"
    r"(?P<iface>\w+)\s+"
    r"(?P<can_id>[0-9A-Fa-f]+)#"
    r"(?P<data>[0-9A-Fa-f]*)"
)

frames = []
for m in can_pattern.finditer(can_log):
    frames.append({
        "timestamp": float(m.group("ts")),
        "interface": m.group("iface"),
        "can_id": int(m.group("can_id"), 16),  # 16 进制字符串转数字
        "data": m.group("data"),
    })

for f in frames:
    print(f"   ID=0x{f['can_id']:03X} 接口={f['interface']:5} "
          f"数据={f['data']:16} 时间={f['timestamp']:.3f}")

# 计算报文间隔（周期分析）
if len(frames) >= 2:
    interval = frames[1]["timestamp"] - frames[0]["timestamp"]
    print(f"   前两帧间隔：{interval * 1000:.1f} ms")

# ==========================================================
# 16. 实战4：脱敏与清洗
# ==========================================================
print("\n--- 实战：数据脱敏 ---")
user_info = "姓名：小石，手机：13812345678，身份证：410101199001011234"
print("  原文：", user_info)
# 手机号中间 4 位打码
masked = re.sub(r"(1[3-9]\d)(\d{4})(\d{4})", r"\1****\3", user_info)
print("  脱敏后：", masked)

# ==========================================================
# 17. ⚠ 正则的坑
# ==========================================================
print("\n--- 常见坑 ---")
print("""  1. 忘记加 r 前缀：正则里的 \\d \\b 会被 Python 先解释，行为诡异
  2. 用 match 当 search 用：match 只从开头找，找不到就 None
  3. 贪婪匹配吃太多：默认 .* 会吃到最后，要加 ? 变非贪婪
  4. 特殊字符没转义：. * + ? ( ) [ ] { } ^ $ \\ | 都要用 \\ 转义
     或者放进 re.escape(字符串) 自动转义
  5. 用正则解析 HTML/XML：不要！用 BeautifulSoup / lxml
  6. 正则太复杂没人看得懂：复杂逻辑宁可多写几行字符串处理
""")

# re.escape：把字符串里的特殊字符自动转义（拼接用户输入时必用）
user_input = "1.5+2"
print("  用户输入：", user_input)
print("  转义后：", re.escape(user_input))
print("  安全匹配：", bool(re.search(re.escape(user_input), "结果是 1.5+2 吗")))


# ===== 练习（取消注释运行）=====
# 1. 提取一段文本里所有的邮箱地址
# text = "联系 a@x.com 或 b@y.cn"
# print(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text))
#
# 2. 把 "hello_world_java" 转成驼峰 "helloWorldJava"
# def to_camel(s):
#     return re.sub(r"_(\w)", lambda m: m.group(1).upper(), s)
# print(to_camel("hello_world_java"))
#
# 3. 写个函数统计一段英文里每个单词出现的次数（用 re.findall + Counter）
# from collections import Counter
# def word_count(text):
#     return Counter(re.findall(r"\b\w+\b", text.lower()))
# print(word_count("Hello hello world"))
