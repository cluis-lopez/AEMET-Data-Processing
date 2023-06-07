import glob
import json
import locale
import os
import sys
from datetime import date


locale.setlocale(locale.LC_NUMERIC, "es_ES.UTF-8")

def lowercase(s):
    if (len(s) <2):
        return s
    else:
        return s[0].upper()+s[1:].lower()

def processYear(data):
    yearData = {}
    monthData = {}
    errors = 0
    daysWithData = 0

    tMax = -100.0
    tMin = 100.0
    tMed = tMaxMed = tMinMed = totalPrec = 0.0
    rainyDays = counttmax = counttmin = counttmed = 0
    rainiestDay ={"day": date(1,1,1), "prec": 0.0}

    daysInMonth = 0

    currentYear = date.fromisoformat(data[0]["fecha"]).year
    currentMonth = date.fromisoformat(data[0]["fecha"]).month
    print("\tProcesando el mes ", end=" ")

    for index, idx in enumerate(data):
        d = date.fromisoformat(idx["fecha"])
        if (d.month > currentMonth or len(data) == index+1):
            print(currentMonth, end=".")
            if (counttmed > 0):
                tMed = tMed / counttmed
            else:
                tMed = 0
            if (counttmax >0):
                tMaxMed = tMaxMed / counttmax
            else:
                tMaxMed = 0
            if (counttmin>0):
                tMinMed = tMinMed / counttmin
            else:
                tMinMed = 0
            rainiestDay["day"] = str(rainiestDay["day"])
            monthData = {"DataDays": daysInMonth, "tMax": round(tMax,2), "tMaxMed": round(tMaxMed,2), "tMin": round(tMin,2), "tMinMed": round(tMinMed,2), "tMed": round(tMed,2), "totalPrec": round(totalPrec,2), "rainyDays": rainyDays, "rainiestDay": rainiestDay}
            yearData[currentMonth] = monthData

            currentMonth += 1
            daysInMonth = 0
            if ("tmax" in idx):
                tMax = float(locale.atof(idx["tmax"]))
            else:
                tMax = -100.0
            if ("tmin" in idx):
                tMin = float(locale.atof(idx["tmin"]))
            else:
                tMin = 100.0
            tMed = tMaxMed = tMinMed = totalPrec = 0.0
            rainyDays = counttmax = counttmin = counttmed = 0
            rainiestDay ={"day": date(1,1,1), "prec": 0.0}
            monthData = {}

        daysInMonth += 1
        daysWithData += 1

        if ("tmax" in idx):
            counttmax +=1
            t = float(locale.atof(idx["tmax"]))
            tMaxMed = tMaxMed + t
            if (t > tMax):
                tMax = t
        else:
            errors += 1

        if ("tmin" in idx):
            counttmin += 1
            t = float(locale.atof(idx["tmin"]))
            tMinMed = tMinMed + t
            if (t < tMin):
                tMin = t
        else:
            errors += 1

        if ("tmed" in idx):
            counttmed += 1
            tMed = tMed + float(locale.atof(idx["tmed"]))
        else:
            errors += 1

        if("prec" in idx):
            try:
                t = float(locale.atof(idx["prec"]))
            except ValueError:
                t = 0
                errors += 1
            if (t > 0):
                rainyDays+= 1
                totalPrec = totalPrec + t
                if (t > rainiestDay["prec"]):
                    rainiestDay["day"] = date.fromisoformat(idx["fecha"])
                    rainiestDay["prec"] = t
        else:
            errors += 1

    print ("Finalizado {0} . Procesados {1} dias con {2} errores".format(currentYear, daysWithData, errors))
    return reviewData(currentYear, yearData)

def reviewData(year, data):
    print("Revisando datos del año ", year)
    diasMes = [31,28,31,30,31,30,31,31,30,31,30,31]
    totalDays = 0
    if (len(data)<12):
        print ("\tWarning !! año con menos de 12 meses en datos")
    t = list(data)
    for i,k in enumerate(t):
        totalDays += data[k]["DataDays"]
        if (data[k]["DataDays"] < diasMes[i] * 0.7):
            print("\tWarning: el mes {0} tiene únicamente datos de {1} días de {2} posibles".format(k,data[k]["DataDays"], diasMes[i]))
        if (data[k]["tMax"] == -100): # Si tMax o tMin son inavalidas, las medias lo son tambien
            print ("\tWarning mes {0}. Temp Maxima invalida".format(k))
            if (i>0 and i<len(data)-1): # mes entre el segundo y el penúltimo
                data[k]["tMax"] = (data[t[i-1]]["tMax"] + data[t[i+1]]["tMax"])/2
                data[k]["tMaxMed"] = data[k]["tMax"]
                print ("\tInterpolado el valor de tMax y tMaxMed al valor ", data[k]["tMax"])
            if (i == len(data)-1):
                data[k]["tMax"] = data[t[i-1]]["tMax"]
                data[k]["tMaxMed"] = data[k]["tMax"]
                print ("\t Usando para tMax el valor del mes anterior ", data[k]["tMax"])
            if (i == 0):
                data[k]["tMax"] = data[t[i+1]]["tMax"]
                data[k]["tMaxMed"] = data[k]["tMax"]
                print ("\t Usando para tMax el valor del mes siguiente ", data[k]["tMax"])
        if (data[k]["tMin"] == 100):
            print ("\tWarning mes {0}. Temp Minima invalida".format(k))
            if (i>0 and i<len(data)-1): # mes entre el segundo y el penúltimo
                data[k]["tMin"] = (data[t[i-1]]["tMin"] + data[t[i+1]]["tMin"])/2
                data[k]["tMinMed"] = data[k]["tMin"]
                print ("\tInterpolado el valor de tMin al valor ", data[k]["tMin"])
            if (i == len(data)-1):
                data[k]["tMin"] = data[t[i-1]]["tMin"]
                data[k]["tMinMed"] = data[k]["tMin"]
                print ("\t Usando para tMin el valor del mes anterior ", data[k]["tMin"])
            if (i == 0):
                data[k]["tMin"] = data[t[i+1]]["tMin"]
                data[k]["tMinMed"] = data[k]["tMin"]
                print ("\t Usando para tMin el valor del mes siguiente ", data[k]["tMin"])
        if (data[k]["tMed"] == 0):
            print ("\tWarning mes {0} tMed invalida".format(k))
            if (i>0 and i<len(data)-1): # mes entre el segundo y el penúltimo
                data[k]["tMed"] = (data[t[i-1]]["tMed"] + data[t[i+1]]["tMed"])/2
                print ("\tInterpolado el valor de tMed al valor ", data[k]["tMed"])
            if (i == len(data)-1):
                data[k]["tMed"] = data[t[i-1]]["tMed"]
                print ("\t Usando para tMax el valor del mes anterior ", data[k]["tMed"])
            if (i == 0):
                data[k]["tMed"] = data[t[i+1]]["tMed"]
                print ("\t Usando para tMax el valor del mes siguiente ", data[k]["tMed"])

    return data

def bulkProc(path):
    files = glob.glob(os.path.join(path, '*.json'))
    if (len(files) == 0):
        print ("No files to process")
        exit()

    files.sort()

    mainData = {}
    metaData = {}

    for file in files:
        with open(file, "r") as f:
            data = json.load(f)
        fecha = data[0]["fecha"]
        initDate = date.fromisoformat(fecha)
        print("Procesando año: ", initDate.year)
        mainData[initDate.year] = processYear(data)

    json2js = "data = " + json.dumps(mainData, indent=4)

    with open("data.js", "w") as f:
        f.write(json2js)
    with open("data.js", "a") as f:
        f.write(";")        

# Process Metadata
    with open(files[0], "r") as f: # First file
        data = json.load(f)

    fecha = data[0]["fecha"]
    initDate = date.fromisoformat(fecha)
    metaData["firstDate"] = fecha
    metaData["firstYear"] = str(initDate.year)
    metaData["nombre"] = lowercase(data[0]["nombre"])
    metaData["provincia"] = lowercase(data[0]["provincia"])
    metaData["altitud"] = data[0]["altitud"]
    metaData["indicativo"] = data[0]["indicativo"]

    with open(files[len(files)-1], "r") as f: # Last file
        data = json.load(f)

    fecha = data[len(data)-1]["fecha"]
    lastDate = date.fromisoformat(fecha)
    metaData["lastDate"] = fecha
    metaData["lastYear"] = str(lastDate.year)

    json2js = "metadata = " + json.dumps(metaData, indent=4)

    with open("metadata.js", "w") as f:
        f.write(json2js)
    with open("metadata.js", "a") as f:
        f.write(";")  

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage bulproc <path to data directory>")
        exit()
    bulkProc(sys.argv[1])
