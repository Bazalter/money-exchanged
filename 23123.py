# import shutil
# class Pytho:
#     def __init__(self):
#         self.__priv = 1
#         self.ab = 2
#     @property
#     def ger_priv(self):
#         return self.__priv
#
#
#
# a = Pytho()
# print(a._Pytho__priv)


# shutil.make_archive('pepe', 'zip', "C:\\Users\\benit\\PycharmProjects")

# import json
#
# json_string = '{"name": "John", "age": 30}'
# data = json.loads(json_string)
#
# print(data)


# def decorator1(func):
#     def wrapper(*args, **kwargs):
#         print("Первый декоратор")
#         return func(*args, **kwargs)
#     return wrapper
#
# def decorator2(func):
#     def wrapper(*args, **kwargs):
#         print("Второй декоратор")
#         return func(*args, **kwargs)
#     return wrapper
#
# @decorator1
# @decorator2
# def say_hello(name):
#     print(f"Hello, {name}!")
#
# say_hello("Alice")