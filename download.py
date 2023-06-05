import requests
import json
import sys
import getopt
from urllib.parse import urlparse

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def getPointer(year, estacion, apikey):
    url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/'
    url = url + 'fechaini/' + str(year) + '-01-01T00%3A00%3A00UTC/'
    url = url + 'fechafin/' + str(year) + '-12-31T00%3A00%3A00UTC/'
    url = url + 'estacion/' + estacion
    
    querystring = {"api_key": apikey}
    headers = {'cache-control': "no-cache"}
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    resp1 = response.json()
    
    if (resp1["descripcion"] == "exito" and resp1["estado"] == 200):
        return (True, resp1["datos"])
    else:
        return (False, resp1["descripcion"])
    
def getData(pointer):
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", pointer, headers=headers)
    if (response.status_code == 200):
        return response.json()
    else:
        return "Fail"
    
def saveFile(preffix, year, data):
    filename = preffix + "_" + str(year) + ".json"
    with open(filename, "w") as write_file:
        json.dump(data, write_file)
        return filename
    
def processYear(year, estacion, apikey, preffix):
    dataUrl = getPointer(year, estacion, apikey)
    if (not dataUrl[0]):
        return dataUrl[1] # Error code coming from AEMET
    elif (is_url(dataUrl[1])):
        data =getData(dataUrl[1])
        if (data != "Fail"):
            filename = saveFile(preffix, year, data)
            return "Salvados datos año " + str(year)+ " en " + filename
        else:
            return ("Error recibiendo datos para " + str(year))
    else:
        return ("Recibida URL incorrecta para " + str(year))

def usage():
    print ("""
    Usage: python download [OPTIONS]

    Opciones obligatorias:

    -f <primer año a descargar>
    -l <ultimo año a descargar>
    -p <prefijo que se asignara a cada fichero>
    -s <indicador de estacion meteorologica>
    -k <clave AEMET opendata apikey>

    Ejemplo:

    python download.py -f 2000 -l 2022 -p Madrid -s 3195 -k yJhbGciOiJIUzI1NiJ9....

    Descargará los datos climatologicos de la estación de Madrid Retiro (codigo 3195)
    entre los años 2000 y 2022 salvándolos en ficheros con el nombre Madrid_2000.json, 
    Madrid_2001.json, etc,,,
    """)
    exit()

def Main():
    apikey = preffix = estacion = fy = ly = ""
    
    try:
        opts, args = getopt.getopt (sys.argv[1:], "f:l:p:s:k:")
    except getopt.GetoptError as err:
        print(err)
        usage()

    for o, a in opts:
        if (o == "-f"):
            fy = a
        elif (o == "-l"):
            ly = a
        elif (o == "-p"):
            preffix = a
        elif (o == "-s"):
            estacion = a
        elif (o == "-k"):
            apikey = a

    if (apikey == "" or estacion == "" or preffix == ""):
        usage()

    try:
        first_year = int(fy)
        last_year = int(ly)
    except Exception as e:
        print ("Error: ", end = ' ')
        print(e)
        usage()
    else:
        if (first_year >= last_year):
            print("Last year must be larger than first year")
            usage()


    for year in range(first_year, last_year):
        print("Processing: " + str(year), end = ' ')
        print(processYear(year, estacion, apikey, preffix))

if __name__ == '__main__':
	Main()