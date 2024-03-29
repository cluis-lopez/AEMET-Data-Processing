## Utilidad para extraer series de datos desde AEMET y formatearlos en HTML

AEMET proporciona, utilizando su plataforma opendata, datos históricos climatológicos de algunas de sus estaciones. Este conjunto de utilidades, permite la descarga automatizada de series de históricos, su procesado, filtrado y  modelado en un fichero HTML para la visualización de los datos en un navegador.

### Requerimientos:

**Python3**: instalado por defecto en cualquier distro Linux y que en Windows se descarga directamente desde la tienda Microsoft

### Instrucciones Previas:
- Es necesario solicitar una API Key a AEMET a través de la página [AEMET OpenData Alta Usuario](https://opendata.aemet.es/centrodedescargas/altaUsuario?) Únicamente requiere de una dirección de correo electrónico válida
- Se necesita el código identificador de la estación meteorológica de la que se quieran extraer los datos históricos. Una forma simple es utilizar el servicio de predicción del tempo por Municipios [AEMET Prediccion Municipios](https://www.aemet.es/es/eltiempo/prediccion/municipios) y una vez seleccionado el municipio, en el fondo de la página seleccionar alguna de las estaciones próximas.Al seleccionar la estación aparecen los datos de posición y altura de la misma junto con un indicador etiquetado como **"Ind. climatológico"** formado por un grupo de cifras y , en ocasiones, una o dos letras.

### Instrucciones:

- Descargar los ficheros de este repo o clonarlo directamente empleando `git clone`
- Descarga de series de datos: emplear la utilidad download.py, ejemplo:

    `python download.py -f año_inicial -l año_final -p prefijo_ficheros -s indicador_estacion_AEMET -k API_Key_AEMET`

Este comando nos generará una serie de ficheros nombrados "prefijo_ficheros_año.json" con los datos diarios regocidos por la estación en cada año solicitado:

- Advertencias:
    -  Es posible que sobrepasemos el límite de datos que nos permite descargar AEMET en un cierto periodo. En ese caso tendremos que realizar varias descargas empleando un rango de años menor
    - Es posible que la estación solicitada no guarde datos históricos: no todas las estaciones de AEMET (o su servicio OpenData) permiten la descarga de históricos. En ese caso probar con estaciones cercanas.
    - Algunas estaciones (ej. Madrid Retiro) permiten la descarga de series de datos muy antiguas (ej. 1930 o incluso anteiores) mientras que otras solo mantienen datos más recientes (ej. Llanes desde 1998). En cualquier caso, se trata de probar

- Tratamiento de los datos:
    - Los ficheros generados por la utilidad anterior de descarga, deben moverse a un directorio o carpeta específico para los mismos.
    - Ejecutar la utilidad `bulkproc`empleando como parámetro el directorio donde se han ubicado los ficheros con la información anual descargada. Ejemplo

        `python bulkproc /Llanes`

    - La utilidad de procesado generará un par de ficheros (data.js y metadata.js) en el directorio actual que serán cargados por el navegador al cargar la página web asi pues la utilidad debe de ejecutarse en el mismo directorio en el que se encuentren los ficheros index.html y style.css. EN caso contrario habrñá que mover manualmente estos ficheros aldirectorio correspondiente
    - Abrir el fichero index.html con el navegador
 
### Ejemplo Práctico
Asumiendo que estamos en una máquina con Windows. Desde una linea de comandos (CMD) ejecutamos:

`git clone  https://github.com/cluis-lopez/AEMET-Data-Processing.git`

Si no tenemos git instalado en nuestro PC, nos creamos una carpeta y copiamos todos los ficheros de este repositorio a la misma y nos cambiamos a ella:

```
mkdir AEMET-Data_Processing
cd AEMET-Data-Processing
```

A traves de la plataforma AEMET Opendata habremos solicitado y obtenido una API Key que nos habrá llegado por correo electrónico y será un chorro de carácteres del estilo de:

`eyJhbGciOiJIUzI1MiJ9.eyJwdWIiOiJjbHfpcy5sb3BlekBnbWFpb55jb20iLCJqdGkiOiJkN2Q1MzcyMy03ZGE5LTQyODgtOTg4ZC03NmVhOTFhODdmNjAiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcwNDg4NjE0NCwidXNlcklkIjoiZDdkNTM3HjMtN2RhOS00Mjg4LTk4OGQtNzZlYTkxYTg3ZjYwIcwicm9sZSI6IiJ9.bOQXPPT9AHfjsVVwpEN1-3owbOfJYsPvtvfM2DzE8l4`

Buscamos el identificador de la estación AEMET de la que queramos extraer el registro histórico ej: Valladolid. Para ello, buscamos dentro de la página de Municipios de [AEMET](https://www.aemet.es/es/eltiempo/prediccion/municipios) "Valladolid":

![Municipios AEMET](AEMET_1.PNG)

Hacemos click en la estación más cercana y obtenemos los datos de la misma:

![Estacion AEMET](AEMET_2.PNG)

Registramos el Id de la estación, en este caso: **2422**

Descargamos la serie de datos anuales utilizando el siguiente comando y sustituyendo obviamente la clave correspondiente, asi como los años inicial y final que queramos recuperar

`python download.py -f 2000 -l 2023 -p Valladolid -s 2422 -k eyJhbGciOiJIUzI1NiJ9.eyJzdsdIiOiJjbHVpcy5sb3BlekBnbWFpbC5jb20iLCJqdGkiOiJkMjI2M2U1My0xYTE0LTQ0ZTctYTEyZi03MGQxODIwOWQ4NTkiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcxMDg0NjIzNlfdsecklkIjoiZDIyNjNlNTMtMWExNC00NGU3LWEewr8632kMTgyMDlkODU5IiwiSI6IiJ9.i6ElSb3wIMgOxRHdDJffgdaVDyYVdLcFdIxCwzw5Ybo`

Esto generará en la carpeta local 24 ficheros (uno por cada año) son nombres `Valladolid_2000.json`, `Valladolid_2001.json`... etc 
Crear una carpeta nueva y mover todos los ficheros `*.json` descargados a la misma. Ejemplo:
```
mkdir Valladolid
mv *.json Valladolid/
```
Ejecutar el programa de procesado de datos sobre el contenido de la carpeta ejecutando:

`python bulkproc.py Valladolid/` 

Abrir directamente el fichero `index.html` con el navegador
