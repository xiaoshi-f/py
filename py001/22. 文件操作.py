# -*- coding: utf-8 -*-
# 22. 文件操作
# 知识点：open() 的打开模式、with 上下文管理（自动关闭）、
#        读文件 4 种方式、写文件的坑、编码问题（Windows 默认 GBK）、
#        pathlib 现代路径写法、csv 模块读写表格、 os.path 常用判断
#
# 为什么要学：前面的程序数据都在内存里，一关就没了。
#             文件操作 = 让程序能「记住」东西、能读别人的数据。

import os
import shutil
import tempfile
import csv
from pathlib import Path

# 演示目录放在系统临时目录里，不污染你的工作区
DEMO_DIR = Path(tempfile.gettempdir()) / "python_file_demo"
DEMO_DIR.mkdir(exist_ok=True)  # exist_ok=True：目录已存在也不报错
print("演示目录：", DEMO_DIR)

# ==========================================================
# 1. 打开文件：open(路径, 模式, encoding=编码)
# ==========================================================
# 模式速记（第二个字符 b 表示二进制，+ 表示既读又写）：
#   'r'  只读（默认）。文件不存在 -> 报错 FileNotFoundError
#   'w'  只写。文件不存在就新建；存在就【清空】！小心！
#   'a'  追加。在文件末尾接着写，不清空
#   'x'  新建。文件已存在 -> 报错（防止误覆盖）
#   'rb'/'wb'  二进制模式，图片/音频/固件包用这个，不能加 encoding

# ==========================================================
# 2. ❌ 错误写法：忘记关闭文件
# ==========================================================
# f = open(path, 'w')
# f.write("hello")
# # 忘了 f.close() -> 数据可能还在缓冲区没落盘，而且占用文件句柄
# 文件句柄泄漏：程序长时间跑，打开几千个文件不关，会 too many open files

# ==========================================================
# 3. ✅ 正确写法：with 语句（强烈推荐，永远用它）
# ==========================================================
# with 会在代码块结束时【自动调用 close()】，哪怕中间抛异常也会关
# 这叫「上下文管理器」，后面 27 号文件会讲它背后的原理

txt_path = DEMO_DIR / "hello.txt"

# 写文件：'w' 模式，encoding 必须显式写 utf-8（Windows 默认 GBK，中文会乱码）
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("第一行：你好 Python\n")
    f.write("第二行：文件操作\n")
    f.write("第三行：with 会自动关闭文件\n")
    # ⚠ 注意：write() 不会自动加换行，要自己写 \n

print("文件是否关闭：", f.closed)  # True，with 块结束自动关了

# ==========================================================
# 4. 读文件的四种方式
# ==========================================================
print("\n--- 方式1：read() 一次性全读（小文件用）---")
with open(txt_path, "r", encoding="utf-8") as f:
    content = f.read()  # 全部内容读成一个字符串
print(content)

print("--- 方式2：readline() 一次读一行 ---")
with open(txt_path, "r", encoding="utf-8") as f:
    print(repr(f.readline()))  # '第一行：你好 Python\n'，包含换行符
    print(repr(f.readline()))

print("--- 方式3：readlines() 读成列表，一行一个元素 ---")
with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(lines)  # ['第一行...\n', '第二行...\n', ...]

print("--- 方式4：直接迭代文件对象（最省内存，推荐）---")
# 文件对象本身就是可迭代的，一次只在内存里放一行
# 读几个 G 的日志也不会爆内存
with open(txt_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  第{i}行：{line.rstrip()}")  # rstrip() 去掉末尾换行

# ==========================================================
# 5. 追加模式 'a' 与新建模式 'x'
# ==========================================================
with open(txt_path, "a", encoding="utf-8") as f:  # a = append，不清空
    f.write("第四行：我是追加进来的\n")

with open(txt_path, "r", encoding="utf-8") as f:
    print("\n追加后共", len(f.readlines()), "行")

# 'x' 模式：文件已存在就报错，适合「不能覆盖重要文件」的场景
try:
    with open(txt_path, "x", encoding="utf-8") as f:
        f.write("这句不会执行")
except FileExistsError:
    print("'x' 模式检测到文件已存在，拒绝覆盖（安全）")

# ==========================================================
# 6. writelines()：写多行（不会自动加换行！）
# ==========================================================
lines_path = DEMO_DIR / "lines.txt"
data = ["苹果", "香蕉", "橘子"]
with open(lines_path, "w", encoding="utf-8") as f:
    # f.writelines(data)          # ❌ 会变成 "苹果香蕉橘子" 粘在一起
    f.writelines(item + "\n" for item in data)  # ✅ 自己补 \n
with open(lines_path, "r", encoding="utf-8") as f:
    print("writelines 结果：", f.read().splitlines())

# ==========================================================
# 7. 二进制模式：复制图片/固件（你的 OTA 升级包就是这么拷的）
# ==========================================================
bin_path = DEMO_DIR / "data.bin"
with open(bin_path, "wb") as f:  # 二进制不加 encoding 参数
    f.write(bytes(range(256)))  # 写入 0~255 共 256 字节

copy_path = DEMO_DIR / "data_copy.bin"
with open(bin_path, "rb") as src, open(copy_path, "wb") as dst:  # 同时开两个
    dst.write(src.read())  # 小文件一次性拷贝
print("二进制复制后大小：", copy_path.stat().st_size, "字节")

# 大文件要分块读，别一次性 read() 到内存
CHUNK = 64 * 1024  # 64KB 一块
big_copy = DEMO_DIR / "data_copy2.bin"
with open(bin_path, "rb") as src, open(big_copy, "wb") as dst:
    while True:
        chunk = src.read(CHUNK)
        if not chunk:  # 读完了，chunk 是空 bytes
            break
        dst.write(chunk)
print("分块复制后大小：", big_copy.stat().st_size, "字节")

# ==========================================================
# 8. pathlib：现代路径写法（推荐替代 os.path）
# ==========================================================
# 以前：os.path.join("a", "b", "c")   -> "a\b\c"
# 现在：Path("a") / "b" / "c"          -> 用 / 拼接，跨平台
p = DEMO_DIR / "sub" / "test.txt"
print("\n路径拼接：", p)
print("文件名：", p.name)          # test.txt
print("文件主干：", p.stem)        # test
print("后缀：", p.suffix)          # .txt
print("父目录：", p.parent)
print("是否存在：", p.exists())
print("父目录是否存在：", p.parent.exists())

# 创建多级目录：parents=True 连父目录一起建，exist_ok=True 已存在不报错
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("pathlib 直接写文件，不用 open", encoding="utf-8")
print("pathlib 读回：", p.read_text(encoding="utf-8"))

# glob：按通配符找文件
print("目录下所有 .txt：", [f.name for f in DEMO_DIR.glob("*.txt")])
print("递归找所有文件：", [f.name for f in DEMO_DIR.rglob("*")])

# ==========================================================
# 9. os.path / os 常用判断（老写法也要认得，老项目里全是它）
# ==========================================================
print("\n是文件吗：", os.path.isfile(txt_path))
print("是目录吗：", os.path.isdir(DEMO_DIR))
print("文件大小：", os.path.getsize(txt_path), "字节")
print("绝对路径：", os.path.abspath("."))
print("目录列表：", os.listdir(DEMO_DIR))

# ==========================================================
# 10. csv 模块：读写表格（导出测试数据很常用）
# ==========================================================
csv_path = DEMO_DIR / "scores.csv"
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    # ⚠ newline="" 必须加，否则 Windows 下每行之间会多一个空行
    writer = csv.writer(f)
    writer.writerow(["姓名", "科目", "分数"])  # 表头
    writer.writerows([
        ["小石", "Python", 88],
        ["老张", "Python", 95],
        ["小石", "CANoe", 92],
    ])

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print("  csv 行：", row)

# DictReader / DictWriter：按列名读写，更直观
with open(csv_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(f"  {row['姓名']} 的 {row['科目']} 是 {row['分数']} 分")

# ==========================================================
# 11. 实战：统计文件的行数、字符数、最长行
# ==========================================================
def analyze_file(path):
    """统计文本文件的基本信息"""
    line_count = 0
    char_count = 0
    longest = ""
    # 用迭代方式读，多大文件都不怕
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            char_count += len(line)
            if len(line) > len(longest):
                longest = line
    return {
        "行数": line_count,
        "字符数": char_count,
        "最长行": longest.rstrip(),
    }


print("\n文件统计：", analyze_file(txt_path))

# ==========================================================
# 12. 实战：安全写入（先写临时文件，成功再替换，防止写一半断电）
# ==========================================================
# 这是写配置文件/固件的标准套路：原子写
def safe_write(path, content):
    """先写 .tmp，再替换原文件，避免中途失败导致文件损坏"""
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()          # 刷到系统缓冲
        os.fsync(f.fileno())  # 强制落盘
    os.replace(tmp, path)  # 原子替换，要么全成功要么全不变


safe_write(DEMO_DIR / "config.txt", "version=1.0\n")
print("安全写入结果：", (DEMO_DIR / "config.txt").read_text(encoding="utf-8"))

# ==========================================================
# 清理演示目录（正式代码里不要随便删东西）
# ==========================================================
shutil.rmtree(DEMO_DIR)
print("\n演示目录已清理：", not DEMO_DIR.exists())


# ===== 练习（取消注释运行）=====
# 1. 写一个函数 copy_file(src, dst)，用分块读取的方式复制任意文件
# def copy_file(src, dst):
#     with open(src, 'rb') as s, open(dst, 'wb') as d:
#         while True:
#             chunk = s.read(1024 * 64)
#             if not chunk:
#                 break
#             d.write(chunk)
# copy_file('a.jpg', 'b.jpg')
#
# 2. 统计一个日志文件里每个错误级别（ERROR/WARN/INFO）出现的次数
# from collections import Counter
# c = Counter()
# with open('app.log', encoding='utf-8') as f:
#     for line in f:
#         for level in ('ERROR', 'WARN', 'INFO'):
#             if level in line:
#                 c[level] += 1
# print(c)
#
# 3. 用 pathlib 找出某个目录下所有大于 10MB 的文件，按大小倒序打印
# for f in sorted(Path('.').rglob('*'), key=lambda x: x.stat().st_size, reverse=True):
#     if f.is_file() and f.stat().st_size > 10 * 1024 * 1024:
#         print(f.stat().st_size, f)
