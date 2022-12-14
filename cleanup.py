from os import popen
from time import sleep
import os

import re


def key_fun(name) -> int:
    num_str = re.findall("[0-9]*", name)[0]
    if not num_str:
        return 9999
    return int(num_str)


def cleanup(PTH):
    w = PTH + os.sep
    dirlist = os.listdir(w[:-1])
    dirlist.sort(key=key_fun)

    n = 0
    last_numbered_file = 0
    rename_rest = False

    for name in dirlist:
        suffix = name[-3:]
        if suffix == 'jpg' or suffix == 'png':
            if name[:-3].isdigit() and not rename_rest:
                number = int(re.findall("[0-9]*", name)[0])

                if number - last_numbered_file != 1:
                    rename_rest = True
                    os.rename(w + name, w + str(last_numbered_file + 1) + f".{suffix}")
                    sleep(0.2)
                    last_numbered_file += 1
                    continue
                last_numbered_file = number

            else:
                os.rename(w + name, w + str(last_numbered_file + 1) + f".{suffix}")
                sleep(0.2)
                last_numbered_file += 1
    print('cleanup done')
