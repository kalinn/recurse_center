# calculator.py
import re

def calculator():
    while(True):
        calc = raw_input('> ')
        if len(re.split('[^0-9]+', calc)) == 1:
            print eval(calc)
        else:
            sp = re.split('\s', calc)
            while(len(sp)>1):
                sp[2] = str(eval(sp[0] + sp[1] + sp[2]))
                sp = sp[2:]







