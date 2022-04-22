"""
Напишите функцию, которая будет по output команды ls возвращать средний размер файла в папке.
$ ls -l ./
В качестве аргумента функции должен выступать путь до файла с output команды ls
"""
import os

from module_02_linux.homework.hw_2_2_ps_aux_rss import _sizeof_fmt


def get_mean_size(ls_output_path: str) -> float:
    dir_files_list = os.listdir(os.path.join(ls_output_path))
    total_size = 0
    for i in dir_files_list:
        total_size += os.path.getsize(os.path.join(ls_output_path, i))
    return _sizeof_fmt(total_size / len(dir_files_list))


if __name__ == "__main__":
    print(get_mean_size("/home/user/PycharmProjects/python_advanced/module_01_flask/homework"))
