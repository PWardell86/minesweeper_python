from pyglet import resource
from sys import path as sys_path
from os import path as os_path
from os import listdir

# Add all subdirectories named "themes" to the resource path
checkDirs = [sys_path[0]]
for checkDir in checkDirs:
    for file in listdir(checkDir):
        possible_directory = os_path.join(checkDir, file)
        if os_path.isdir(possible_directory):
            checkDirs.append(possible_directory)
            if file == "themes":
                resource.path.append(os_path.join(checkDir, file))

resource.reindex()