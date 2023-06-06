## Utilidad para extraer datos desde AEMET y formatearlos en HTML para su análisis

AEMET proporciona, utilizando su plataforma opendata, datos históricos climatológicos de algunas de sus estaciones. Este conjunto de utilidades, permite la descarga automatizada de series de históricos, su procesado, filtrado y  modelado en un fichero HTML para la visualización de los datos en un navegador.

- Requerimientos:
    - Python3: instalado por defecto en cualquier distro Linux y que en Windows se descarga directamente desde la tienda Microsoft

- Instrucciones Previas:
    - Es necesario solicitar una API Key a AEMET a través de la página [AEMET OpenData Alta Usuario](https://opendata.aemet.es/centrodedescargas/altaUsuario?) Únicamente requiere de una dirección de correo electrónico válida
    - Se necesita el código identificador de la estación meteorológica de la que se quieran extraer los datos históricos. Una forma simple es utilizar el servicio de predicción del tempo por Municipios [AEMET Prediccion Municipios](https://www.aemet.es/es/eltiempo/prediccion/municipios) y una vez seleccionado el municipio, en el fondo de la página seleccionar alguna de las estaciones próximas.Al seleccionar la estación aparecen los datos de posición y altura de la misma junto con un indicador etiquetado como **"Ind. climatológico"** formado por un grupo de cifras y , en ocasiones, una o dos letras.

- Instrucciones:

    - Descargar los ficheros de este repo o clonarlo directamente empleando `git --clone`
    - Descarga ficheros: emplear la utilidad download.py, ejemplo:

    `python download.py -f <año inicial> -l <año final> -p <prefijo ficheros> -s <indicador estacion AEMET> -k <API Key AEMET>`

    Este comando nos generará una serie de ficheros nombrados <prefijo ficheros>_<año>.json con los datos diarios regocidos por la estación en cada año solicitado:

       - **Advertencia**:
           -  Es posible que sobrepasemos el límite de datos que nos permite descargar AEMET en un coerto periodo. En ese caso tendremos que realizar varias descargas empleando un rango de años menor
           - Es posible que la estación solicitada no guarde datos históricos: no todas las estaciones de AEMET (o su servicio OpenData) permiten la descarga de históricos. En ese caso probar con estaciones cercanas.
           - Algunas estaciones (ej. Madrid Retiro) permiten la descarga de series de datos muy antiguas (ej. 1950 o anteiores) mientras que otras solo mantienen datos más recientes (ej. Llanes desde 1998). EN cualquier caso, se trata de probar