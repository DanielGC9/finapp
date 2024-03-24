from notion_client import Client
from pprint import pprint
import os
from memory_profiler import profile

t=10
@profile
def my_func():
    a = [1] * (t ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

my_func()