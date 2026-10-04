# -*- coding: utf-8 -*-
# 29. 标准库 - time 与 datetime
# 知识点：时间戳 timestamp、time 模块的 sleep/strftime/strptime/ perf_counter、
#        datetime 的 date/time/datetime/timedelta、
#        格式化符号 %Y %m %d %H %M %S、字符串与日期互转、
#        日期加减、时区 timezone、实战（倒计时/日志时间戳/性能测试）
#
# 为什么要学：日志要打时间、定时要 sleep、统计要算间隔、
#             解析 CAN 报文里的时间戳也靠它。

import time
import datetime
from datetime import datetime as dt, date, time as dtime, timedelta, timezone

# ==========================================================
# 1. 时间戳：从 1970-01-01 00:00:00 UTC 到现在的秒数
# ==========================================================
print("--- 时间戳 ---")
ts = time.time()
print("  当前时间戳（秒，带小数）：", ts)
print("  整数秒：", int(ts))
print("  毫秒：", int(ts * 1000))
# 时间戳的好处：全球统一、方便计算间隔、存数据库省空间
# 2038 年问题：32 位系统的 time_t 溢出（Python 用 float，不受影响）

# ==========================================================
# 2. time 模块的三大用途
# ==========================================================
print("\n--- time 模块 ---")

# ① 睡眠（让程序暂停）
print("  sleep 前：", time.strftime("%H:%M:%S"))
time.sleep(0.1)  # 暂停 0.1 秒
print("  sleep 后：", time.strftime("%H:%M:%S"))

# ② 高精度计时（测代码性能用 perf_counter，不要用 time.time()）
start = time.perf_counter()
sum(range(1_000_00))   # 随便算点东西
cost = time.perf_counter() - start
print(f"  耗时：{cost * 1000:.3f} ms")
# perf_counter 是单调时钟，不受系统时间被修改的影响，是计时的唯一正确选择

# ③ 格式化与解析
print("  time.strftime：", time.strftime("%Y-%m-%d %H:%M:%S"))
print("  带中文：", time.strftime("%Y年%m月%d日 %H时%M分%S秒"))
print("  本地时间结构：", time.localtime().tm_year, "年")
print("  UTC 时间结构：", time.gmtime().tm_hour, "点（UTC）")

# 字符串 -> 时间元组（老式解析）
t_tuple = time.strptime("2026-09-21 19:30:00", "%Y-%m-%d %H:%M:%S")
print("  strptime 解析：", t_tuple.tm_year, t_tuple.tm_mon, t_tuple.tm_mday)
# 元组 -> 时间戳
print("  转回时间戳：", int(time.mktime(t_tuple)))

# ==========================================================
# 3. datetime：现代日期时间处理（推荐用它替代 time）
# ==========================================================
print("\n--- datetime 基础 ---")
now = dt.now()          # 本地当前时间（naive，不带时区信息）
# ⚠ dt.utcnow() 从 3.12 起已弃用：它返回的 UTC 时间不带时区标记，
#    后面做时区运算容易出错。正确写法是下面这种：
utc_now2 = dt.now(timezone.utc)  # ✅ 带时区信息的 UTC 时间
print("  现在：", now)
print("  UTC：", utc_now2)
print("  今天：", date.today())
print("  时间部分：", now.time())

# 手动构造
d = dt(2026, 9, 21, 19, 30, 0)
print("  构造：", d)
print("  取各部分：", d.year, d.month, d.day, d.hour, d.minute, d.second)
print("  星期几（0=周一）：", d.weekday(), "| isoweekday（1=周一）：", d.isoweekday())
print("  一年第几天：", d.timetuple().tm_yday)

# ==========================================================
# 4. 格式化：datetime -> 字符串（strftime）
# ==========================================================
print("\n--- strftime 格式化 ---")
# 常用格式化符号（背这几个够用）：
#   %Y 四位年 2026      %y 两位年 26
#   %m 月 09            %d 日 21
#   %H 24小时制 19      %I 12小时制 07     %p AM/PM
#   %M 分                %S 秒              %f 微秒
#   %a 星期缩写 Mon      %A 星期全名 Monday
#   %b 月份缩写 Sep      %B 月份全名 September
#   %j 一年第几天        %U 一年第几周
#   %z 时区偏移 +0800    %Z 时区名
#   %% 字面百分号
print("  标准格式：", now.strftime("%Y-%m-%d %H:%M:%S"))
print("  中文格式：", now.strftime("%Y年%m月%d日 %H:%M:%S"))
print("  文件名安全格式：", now.strftime("%Y%m%d_%H%M%S"))  # 不能有冒号
print("  带星期：", now.strftime("%Y-%m-%d %A"))
print("  ISO 格式：", now.isoformat())  # 2026-09-21T19:30:00.123456
print("  只要日期：", now.date().isoformat())

# ==========================================================
# 5. 解析：字符串 -> datetime（strptime）
# ==========================================================
print("\n--- strptime 解析 ---")
s1 = "2026-09-21 19:30:00"
d1 = dt.strptime(s1, "%Y-%m-%d %H:%M:%S")
print("  解析：", d1, type(d1).__name__)

s2 = "21/09/2026"
d2 = dt.strptime(s2, "%d/%m/%Y")
print("  日/月/年格式：", d2)

# 解析失败会 ValueError，实际项目里要 try 包住
try:
    dt.strptime("不是日期", "%Y-%m-%d")
except ValueError as e:
    print("  解析失败：", str(e)[:50])

# 常见格式汇总（解析别人的日志时用得上）
formats = [
    ("2026-09-21", "%Y-%m-%d"),
    ("2026/09/21", "%Y/%m/%d"),
    ("2026-09-21 19:30", "%Y-%m-%d %H:%M"),
    ("2026-09-21T19:30:00", "%Y-%m-%dT%H:%M:%S"),  # ISO8601
    ("21-Sep-2026", "%d-%b-%Y"),
]
for s3, fmt in formats:
    print(f"   {s3:22} -> {dt.strptime(s3, fmt)}")

# ==========================================================
# 6. timedelta：时间加减
# ==========================================================
print("\n--- timedelta 时间计算 ---")
now = dt.now()
print("  现在：", now.strftime("%Y-%m-%d %H:%M:%S"))
print("  加 1 天：", (now + timedelta(days=1)).strftime("%Y-%m-%d"))
print("  减 2 小时：", (now - timedelta(hours=2)).strftime("%H:%M"))
print("  加 1 周：", (now + timedelta(weeks=1)).strftime("%Y-%m-%d"))
# timedelta 支持的参数：weeks days hours minutes seconds milliseconds microseconds
print("  复杂组合：", (now + timedelta(days=3, hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M"))

# 两个 datetime 相减 = timedelta
d_a = dt(2026, 9, 21)
d_b = dt(2026, 12, 31)
diff = d_b - d_a
print(f"  相距：{diff.days} 天，{diff.total_seconds() / 3600:.0f} 小时")

# timedelta 的属性
td = timedelta(days=2, hours=3, minutes=4)
print("  timedelta 的 days：", td.days, "| seconds：", td.seconds)
print("  总秒数：", td.total_seconds())

# ==========================================================
# 7. 时区处理
# ==========================================================
print("\n--- 时区 ---")
# 不带时区的 datetime 叫「naive」，带时区的叫「aware」
# ⚠ naive 和 aware 不能互相比较，会 TypeError

# 构造时区：timezone(timedelta(hours=8))
tz_cn = timezone(timedelta(hours=8), "CST")   # 中国标准时间 UTC+8
tz_utc = timezone.utc

cn_time = dt.now(tz_cn)
utc_time = dt.now(tz_utc)
print("  北京时间：", cn_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
print("  UTC 时间：", utc_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
print("  相差小时：", (cn_time - utc_time).total_seconds() / 3600)

# 时区转换：astimezone
beijing = dt(2026, 9, 21, 12, 0, tzinfo=tz_cn)
new_york = beijing.astimezone(timezone(timedelta(hours=-4)))
print("  北京 12:00 对应纽约：", new_york.strftime("%H:%M"))

# ⚠ Python 3.9+ 才内置 zoneinfo（支持 'Asia/Shanghai' 这种名字）
try:
    from zoneinfo import ZoneInfo
    try:
        sh = dt.now(ZoneInfo("Asia/Shanghai"))
        print("  zoneinfo 上海：", sh.strftime("%Y-%m-%d %H:%M:%S %Z"))
    except Exception as e:
        # Windows 上 Python 不带系统时区数据库，需要 pip install tzdata
        print(f"  zoneinfo 取不到时区数据：{type(e).__name__}")
        print("  解决：pip install tzdata（Windows 平台需要）")
except ImportError:
    print("  zoneinfo 不可用（需要 Python 3.9+）")

# ==========================================================
# 8. 时间戳与 datetime 互转
# ==========================================================
print("\n--- 时间戳 <-> datetime ---")
ts = time.time()
# 时间戳 -> datetime（本地时区）
print("  fromtimestamp：", dt.fromtimestamp(ts))
# 时间戳 -> datetime（UTC）
print("  utcfromtimestamp（已弃用，用下面这种）：")
print("  fromtimestamp(ts, tz=utc)：", dt.fromtimestamp(ts, tz=timezone.utc))
# datetime -> 时间戳
d5 = dt(2026, 9, 21, 12, 0, 0)
print("  timestamp()：", d5.timestamp())
# ⚠ 注意：naive datetime 调 timestamp() 会按本地时区解释，容易出偏差
#    建议统一用带时区的 datetime，或者全程用 UTC

# ==========================================================
# 9. 实战1：性能测试装饰器（time 的经典用法）
# ==========================================================
print("\n--- 实战：计时装饰器 ---")
from functools import wraps


def timeit(func):
    """统计函数耗时的装饰器（19 号文件讲过装饰器）"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # perf_counter 是高精度单调时钟，专门用于测间隔
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"   {func.__name__} 耗时 {time.perf_counter() - t0:.6f}s")
        return result
    return wrapper


@timeit
def slow_task():
    return sum(i * i for i in range(200_000))


slow_task()

# ==========================================================
# 10. 实战2：日志时间戳（打日志必备）
# ==========================================================
print("\n--- 实战：带时间戳的日志 ---")


def log(msg, level="INFO"):
    """简易日志函数：时间 + 级别 + 内容"""
    ts = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 精确到毫秒
    print(f"   [{ts}] [{level}] {msg}")


log("程序启动")
log("连接 ECU 成功")
log("CAN 报文超时", "WARN")
# 正式项目用 logging 模块，能自动分级别、写文件、按大小切分

# ==========================================================
# 11. 实战3：倒计时与定时任务
# ==========================================================
print("\n--- 实战：倒计时 ---")


def countdown(seconds):
    """倒计时：每秒打印剩余时间"""
    for i in range(seconds, 0, -1):
        print(f"   {i}...", end=" ", flush=True)  # flush=True 强制立刻输出
        time.sleep(0.05)  # 演示用 0.05 秒，实际是 1
    print("   时间到！")


countdown(3)

# 计算距离某个日期还有多久
target = dt(2026, 10, 1)  # 国庆
remain = target - dt.now()
print(f"   距离 2026-10-01 还有 {remain.days} 天 "
      f"{remain.seconds // 3600} 小时")

# ==========================================================
# 12. 实战4：CAN 报文时间戳解析（你的方向）
# ==========================================================
print("\n--- 实战：报文时间戳 ---")


class CanFrame:
    """CAN 帧：带时间戳（车载总线分析常用）"""

    def __init__(self, can_id, data, timestamp=None):
        self.can_id = can_id
        self.data = data
        # 没传时间戳就用当前时间
        self.timestamp = timestamp or dt.now()

    def __repr__(self):
        # 报文时间精确到毫秒，方便分析时序
        t = self.timestamp.strftime("%H:%M:%S.%f")[:-3]
        data_hex = " ".join(f"{b:02X}" for b in self.data)
        return f"[{t}] ID=0x{self.can_id:03X} DATA={data_hex}"


f1 = CanFrame(0x123, bytes([0x11, 0x22, 0x33]))
time.sleep(0.02)
f2 = CanFrame(0x123, bytes([0x11, 0x23, 0x33]))
print("  ", f1)
print("  ", f2)
delta_ms = (f2.timestamp - f1.timestamp).total_seconds() * 1000
print(f"   两帧间隔：{delta_ms:.1f} ms")

# 计算报文周期（周期报文的周期稳定性是诊断项之一）
frames = [CanFrame(0x456, b"\x01"), CanFrame(0x456, b"\x02")]
print("   周期稳定性分析：间隔越大越可能丢帧")

# ==========================================================
# 13. 常用操作速查
# ==========================================================
print("\n--- 速查 ---")
print("""  时间戳          time.time()                    -> float 秒
  高精度计时       time.perf_counter()            -> 测间隔专用
  睡眠             time.sleep(秒)
  datetime 格式化  dt.strftime("%Y-%m-%d %H:%M:%S")
  字符串解析       dt.strptime(s, "%Y-%m-%d")
  时间加减         dt.now() + timedelta(days=1)
  时间差           (d2 - d1).total_seconds()
  今天             date.today()
  ISO 格式         dt.now().isoformat()
  时区             dt.now(timezone(timedelta(hours=8)))
""")


# ===== 练习（取消注释运行）=====
# 1. 写个函数 days_between(d1, d2)，返回两个日期字符串之间相差的天数
# def days_between(d1, d2):
#     a = dt.strptime(d1, "%Y-%m-%d")
#     b = dt.strptime(d2, "%Y-%m-%d")
#     return (b - a).days
# print(days_between("2026-01-01", "2026-12-31"))
#
# 2. 写个函数 is_weekend(date_str)，判断是不是周末
# def is_weekend(date_str):
#     return dt.strptime(date_str, "%Y-%m-%d").weekday() >= 5
# print(is_weekend("2026-09-21"))
#
# 3. 写个装饰器，统计函数被调用的总次数和总耗时
# def stats(func):
#     func.total_time = 0
#     func.call_count = 0
#     @wraps(func)
#     def wrapper(*a, **kw):
#         t0 = time.perf_counter()
#         r = func(*a, **kw)
#         func.total_time += time.perf_counter() - t0
#         func.call_count += 1
#         return r
#     return wrapper
