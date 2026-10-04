# -*- coding: utf-8 -*-
# 23. 异常处理
# 知识点：异常是什么、try/except/else/finally 四段各自何时执行、
#        捕获多个异常、as e 拿错误信息、Exception 兜底、raise 主动抛出、
#        自定义异常类、异常链 raise ... from、常见内置异常类型、
#        ⚠ 裸 except 的危害、assert 断言
#
# 为什么要学：不会异常处理的程序，遇到一个意外输入就崩溃退出。
#             真实项目里，异常用来「优雅地失败」而不是直接死。

# ==========================================================
# 1. 异常是什么：程序运行时出的错
# ==========================================================
# 常见内置异常（记住这几个就够用一阵）：
#   SyntaxError        语法错误（写代码时就该发现，except 抓不到）
#   NameError          用了没定义的变量
#   TypeError          类型不对，如 '1' + 1
#   ValueError         类型对但值不对，如 int('abc')
#   IndexError         列表下标越界
#   KeyError           字典键不存在
#   ZeroDivisionError  除以 0
#   FileNotFoundError  文件不存在
#   AttributeError     对象没有这个属性
#   ImportError        导入模块失败
#   KeyboardInterrupt  用户按 Ctrl+C（继承自 BaseException，不是 Exception）

# 不处理就是这个下场（取消注释看效果）：
# print(1 / 0)   # ZeroDivisionError: division by zero，程序直接终止

# ==========================================================
# 2. 最基础的 try / except
# ==========================================================
print("--- 基础 try/except ---")
try:
    # try 里放「可能出错的代码」，要尽量短，只包住真正危险的那句
    result = 10 / 0
except ZeroDivisionError:
    # 只有抛出指定类型异常时才进来
    print("  除数为 0，不能算")

print("  程序继续往下走了，没崩")

# ==========================================================
# 3. as e：拿到异常的详细信息
# ==========================================================
print("\n--- as e 获取错误信息 ---")
try:
    num = int("abc")
except ValueError as e:
    print("  错误类型：", type(e).__name__)
    print("  错误内容：", e)  # invalid literal for int() with base 10: 'abc'

# ==========================================================
# 4. 捕获多个异常
# ==========================================================
print("\n--- 捕获多个异常 ---")


def safe_div(a, b):
    """安全除法，处理多种异常"""
    try:
        return a / b
    except ZeroDivisionError:
        return "除数不能为 0"
    except TypeError:
        return "必须是数字"


print(" ", safe_div(10, 2))    # 5.0
print(" ", safe_div(10, 0))    # 除数不能为 0
print(" ", safe_div(10, "a"))  # 必须是数字

# 一个 except 抓多种异常：写成元组
def safe_div2(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError) as e:
        return f"出错了：{e}"


print(" ", safe_div2(1, "x"))

# ==========================================================
# 5. else 与 finally（很多人搞不清这两段）
# ==========================================================
print("\n--- else / finally ---")
#   try:     可能出错的代码
#   except:  出错时执行
#   else:    【没出错】才执行（和 for/while 的 else 一个思路）
#   finally: 【无论是否出错，一定执行】—— 用来释放资源（关文件、断连接、解锁）

def divide_with_log(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  except：除数为 0")
    else:
        # 只有 try 成功走完才进来
        # 把「成功后的操作」放这里，而不是塞进 try，可以让 try 保持干净
        print(f"  else：计算成功，结果是 {result}")
        return result
    finally:
        # 哪怕 try 里 return 了、except 里也 return 了，finally 照样执行
        print("  finally：无论如何都会执行（回收资源）")


divide_with_log(10, 2)
divide_with_log(10, 0)

# ⚠ 注意 finally 里的 return 会「吞掉」前面的 return/异常，别这么写
def bad_finally():
    try:
        return "try 的返回值"
    finally:
        return "finally 覆盖了它"  # 最终返回这句


print(" ", bad_finally())

# ==========================================================
# 6. 兜底：Exception 与 BaseException
# ==========================================================
print("\n--- 兜底捕获 ---")


def robust(func, *args):
    """不管什么错都兜住，返回 None"""
    try:
        return func(*args)
    except Exception as e:
        # Exception 是所有「常规异常」的父类
        # 它抓不到 KeyboardInterrupt / SystemExit（那些是 BaseException 的子类）
        print(f"  捕获到 {type(e).__name__}：{e}")
        return None


robust(lambda: [1, 2][5])      # IndexError
robust(lambda: {}["key"])      # KeyError

# ⚠ 千万别写裸 except：
# try:
#     do_something()
# except:          # 裸 except == except BaseException，连 Ctrl+C 都拦
#     pass         # 还会把真正的 bug 悄悄吞掉，最难排查的那种
# 至少要写成 except Exception as e: 并且打印/记录日志

# ==========================================================
# 7. raise：主动抛出异常
# ==========================================================
print("\n--- raise 主动抛出 ---")


def set_age(age):
    """设置年龄，不合法就抛异常"""
    if not isinstance(age, int):
        # 主动抛出异常：类型错了
        raise TypeError("年龄必须是整数")
    if age < 0 or age > 150:
        # 值不合理
        raise ValueError(f"年龄 {age} 不在 0~150 范围内")
    return age


for a in [18, -5, "二十"]:
    try:
        set_age(a)
        print(f"  {a} 合法")
    except (TypeError, ValueError) as e:
        print(f"  {a} 不合法：{e}")

# 在 except 里再抛：可以先记日志，再原样往上抛给调用方
def process(data):
    try:
        return int(data)
    except ValueError as e:
        print("  记录日志：转换失败，数据 =", data)
        raise  # 单独一个 raise = 把当前异常原样重新抛出


try:
    process("abc")
except ValueError:
    print("  上层又接住了一次")

# ==========================================================
# 8. 自定义异常类
# ==========================================================
print("\n--- 自定义异常 ---")
# 继承 Exception（业务异常一般都继承它，不要继承 BaseException）
# 好处：调用方可以精确地 except 你自己定义的异常类型


class InsufficientFundsError(Exception):
    """余额不足异常"""

    def __init__(self, balance, amount):
        self.balance = balance   # 把上下文信息挂到异常对象上
        self.amount = amount
        # 调用父类构造，设置异常信息文本
        super().__init__(f"余额不足：当前 {balance} 元，需要 {amount} 元")


class InvalidAccountError(Exception):
    """账户非法异常"""
    pass  # 不需要额外信息时，一个 pass 就行


def withdraw(balance, amount, account_valid=True):
    """取钱"""
    if not account_valid:
        raise InvalidAccountError("账户已被冻结")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


for args in [(100, 30), (100, 200), (100, 50, False)]:
    try:
        print("  取款后余额：", withdraw(*args))
    except InsufficientFundsError as e:
        # 能拿到自定义属性，做精细化处理
        print(f"  {e}（差额 {e.amount - e.balance} 元）")
    except InvalidAccountError as e:
        print("  账户问题：", e)

# ==========================================================
# 9. 异常链：raise ... from
# ==========================================================
print("\n--- raise ... from 保留原始异常 ---")


def load_config():
    """加载配置，把底层异常包装成业务异常但不丢根因"""
    try:
        with open("not_exist.ini", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        # from e 会保留原始异常，打印时能看到
        # "The above exception was the direct cause of..."
        raise RuntimeError("配置文件读取失败，请检查安装") from e
    # 如果写 raise RuntimeError(...) 不带 from，会显示
    # "During handling of the above exception, another exception occurred"


try:
    load_config()
except RuntimeError as e:
    print("  上层收到：", e)
    print("  根本原因：", type(e.__cause__).__name__)

# ==========================================================
# 10. 用异常做「重试」和「用完了才算完」
# ==========================================================
print("\n--- 实战：带异常处理的输入校验 ---")


def get_int(prompt_times=3):
    """最多试 3 次，把输入转成整数（这里用预设值模拟输入）"""
    inputs = ["abc", "12.5", "42"]  # 模拟用户三次输入
    for i in range(prompt_times):
        raw = inputs[i]
        try:
            return int(raw)
        except ValueError:
            print(f"  第{i + 1}次输入 '{raw}' 不是整数，重试")
    else:
        # for 的 else：循环正常走完（没 break/return）才执行
        print("  三次都失败，放弃")
        return None


print("  最终结果：", get_int())

# ==========================================================
# 11. EAFP vs LBYL：Python 的哲学
# ==========================================================
print("\n--- EAFP：先做了再说，错了再补 ---")
# LBYL（Look Before You Leap）：三思而后行 —— 先检查再操作
# EAFP（Easier to Ask Forgiveness than Permission）：先操作，出错再处理
# Python 更推崇 EAFP，因为异常在 Python 里开销很低

d = {"a": 1}

# LBYL 写法（啰嗦，而且还有竞态问题：检查完可能状态已变）
if "b" in d:
    print("  ", d["b"])
else:
    print("  键不存在（LBYL）")

# EAFP 写法（推荐）
try:
    print("  ", d["b"])
except KeyError:
    print("  键不存在（EAFP）")

# dict 的 setdefault / get 也是这种思路的封装
print("  get 带默认值：", d.get("b", 0))

# ==========================================================
# 12. assert 断言：调试用，不是错误处理
# ==========================================================
print("\n--- assert ---")
# assert 条件, "提示信息"
# 条件为假 -> 抛 AssertionError
# ⚠ 别用 assert 做参数校验：python -O 运行时所有 assert 会被跳过
# assert 只用于「绝对不该发生」的内部检查

def calc_average(nums):
    assert len(nums) > 0, "列表不能为空"  # 调试期保护
    return sum(nums) / len(nums)


print(" ", calc_average([1, 2, 3]))
try:
    calc_average([])
except AssertionError as e:
    print("  断言触发：", e)


# ===== 练习（取消注释运行）=====
# 1. 写一个 safe_int(s, default=0)：转换失败返回默认值而不是崩溃
# def safe_int(s, default=0):
#     try:
#         return int(s)
#     except (TypeError, ValueError):
#         return default
# print(safe_int("abc"), safe_int("12"), safe_int(None))
#
# 2. 写 read_json_file(path)，文件不存在返回 {}，格式错误打印提示
# import json
# def read_json_file(path):
#     try:
#         with open(path, encoding='utf-8') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}
#     except json.JSONDecodeError as e:
#         print("JSON 格式错误：", e)
#         return {}
#
# 3. 自定义一个 PasswordTooShortError，写注册函数校验密码长度 >= 8
# class PasswordTooShortError(Exception):
#     pass
# def register(pwd):
#     if len(pwd) < 8:
#         raise PasswordTooShortError("密码至少 8 位")
#     return "注册成功"
# try:
#     print(register("123"))
# except PasswordTooShortError as e:
#     print(e)
