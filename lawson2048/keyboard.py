#from evdev import uinput, ecodes as e
import time
import random

from threading import Lock

mutex = Lock()

#ui = uinput.UInput()
ui = None

output = ""

def keypress(ui, key):
    global output
    global mutex
    mutex.acquire()
    try:
        output += "gm.inputManager.emit(\"move\", {});\n".format(key)+'document.getElementById("last").textContent = "'+ui+'";\n\n'
    finally:
        mutex.release()
    print "keypress %s" % (key,)

def getKeypresses():
    global output
    global mutex
    mutex.acquire()
    b = ""
    try:
        b = output
        output = ""
    finally:
        mutex.release()
    return b

def up():
    keypress("up", 0)

def down():
    keypress("down", 2)

def left():
    keypress("left", 3)

def right():
    keypress("right", 1)

def scalePctAlpha(num):
    return num / 200.0  + .5


def update_pct(up, down, left, right):
    ''' in = 4 int values 0-100 in pct
    '''
    global output
    global mutex
    mutex.acquire()
    #print "u{} d{} l{} r{}".format(up, down, left, right)

    try:
        output += "\ndocument.getElementById('up-outline').style.opacity = {};\n".format(scalePctAlpha(up))
        output += "\ndocument.getElementById('down-outline').style.opacity = {};\n".format(scalePctAlpha(down))
        output += "\ndocument.getElementById('left-outline').style.opacity = {};\n".format(scalePctAlpha(left))
        output += "\ndocument.getElementById('right-outline').style.opacity = {};\n".format(scalePctAlpha(right))

    finally:
        mutex.release()
