import sys
from PyQt5.QtCore import *

weirdkeys = [Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5, Qt.Key_F6, Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10, Qt.Key_F11, Qt.Key_F12,
Qt.Key_Tab, Qt.Key_CapsLock, Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_AltGr,
Qt.Key_Space, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]

def weirdKeyGenerator():
    for i in weirdkeys:
        yield i

def qtKeyToHuman(key):
    generator = weirdKeyGenerator()
    if key == next(generator):
        return "F1"
    elif key == next(generator):
        return "F2"
    elif key == next(generator):
        return "F3"
    elif key == next(generator):
        return "F4"
    elif key == next(generator):
        return "F5"
    elif key == next(generator):
        return "F6"
    elif key == next(generator):
        return "F7"
    elif key == next(generator):
        return "F8"
    elif key == next(generator):
        return "F9"
    elif key == next(generator):
        return "F10"
    elif key == next(generator):
        return "F11"
    elif key == next(generator):
        return "F12"
    elif key == next(generator):
        return "Tab"
    elif key == next(generator):
        return "Caps Lock"
    elif key == next(generator):
        return "Left Shift"
    elif key == next(generator):
        return "Left Ctrl"
    elif key == next(generator):
        return "Alt"
    elif key == next(generator):
        return "Alt"
    elif key == next(generator):
        return "Space"
    elif key == next(generator):
        return "Left Arrow"
    elif key == next(generator):
        return "Right Arrow"
    elif key == next(generator):
        return "Up Arrow"
    elif key == next(generator):
        return "Down Arrow"
    
    

def qtKeyToPygameKey(keylist):
    j=0
    for i in keylist:
        if i in range(65, 91):
            keylist[j]=i+32
        elif i in weirdkeys:
            generator = weirdKeyGenerator()
            if i == next(generator):
                keylist[j]=282
            elif i == next(generator):
                keylist[j]=283
            elif i == next(generator):
                keylist[j]=284
            elif i == next(generator):
                keylist[j]=285
            elif i == next(generator):
                keylist[j]=286
            elif i == next(generator):
                keylist[j]=287
            elif i == next(generator):
                keylist[j]=288
            elif i == next(generator):
                keylist[j]=289
            elif i == next(generator):
                keylist[j]=290
            elif i == next(generator):
                keylist[j]=291
            elif i == next(generator):
                keylist[j]=292
            elif i == next(generator):
                keylist[j]=293
            elif i == next(generator):
                keylist[j]= 9
            elif i == next(generator):
                keylist[j]= 301
            elif i == next(generator):
                keylist[j]= 304
            elif i == next(generator):
                keylist[j]= 306
            elif i == next(generator):
                keylist[j]= 308
            elif i == next(generator):
                keylist[j]= 307
            elif i == next(generator):
                keylist[j]= 32
            elif i == next(generator):
                keylist[j]= 276
            elif i == next(generator):
                keylist[j]= 275
            elif i == next(generator):
                keylist[j]= 273
            elif i == next(generator):
                keylist[j]= 274
        j+=1
    return keylist

    32,276,275,273,274