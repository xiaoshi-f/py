# -*- coding: utf-8 -*-
# 24. 模块与包
# 知识点：模块就是一个 .py 文件、四种 import 写法、as 起别名、
#        from ... import * 的危害、__all__ 控制导出、
#        if __name__ == '__main__' 到底防什么、模块搜索路径 sys.path、
#        __pycache__ 是什么、包（带 __init__.py 的文件夹）、相对导入、
#        标准库/第三方/自定义三类模块、pip 与 venv 虚拟环境
#
# 为什么要学：代码超过 300 行就该拆文件了，不然改一行要翻半天。
#             模块 = 拆分代码的第一层手段；包 = 模块的文件夹。

import os
import sys
import math
import random

# ==========================================================
# 1. 模块是什么：一个 .py 文件就是一个模块
# ==========================================================
# 模块名 = 文件名（去掉 .py）
# 模块里可以放：函数、类、变量、可执行语句
# 导入模块的本质：把那个文件执行一遍，然后把里面的名字拿过来用

print("--- 使用标准库模块 ---")
print("  math.pi =", math.pi)
print("  math.sqrt(16) =", math.sqrt(16))
print("  random.randint(1, 10) =", random.randint(1, 10))

# ==========================================================
# 2. import 的四种写法
# ==========================================================
print("\n--- 四种 import 写法 ---")

# 写法1：import 模块名 —— 用的时候要带前缀，最清晰，推荐
import math
print("  写法1：", math.floor(3.7))

# 写法2：import 模块名 as 别名 —— 名字太长或避免冲突时用
# 行业惯例别名（记住这几个）：
#   import numpy as np
#   import pandas as pd
#   import matplotlib.pyplot as plt
import math as m
print("  写法2：", m.ceil(3.2))

# 写法3：from 模块 import 名字 —— 直接用名字，不用前缀
from math import sqrt, pi
print("  写法3：", sqrt(9), pi)

# 写法4：from 模块 import 名字 as 别名
from math import factorial as fac
print("  写法4：", fac(5))

# ==========================================================
# 3. ⚠ from xxx import * 的危害（不要用）
# ==========================================================
# from math import *   # 把 math 里所有公开名字倒进来
# 危害：
#   1. 污染命名空间：你自己的 sqrt / pi 变量会被覆盖，而且很难发现
#   2. 看代码时不知道这个名字从哪来，可读性极差
#   3. 可能覆盖内置函数（比如某个模块里定义了 list 或 id）
# 唯一可接受的场景：交互式环境里图省事

# 如果模块作者不希望被 * 导入，用 __all__ 声明白名单（见下文）

# ==========================================================
# 4. 模块的内置属性
# ==========================================================
print("\n--- 模块属性 ---")
print("  当前模块名 __name__：", __name__)  # 直接运行时是 '__main__'
print("  模块的文件路径 __file__：", __file__)
print("  math 的文档：", (math.__doc__ or "").strip()[:20], "...")

# dir(模块)：列出模块里所有名字（调试时用来「摸清一个陌生模块」）
print("  math 里的名字（前 10 个）：", dir(math)[:10])

# help(模块名 / 函数名)：看详细文档
# help(math.sqrt)   # 取消注释试试

# ==========================================================
# 5. if __name__ == '__main__'：最重要的一个知识点
# ==========================================================
# 每个模块都有一个 __name__ 变量：
#   - 直接运行这个文件时，__name__ == '__main__'
#   - 被别的模块 import 时，__name__ == '模块名'
#
# 所以下面这个 if 的作用是：
#   「只有当我被直接运行时，才执行测试/演示代码；
#     被别人 import 时不要执行，只提供函数给别人用。」
#
# 为什么必须加？看这个例子：
# 假设 utils.py 里有：
#   def add(a, b): return a + b
#   print("测试：", add(1, 2))      # ← 这句在模块顶层
# 那么 main.py 里 import utils 时，那句 print 会立刻执行，
# 别人只是想用你的 add 函数，却被强塞了一堆输出。
# 加上 if __name__ == '__main__': 就能避免。

def add(a, b):
    """供其他模块使用的加法函数"""
    return a + b


print("\n--- __name__ 演示 ---")
print("  本文件 __name__ =", __name__)
# 注意：这个文件是被直接运行的，所以 __name__ 是 '__main__'
# 如果别的文件 import 它，这里的值就变成文件名了

# 标准写法：把「演示/测试代码」关进这个 if 里
if __name__ == "__main__":
    print("  这是只有直接运行时才会执行的演示代码")
    print("  add(1, 2) =", add(1, 2))

# ==========================================================
# 6. 模块的搜索路径 sys.path
# ==========================================================
print("\n--- 模块搜索顺序 ---")
# import 一个模块时，Python 按顺序在下面这些地方找：
#   1. 当前脚本所在目录
#   2. 环境变量 PYTHONPATH 指定的目录
#   3. 标准库目录
#   4. site-packages（pip 装的第三方包都在这）
print("  sys.path 前 3 项：")
for p in sys.path[:3]:
    print("   ", p)

# 找不到就 ImportError / ModuleNotFoundError
# 排查思路：print(sys.path) 看看目标目录在不在里面

# ⚠ 常见坑：把自己的文件命名为标准库同名（如 random.py、json.py、email.py）
# 会导致 import 时先找到你的文件，标准库被"遮蔽"，报错非常难查

# ==========================================================
# 7. __pycache__ 是什么
# ==========================================================
# 第一次 import 一个模块时，Python 会把它编译成字节码，
# 存到 __pycache__/模块名.cpython-314.pyc
# 下次 import 直接用缓存，启动更快
# - 它是自动生成的，可以整个删掉，不影响运行
# - 提交 Git 时要忽略（.gitignore 里加 __pycache__/）
print("\n--- 字节码缓存 ---")
print("  __pycache__ 是 Python 自动生成的字节码缓存目录，可安全删除")
print("  是否禁用字节码缓存：", sys.dont_write_bytecode)  # 加 -B 参数运行会是 True

# ==========================================================
# 8. 包（Package）：装模块的文件夹
# ==========================================================
# 目录结构示例：
#
#   myproject/
#   ├── main.py
#   └── mypkg/              <- 包
#       ├── __init__.py     <- 有这个文件，目录才是「包」（3.3+ 其实可省略，但建议保留）
#       ├── utils.py        <- 模块
#       └── models.py
#
# 导入方式：
#   import mypkg.utils
#   from mypkg import utils
#   from mypkg.utils import helper
#
# __init__.py 的作用：
#   1. 标记这是个包
#   2. 包被 import 时先执行它，可以在里面做初始化
#   3. 在里面写 from . import utils，就能直接 import mypkg 后使用 mypkg.utils
#   4. 定义 __all__ 控制 from mypkg import * 导出什么

print("\n--- 包的结构 ---")
print("""
  mypkg/
    __init__.py      # 包标识 + 初始化
    utils.py
    models.py
""")

# ==========================================================
# 9. __all__：控制被 import * 时导出哪些名字
# ==========================================================
# 在模块顶部写：
#   __all__ = ['public_func', 'PublicClass']
# 那么 from 该模块 import * 时，只会导入 __all__ 里列出的名字
# 没列出来的（哪怕是公开的）也不会被 * 导入
# 注意：__all__ 只影响 import *，直接 from x import y 依然能拿到

# 本文件如果写：
#   __all__ = ['add']
# 那么 from 本模块 import * 只会得到 add

# ==========================================================
# 10. 相对导入 vs 绝对导入
# ==========================================================
# 绝对导入（推荐）：从项目根目录写全路径
#   from mypkg.utils import helper
#
# 相对导入（只能在包内部用，用 . 表示当前包）：
#   from . import utils          # 同级模块
#   from .utils import helper    # 同级模块里的名字
#   from ..parent import thing   # 上级包
#
# ⚠ 相对导入只能在包内使用。直接运行一个用了相对导入的文件会报：
#   ImportError: attempted relative import with no known parent package
# 解决办法：用 python -m mypkg.module 的方式运行，而不是直接 python module.py

# ==========================================================
# 11. 三类模块
# ==========================================================
print("\n--- 模块分类 ---")
print("""  1. 标准库模块：Python 自带，直接 import
     os sys math random datetime json re collections itertools
     functools itertools pathlib logging unittest sqlite3 socket

  2. 第三方模块：pip 安装后使用
     requests（HTTP）  numpy/pandas（数据分析）
     python-can（CAN 总线，你的方向）  pyserial（串口）
     cantools（DBC 解析）  pytest（测试）

  3. 自定义模块：你自己写的 .py 文件
""")

# ==========================================================
# 12. pip 与虚拟环境（命令，不在 Python 代码里执行）
# ==========================================================
print("\n--- pip 常用命令（在命令行执行）---")
print("""  pip install 包名              安装包
  pip install 包名==1.2.3       装指定版本
  pip install -r requirements.txt   按清单批量装
  pip uninstall 包名            卸载
  pip list                      已装列表
  pip show 包名                 查看包信息
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名   # 清华源，国内快
""")

print("\n--- venv 虚拟环境（每个项目必配）---")
print("""  # 为什么需要：A 项目要 Django 2.0，B 项目要 Django 4.0，全局只能装一个
  # 虚拟环境 = 每个项目一套独立的 Python 包目录

  python -m venv venv                 # 创建（Windows）
  venv\\Scripts\\activate              # 激活（激活后命令行前面有 (venv)）
  pip install requests                # 装包装到虚拟环境里
  pip freeze > requirements.txt       # 导出依赖清单
  deactivate                          # 退出

  # Linux/Mac 激活命令不同：
  # source venv/bin/activate
""")

# ==========================================================
# 13. 查看模块信息的小工具
# ==========================================================
print("\n--- 自省：摸清一个陌生模块 ---")


def describe_module(mod):
    """打印模块里有哪些函数（排除下划线开头的内部名字）"""
    funcs = [n for n in dir(mod)
             if not n.startswith("_") and callable(getattr(mod, n))]
    print(f"  {mod.__name__} 有 {len(funcs)} 个公开可调用对象：")
    print("   ", funcs[:8], "..." if len(funcs) > 8 else "")


describe_module(math)
describe_module(random)

# 用 importlib 动态导入（模块名是字符串时用）
import importlib
mod = importlib.import_module("math")  # 等价于 import math
print("  动态导入 math.sqrt(25) =", mod.sqrt(25))

# 判断模块能不能导入（可选依赖的场景常用）
def has_module(name):
    """检查某个第三方模块是否已安装"""
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False


for name in ["json", "requests", "python_can"]:
    print(f"  {name} 可用：{has_module(name)}")

# ==========================================================
# 14. 单文件也可以当脚本用：命令行参数 sys.argv
# ==========================================================
print("\n--- sys.argv 命令行参数 ---")
print("  当前脚本名：", sys.argv[0])
print("  传入参数个数：", len(sys.argv) - 1)
print("""  用法（命令行）：python xxx.py arg1 arg2
  sys.argv = ['xxx.py', 'arg1', 'arg2']
  正式项目用 argparse 模块，能自动生成 --help
""")


# 一个典型的文件结构模板（照抄这个布局就行）
print("\n--- 推荐的模块文件模板 ---")
print('''  # -*- coding: utf-8 -*-
  """模块文档字符串：说明这个模块是干什么的"""

  import os            # 1. 标准库导入
  import sys

  import requests      # 2. 第三方库导入（空一行分开）

  from mypkg import x  # 3. 本地模块导入

  # 4. 常量（全大写）
  MAX_RETRY = 3

  # 5. 函数/类定义
  def do_something():
      """函数文档字符串"""
      pass

  # 6. 最后：入口保护
  if __name__ == "__main__":
      do_something()
''')


# ===== 练习（取消注释运行）=====
# 1. 自己写一个 mymath.py，里面放 add/sub/mul/div 四个函数，
#    在另一个文件里 import mymath 并调用，体会 __name__ 的作用
# # mymath.py
# def add(a, b): return a + b
# if __name__ == '__main__':
#     print('测试：', add(1, 2))
#
# 2. 用 importlib 写个小工具：输入模块名，打印它所有的公开函数
# def list_funcs(name):
#     mod = importlib.import_module(name)
#     return [n for n in dir(mod) if not n.startswith('_') and callable(getattr(mod, n))]
# print(list_funcs('string'))
#
# 3. 用 sys.argv 写一个脚本：python calc.py 3 + 5，输出 8
# import sys
# a, op, b = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
# print(eval(f"{a} {op} {b}"))   # 注意 eval 有安全风险，练习用可以
