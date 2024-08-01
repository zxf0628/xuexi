"""
数据处理路由

书写格式注意：匹配的函数名称后一定不可有括号  否则视为提前调用 其他模块在调用认为是字符串
"""

from views import *

urls = [
    ("/hello", hello),
    ("/time", get_time)
]
