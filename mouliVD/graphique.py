import os
from socket import getnameinfo
import sys
from unicodedata import category

from moulitek.moulitek import *


test_failed = []


def get_folder_size():
    os.system("du -hs > output")
    try:
        text_file = open("output", "r")
        data = text_file.read()
        data = [e for e in data.split('\t') if len(e) > 0]
        text_file.close()
    except:
        exit(168)
    os.system("rm output")
    return data[0]


def check_size():
    size = get_folder_size()
    if size[-1] == 'G':
        return 0
    if size[-1] == 'K':
        return 1
    if size[-1] == 'M':
        if int(round(float(size[:-1]))) < 15:
            return 1
        else:
            return 0
    return 1


def check_event():
    total = 0
    total += greperino("event.type", 3)
    total += greperino("sfEvent", 1)
    total += greperino("sfRenderWindow_pollEvent", 1)
    return total == 3


def basic_window():
    total = 0
    total += greperino("sfVideoMode", 1)
    total += greperino("sfClose", 1)
    total += greperino("sfRenderWindow", 1)
    total += greperino("sfRenderWindow_create", 1)
    total += greperino("sfRenderWindow_setFramerateLimit", 1)
    total += greperino("sfEvtClosed", 1)
    return total == 6


def check_music():
    total = 0
    total += greperino("sfMusic *", 2)
    total += greperino("sfSound *", 2)
    total += greperino("sfMusic_play", 2)
    total += greperino("sfSoundBuffer_destroy", 2)
    total += greperino("sfSound_destroy", 2)
    return total == 5

def greperino(cmd, edge):
    true_cmd = "grep -r --include='*.c' --include='*.h' \"" + cmd + "\" > output"
    print(true_cmd)
    os.system(true_cmd)
    try:
        text_file = open("output", "r")
        data = text_file.read()
        data = [e for e in data.split('\n') if len(e) > 0]
        text_file.close()
    except:
        exit(168)
    os.system("rm output")
    if len(data) >= edge:
        return 1
    return 0


def check_help(mode):
    if mode == "-s":
        mode = "my_screensaver"
    if mode == "-r":
        mode = "my_runner"
    if mode == "-rpg":
        mode = "my_rpg"
    if mode == "-d":
        mode = "my_defender"
    if mode == "-h":
        mode = "my_hunter"
    if mode == "-cringe":
        mode = "my_radar"
    if mode == "-w":
        mode = "my_world"
    os.system("make")
    cmd = "./" + mode + " -h > output"
    os.system(cmd)
    try:
        text_file = open("output", "r")
        data = text_file.read()
        text_file.close()
    except:
        exit(168)
    return len(data) >= 50

try:
    mode = sys.argv[1]
except:
    mode = "-h"

if check_size() == 0:
    test_failed.append("size too big > 15M")

if greperino("sfSprite \*", 7) == False:
    test_failed.append("Not enougt sprite used")

if greperino("sfClock *", 3) == 0:
    test_failed.append("Not enougt sfClock used")

if basic_window() == 0:
    test_failed.append("basic functions missing")

if check_event() == 0:
    test_failed.append("Missing events")

if check_music() == 0:
    test_failed.append("Not enought music and sounds effect")

if check_help(mode) == 0:
    test_failed.append("missing or incomplet -h")

print("^")
for elem in test_failed:
    print(elem)
if len(test_failed) == 0:
    print("GG")
gen_trace()

