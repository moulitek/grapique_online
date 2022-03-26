from moulitek.moulitek import *
import os

data = []
Size = Category("Taille du dossier", "verification de la taille du repo < 15MB")
Basics = Category("Minimal functions", "verification des functions cruciales au bon fonctionnment d'un projet CSFML")

def get_trace():
    data = []
    os.system("python graphique.py > trace")
    try:
        text_file = open("trace", "r")
        data = text_file.read()
        data = [e for e in data.split('^') if len(e) > 0]
        data = [e for e in data[1].split('\n') if len(e) > 0]
        text_file.close()
    except:
        data = []
    os.system("rm trace")
    return data

def get_elem(lst, to_find):
    for elem in lst:
        if to_find in elem:
            return elem
    return "Oups"


data = get_trace()
## SIZE ##

sizerino = Size.add_sequence("folder Size")
sizerino.add_test("Size (< 15MB)")

for elem in data:
    if "size" in elem:
        sizerino.set_status("Size (< 15MB)", False, BADOUTPUT, expected="OK", got="size too big > 15M")
        break
    else:
        sizerino.set_status("Size (< 15MB)", True)

## MINIMAL FUNCS ##

graph_name = ["sprite", "Clock", "basic functions", "events", "music and sounds effect", "-h"]

for elem in graph_name:
    Minimal_functions = 0
    Minimal_functions = Basics.add_sequence(elem)
    Minimal_functions.add_test(elem)
    for uwu in data:
        if elem in uwu:
            Minimal_functions.set_status(elem, False, BADOUTPUT, expected="OK", got=get_elem(data, elem))
            break
        else:
            Minimal_functions.set_status(elem, True)
gen_trace()