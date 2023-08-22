from os import listdir
from os import path as os_path
from sys import path as sys_path

from pyglet import resource


def add_theme_dirs_to_path():
    check_dirs = [sys_path[0]]
    for check_dir in check_dirs:
        for file in listdir(check_dir):
            possible_directory = os_path.join(check_dir, file)
            if os_path.isdir(possible_directory):
                check_dirs.append(possible_directory)
                if file == "themes":
                    resource.path.append(possible_directory)
    resource.reindex()
resource.path.append(sys_path[0])
add_theme_dirs_to_path()