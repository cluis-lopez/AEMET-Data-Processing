# For degugging purposes
import json
import sys
from datetime import date
import locale

locale.setlocale(locale.LC_NUMERIC, "es_ES.UTF-8")

def processData(data, month, token):
    ret = []
    dias = 0
    valmin = 100
    valmax = -100
    valmed = 0
    for x in data:
        d = date.fromisoformat(x["fecha"])
        if (d.month == int(month)):
            dias += 1
            element = {}
            if (token in x):
                try:
                    el = float(locale.atof(x[token]))
                    element[token] = round(el, 2)
                    if el > valmax:
                        valmax = el
                    if el < valmin:
                        valmin = el
                    valmed += el
                except:
                    print("Fail to read float value from ", x[token], file= sys.stderr)
            else:
                print ("Elemento " + token + " no existe en " + str(x), file = sys.stderr)
            if (len(element) > 0):
                ret.append(element)
    
    print ("Procesados ", dias, " dias", file = sys.stderr)
    print ("Maximo valor: ", valmax, "\tMínimo valor: ", valmin, "Acumulado: ", valmed, "\tPromedio: ", valmed/dias)
    return ret

def Main():
    if (len(sys.argv) < 4):
        print ("Usage: extract.py <filename> <mes> <token>")
        exit()
    FILE = sys.argv[1]
    month = sys.argv[2]
    token = sys.argv[3]

    with open(FILE, "r") as f:
        datafile = json.load(f);

    print (json.dumps(processData(datafile, month, token)))


if (__name__ == '__main__'):
    Main()