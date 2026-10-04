# -*- coding: utf-8 -*-
# 28. 标准库 - os 与 sys（外加 pathlib）
# 知识点：os 操作系统交互、os.path 路径处理、目录遍历 os.walk、
#        环境变量 os.environ、执行系统命令 os.system / subprocess、
#        sys.argv 命令行参数、sys.path 模块搜索路径、sys.exit 退出、
#        sys.stdout 重定向、pathlib 现代路径（推荐）、shutil 高级文件操作
#
# 为什么要学：写工具脚本必备。批量改文件名、遍历目录找文件、
#             读环境变量配置、让脚本接受命令行参数——全靠这两个模块。

import os
import sys
import shutil
import tempfile
from pathlib import Path

# 准备一个演示目录（放在系统临时目录，不污染工作区）
DEMO = Path(tempfile.gettempdir()) / "python_os_demo"
if DEMO.exists():
    shutil.rmtree(DEMO)
(DEMO / "sub1" / "deep").mkdir(parents=True)
(DEMO / "sub2").mkdir(parents=True)
(DEMO / "a.txt").write_text("aaa", encoding="utf-8")
(DEMO / "b.log").write_text("log", encoding="utf-8")
(DEMO / "sub1" / "c.py").write_text("print(1)", encoding="utf-8")
(DEMO / "sub1" / "deep" / "d.txt").write_text("ddd", encoding="utf-8")

# ==========================================================
# 1. os 基本信息
# ==========================================================
print("--- os 基本信息 ---")
print("  操作系统类型 os.name：", os.name)          # Windows='nt', Linux='posix'
print("  路径分隔符 os.sep：", repr(os.sep))         # Windows='\\', Linux='/'
print("  当前工作目录 os.getcwd()：", os.getcwd())
print("  当前用户：", os.environ.get("USERNAME") or os.environ.get("USER"))
# 平台判断（跨平台脚本常用）
print("  是不是 Windows：", sys.platform.startswith("win"))

# ==========================================================
# 2. os.path：路径处理（老写法，但老项目里到处都是）
# ==========================================================
print("\n--- os.path 常用函数 ---")
p = str(DEMO / "sub1" / "c.py")
print("  原始路径：", p)
print("  basename：", os.path.basename(p))       # c.py
print("  dirname：", os.path.dirname(p))         # 目录部分
print("  拆分：", os.path.split(p))              # (目录, 文件名) 元组
print("  拆扩展名：", os.path.splitext(p))       # (主干, '.py')
print("  是否存在：", os.path.exists(p))
print("  是文件吗：", os.path.isfile(p))
print("  是目录吗：", os.path.isdir(p))
print("  文件大小：", os.path.getsize(p), "字节")
print("  绝对路径：", os.path.abspath("."))
print("  规范化（处理 .. 和 .）：", os.path.normpath("a/../b/./c"))

# ⚠ 拼接路径永远用 os.path.join，不要手写字符串拼：
#   错误：path = "dir" + "\\" + "file.txt"   # Linux 上就废了
#   正确：path = os.path.join("dir", "file.txt")  # 自动用对应平台的分隔符
print("  拼接 join：", os.path.join("dir", "sub", "file.txt"))

# ==========================================================
# 3. pathlib：现代写法（推荐，代码更短更直观）
# ==========================================================
print("\n--- pathlib（推荐）---")
pd = Path(DEMO) / "sub1" / "c.py"
print("  用 / 拼接：", pd)
print("  .name：", pd.name)
print("  .stem：", pd.stem)          # 不带后缀的文件名
print("  .suffix：", pd.suffix)
print("  .parent：", pd.parent)
print("  .parts：", pd.parts)        # 拆成元组
print("  .exists()：", pd.exists())
print("  .is_file()：", pd.is_file())
print("  .is_dir()：", pd.is_dir())
print("  .stat().st_size：", pd.stat().st_size)
print("  with_suffix：", pd.with_suffix(".bak"))
print("  with_name：", pd.with_name("new.py"))
# 读写一步到位，不用 open
print("  read_text：", pd.read_text(encoding="utf-8"))

# 路径运算对照表（记住这套）：
#   os.path.join(a, b)     ->  Path(a) / b
#   os.path.basename(p)    ->  Path(p).name
#   os.path.dirname(p)     ->  Path(p).parent
#   os.path.exists(p)      ->  Path(p).exists()
#   os.listdir(d)          ->  Path(d).iterdir()
#   os.makedirs(d)         ->  Path(d).mkdir(parents=True)

# ==========================================================
# 4. 目录操作
# ==========================================================
print("\n--- 目录操作 ---")
print("  os.listdir（只列当前层）：", sorted(os.listdir(DEMO)))
print("  Path.iterdir：", sorted(x.name for x in DEMO.iterdir()))
print("  只列文件：", sorted(x.name for x in DEMO.iterdir() if x.is_file()))
print("  只列目录：", sorted(x.name for x in DEMO.iterdir() if x.is_dir()))

# 创建目录
new_dir = DEMO / "new" / "nested"
new_dir.mkdir(parents=True, exist_ok=True)  # parents=建多级, exist_ok=已存在不报错
print("  创建多级目录：", new_dir.exists())

# os.makedirs 是老写法：os.makedirs(path, exist_ok=True)
# 注意：不加 exist_ok=True 时目录已存在会抛 FileExistsError

# 重命名 / 移动
src = DEMO / "a.txt"
dst = DEMO / "a_renamed.txt"
src.rename(dst)                      # pathlib 方式
print("  重命名后：", dst.exists())
os.rename(str(dst), str(DEMO / "a.txt"))  # os 方式（要字符串路径）

# 删除：rmdir 只能删【空目录】，非空会报 OSError
try:
    (DEMO / "new").rmdir()  # new 里面还有 nested，删不掉
except OSError as e:
    print("  非空目录 rmdir 失败：", e.strerror or e)

# 正确做法：从最里层往外删，或者直接用 shutil.rmtree 整棵树删掉
(DEMO / "new" / "nested").rmdir()    # 先删子目录
(DEMO / "new").rmdir()               # 再删父目录
print("  由内往外删，成功：", not (DEMO / "new").exists())

# ==========================================================
# 5. os.walk：递归遍历目录树（找文件神器）
# ==========================================================
print("\n--- os.walk 递归遍历 ---")
# os.walk(顶层目录) 每次返回三元组 (当前目录, 子目录列表, 文件列表)
# 它是个生成器，一层一层往下走
for root, dirs, files in os.walk(DEMO):
    # root：当前正在看的目录
    # dirs：这个目录下的子目录名列表
    # files：这个目录下的文件名列表
    level = str(root).replace(str(DEMO), "").count(os.sep)
    indent = "  " * level
    print(f"  {indent}{os.path.basename(root) or '根'}/")
    for f in files:
        print(f"  {indent}  - {f}")

# 实战：找出目录下所有 .txt 文件
txt_files = []
for root, dirs, files in os.walk(DEMO):
    for f in files:
        if f.endswith(".txt"):
            txt_files.append(os.path.join(root, f))
print("  所有 txt 文件：", [Path(x).name for x in txt_files])

# pathlib 的等价写法更简洁：rglob 递归匹配
print("  rglob('*.txt')：", [f.name for f in DEMO.rglob("*.txt")])
print("  glob('*.txt')（只当前层）：", [f.name for f in DEMO.glob("*.txt")])

# 实战：按后缀统计文件数量
from collections import Counter
suffix_count = Counter(f.suffix for f in DEMO.rglob("*") if f.is_file())
print("  后缀统计：", dict(suffix_count))

# ==========================================================
# 6. 环境变量 os.environ
# ==========================================================
print("\n--- 环境变量 ---")
# 环境变量是操作系统级别的键值对，常用来放配置（数据库密码、API Key、路径）
print("  PATH 的前 2 段：", os.environ.get("PATH", "")[:60], "...")
print("  取不到给默认值：", os.environ.get("MY_NOT_EXIST_KEY", "默认值"))

# 设置环境变量（只对当前进程及子进程有效，不会改系统的）
os.environ["DEMO_KEY"] = "demo_value"
print("  设置后读取：", os.environ["DEMO_KEY"])

# ⚠ 直接用 os.environ['不存在的键'] 会 KeyError，一律用 .get()
# 项目里读配置的典型写法：
#   DB_HOST = os.environ.get("DB_HOST", "localhost")
#   DEBUG = os.environ.get("DEBUG", "0") == "1"

# ==========================================================
# 7. 执行系统命令
# ==========================================================
print("\n--- 执行外部命令 ---")
# 方式1：os.system（最简单，但拿不到输出，只返回退出码）
# 不推荐用于正式项目
code = os.system("echo hello from shell")  # Windows 下用 echo
print("  os.system 返回码：", code)  # 0 表示成功

# 方式2：subprocess（推荐，能拿输出、能传参、更安全）
import subprocess
r = subprocess.run(
    [sys.executable, "-c", "print('子进程输出：hello')"],  # 命令和参数分开写，防注入
    capture_output=True,   # 捕获 stdout/stderr
    text=True,             # 输出转成字符串而不是 bytes
    encoding="utf-8",
)
print("  subprocess 返回码：", r.returncode)
print("  stdout：", r.stdout.strip())

# ⚠ 安全提醒：绝不要 shell=True + 拼接用户输入
#   危险：subprocess.run(f"rm -rf {user_input}", shell=True)
#   正确：subprocess.run(["rm", "-rf", user_input], shell=False)

# 方式3：os.startfile（Windows 用默认程序打开文件）
# os.startfile("report.pdf")   # 用默认 PDF 阅读器打开

# ==========================================================
# 8. sys：解释器相关
# ==========================================================
print("\n--- sys 常用属性 ---")
print("  Python 版本 sys.version：", sys.version.split()[0])
print("  版本信息 sys.version_info：", sys.version_info[:3])
print("  运行平台 sys.platform：", sys.platform)
print("  可执行文件：", sys.executable)
print("  默认编码：", sys.getdefaultencoding())
print("  递归上限：", sys.getrecursionlimit())

# sys.argv：命令行参数（写 CLI 工具的基础）
print("\n--- sys.argv ---")
print("  argv[0]（脚本名）：", sys.argv[0])
print("  argv 长度：", len(sys.argv))
# 命令行运行：python 28.py 参数1 参数2
# sys.argv = ['28.py', '参数1', '参数2']

# 简单参数处理示例（正式项目用 argparse）
args = sys.argv[1:]  # 去掉脚本名
if args:
    print("  收到的参数：", args)
else:
    print("  （没有传参数）")

# sys.exit：提前退出程序
# sys.exit(0)        # 0 = 正常退出
# sys.exit("错误信息")  # 传字符串会打印到 stderr 并以状态码 1 退出
print("  sys.exit(0) 用来在出错时提前结束脚本")

# sys.path：模块搜索路径（import 找不到模块时先查这里）
print("\n--- sys.path ---")
print("  共", len(sys.path), "项，前 3 项：")
for p2 in sys.path[:3]:
    print("   ", p2)
# 临时加搜索路径（不推荐常用，正规做法是装包或配 PYTHONPATH）
# sys.path.insert(0, "/path/to/my/modules")

# ==========================================================
# 9. shutil：高级文件操作
# ==========================================================
print("\n--- shutil ---")
# 复制文件
shutil.copy2(DEMO / "a.txt", DEMO / "a_copy.txt")  # copy2 保留元数据
print("  复制文件：", (DEMO / "a_copy.txt").exists())

# 复制整个目录树
shutil.copytree(DEMO / "sub1", DEMO / "sub1_backup")
print("  复制目录树：", (DEMO / "sub1_backup").exists())

# 移动/重命名（跨设备也行）
shutil.move(str(DEMO / "a_copy.txt"), str(DEMO / "a_moved.txt"))
print("  移动文件：", (DEMO / "a_moved.txt").exists())

# 删除目录树（⚠ 危险：整个目录连内容一起删，没有回收站）
shutil.rmtree(DEMO / "sub1_backup")
print("  删除目录树：", not (DEMO / "sub1_backup").exists())

# 磁盘空间
total, used, free = shutil.disk_usage(DEMO)
print(f"  磁盘：总 {total // 2**30}GB，已用 {used // 2**30}GB，剩余 {free // 2**30}GB")

# 查找可执行程序路径
print("  python 在哪：", shutil.which("python") or shutil.which("python3"))

# ==========================================================
# 10. 实战：批量重命名（把目录下所有 .txt 加前缀）
# ==========================================================
print("\n--- 实战：批量重命名 ---")


def batch_rename(directory, prefix, suffix_filter=".txt"):
    """给目录下指定后缀的文件统一加前缀"""
    directory = Path(directory)
    count = 0
    # 用 list() 包一层：避免在遍历的同时修改目录内容
    for f in list(directory.glob(f"*{suffix_filter}")):
        new_name = prefix + f.name
        f.rename(f.parent / new_name)
        count += 1
        print(f"   {f.name} -> {new_name}")
    return count


print("  改了", batch_rename(DEMO, "pre_"), "个文件")

# ==========================================================
# 11. 实战：找出目录下最大的 N 个文件
# ==========================================================
print("\n--- 实战：找大文件 ---")


def find_large_files(directory, top_n=3):
    """找出目录下最大的几个文件"""
    files = [f for f in Path(directory).rglob("*") if f.is_file()]
    # 按大小倒序排，取前 N 个
    files.sort(key=lambda f: f.stat().st_size, reverse=True)
    return [(f.name, f.stat().st_size) for f in files[:top_n]]


print("  ", find_large_files(DEMO))

# ==========================================================
# 12. 实战：项目目录扫描器（把学到的串起来）
# ==========================================================
print("\n--- 实战：统计项目代码行数 ---")


def count_code_lines(directory, extensions=(".py",)):
    """统计目录下指定后缀文件的总行数（跳过空行和注释行）"""
    stats = {"文件数": 0, "总行数": 0, "有效行": 0}
    for f in Path(directory).rglob("*"):
        if f.is_file() and f.suffix in extensions:
            try:
                # errors='ignore' 防止遇到二进制或奇怪编码时崩掉
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue  # 打不开就跳过
            stats["文件数"] += 1
            for line in content.splitlines():
                stats["总行数"] += 1
                s = line.strip()
                # 跳过空行和纯注释行
                if s and not s.startswith("#"):
                    stats["有效行"] += 1
    return stats


# 统计 py 文件所在目录（就是这门课的代码目录）
code_dir = Path(__file__).parent
print("  本目录统计：", count_code_lines(code_dir))

# ==========================================================
# 清理
# ==========================================================
shutil.rmtree(DEMO)
print("\n演示目录已清理：", not DEMO.exists())


# ===== 练习（取消注释运行）=====
# 1. 写个脚本：传入目录路径，打印该目录下所有文件的名字和大小，按大小排序
# import sys
# d = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
# for f in sorted(d.rglob('*'), key=lambda x: x.stat().st_size, reverse=True):
#     if f.is_file():
#         print(f.stat().st_size, f.name)
#
# 2. 写个函数 find_files(directory, keyword)，找出文件名包含 keyword 的所有文件
# def find_files(directory, keyword):
#     return [f for f in Path(directory).rglob('*') if keyword in f.name]
# print(find_files('.', '函数'))
#
# 3. 用 os.walk 统计某个目录下每个子目录各占多少空间
# def dir_sizes(root):
#     result = {}
#     for r, dirs, files in os.walk(root):
#         size = sum(os.path.getsize(os.path.join(r, f)) for f in files)
#         result[r] = size
#     return result
# print(dir_sizes('.'))
