<p align="center">
  <img width="275" height="150" src="https://i.imgur.com/Ta3Fx7Q.png ">
</p>

# PyCNE 0.1
**PyCNE** es una librería de Python que permite consultar fácilmente información del Registro Electoral de Venezuela, extrayendo datos de la web oficial del CNE.

## Instalación

 Puedes instalar PyCNE utilizando el instalador de paquetes [pip](https://pip.pypa.io/en/stable/).
```bash
pip install PyCNE
```

## Uso
Una aplicación sencilla de PyCNE se vería así:
```python
import PyCNE

consulta = PyCNE.consulta('V',12345678)

print(consulta.info)
```
**¿Qué acabamos de hacer?**

 1. Importamos la librería a nuestro script.
 2. Creamos una instancia de la **clase consulta** *(ver más abajo)*.
 3. Imprimimos en pantalla la variable `consulta.info` para mostrar los datos obtenidos.

A continuación encontrarás más información al respecto:

### La clase consulta
Es la clase principal del módulo PyCNE, al inicializar realiza una consulta —tal como su nombre indica— a la web con los datos proporcionados. Por tanto, para poder extraer cualquier información, necesitaremos **crear una instancia** de esta clase.

**Sintaxis:**
```python
consulta = PyCNE.consulta(nacionalidad, cedula[,opciones])
```
**Parámetros:**
| Nombre | Tipo | Descripción | Valor por defecto |
|:---:|:---:|:---:|:---:|
| ***nacionalidad*** | str | El prefijo correspondiente a la cédula  a consultar. Acepta los valores **V** (venezolano) y **E** (extranjero).  | No tiene un valor por defecto. Es obligatorio especificarlo.
| ***cedula*** | int | El número de cédula a consultar.| No tiene un valor por defecto. Es obligatorio especificarlo.
| ***altmode*** | bool | Modo alternativo *(ver más abajo)*. |Por defecto es `False`
| ***base_url*** | str | La URL base a la cual se realizará la consulta|`http://www.cne.gob.ve/...`

### Modos de consulta
Existen dos formas de extraer los datos: 

 - El **modo normal** —la manera más sencilla, rápida y precisa— funciona a través de la librería *BeautifulSoup*. Se obtienen los datos realizando una búsqueda a partir de las etiquetas HTML y se añaden a las variables correspondientes.
 - El **modo alternativo**, que no depende de la librería *BeautifulSoup*, extrae el contenido de la consulta y elimina (mediante expresiones regulares) la información no deseada, para posteriormente separar los datos y añadirlos a sus respectivas variables. 
Generalmente, este modo es más lento y engorroso. Por tanto, no es recomendable usarlo a no ser que exista algún problema que impida utilizar el modo normal.

### ¿Cómo acceder a la información? (Variables)
Una vez se crea la instancia, los datos de la consulta son almacenados en distintas variables. Para acceder a ellas debemos llamarlas utilizando la misma instancia que creamos previamente.

| Variable | Tipo | Contenido | Ejemplo
|:---:|:---:|:---:|:---:|
| ***cedula*** | str | Cédula de la consulta realizada.  | `V-12345678`|
| ***nombre*** | str | Nombre correspondiente a la cédula.|`MARCOS EVANGELISTA PÉREZ JIMÉNEZ`|
| ***estado*** | str | Estado del centro. |`DTTO. CAPITAL`|
| ***municipio*** | str | Municipio del centro.|`MP. BLVNO LIBERTADOR`|
| ***parroquia*** | str | Parroquia del centro.|`PQ. SUCRE`|
| ***centro*** | str | Centro de votación.|`COLEGIO DE CARACAS`|
| ***dirección*** | str | Dirección del centro.|`SECTOR XXX AVENIDA XXX CALLE XXX`|

Adicionalmente, toda la información de la consulta es recogida dentro de un diccionario de Python, de manera que se pueda acceder a ella con mayor facilidad:
| Variable | Tipo | Descripción |
|:---:|:---:|:---:|
| ***info*** | dict* | Diccionario que contiene todas las variables anteriores.*|
| ***info_json*** | json string | Similar a la variable **info**, pero en formato JSON.|  
###### * de usarse la *clase multi*, la variable `info` pasaría de ser un diccionario a ser una *lista de diccionarios*.

**Ejemplos:**
```python
import PyCNE

consulta = PyCNE.consulta('V',12345678)

print(consulta.cedula)
# Resultado: V-12345678

print(consulta.nombre)
# Resultado: MARCOS EVANGELISTA PÉREZ JIMÉNEZ

print(consulta.info)
# Resultado: {'cedula':'V-12345678',
#			  'nombre':'MARCOS EVANGELISTA PÉREZ JIMÉNEZ',
#			  'estado':'DTTO. CAPITAL',
#			  'municipio':'MP. BLVNO LIBERTADOR',
#			  'parroquia':'PQ. SUCRE',
#			  'centro':'COLEGIO DE CARACAS',
#			  'direccion':'SECTOR XXX AVENIDA XXX CALLE XXX'}
```

### La clase multi
A veces, es necesario realizar el proceso con más de una cédula. La **clase multi** es una clase hija de la *clase consulta*, que nos permitirá consultar múltiples cédulas sin la necesidad de crear infinitas instancias de la clase padre. 

Esta clase tomará las cédulas de una **lista** y asignará los resultados a la variable `info` anteriormente mencionada, esta vez como una **lista de diccionarios** *(ver ejemplo más abajo)*.

**Sintaxis:**
```python
consulta = PyCNE.consulta.multi(cedulas[,opciones])
```
**Parámetros:**
| Nombre | Tipo | Descripción | Valor por defecto |
|:---:|:---:|:---:|:---:|
| ***cedulas*** | list | Lista que contiene todas las cédulas a consultar, en el formato: `V-123456789` o `E-123456789`| No tiene un valor por defecto. Es obligatorio especificarlo.
| ***altmode*** | bool | Modo alternativo *(ver arriba)*. |Por defecto es `False`
| ***base_url*** | str | La URL base a la cual se realizará la consulta|`http://www.cne.gob.ve/...`

**Ejemplo:**
```python
import PyCNE

cedulas = ['V-12345678','V-87654321']

consulta = PyCNE.consulta.multi(cedulas)

print(consulta.info)
```
El resultado de esta función **print** sería:
```python
[{'cedula':'V-12345678',
'nombre':'MARCOS EVANGELISTA PÉREZ JIMÉNEZ',
'estado':'DTTO. CAPITAL',
'municipio':'MP. BLVNO LIBERTADOR',
'parroquia':'PQ. SUCRE',
'centro':'COLEGIO DE CARACAS',
'direccion':'SECTOR XXX AVENIDA XXX CALLE XXX'},

{'cedula':'V-87654321',
'nombre':'JOSÉ GREGORIO HERNÁNDEZ CISNEROS',
'estado':'TRUJILLO',
'municipio':'MP. ANDRÉS BELLO',
'parroquia':'PQ. LA ESPERANZA',
'centro':'COLEGIO DE TRUJILLO',
'direccion':'SECTOR XXX AVENIDA XXX CALLE XXX'}]
```
## Errores y excepciones

### Exception: La cédula no se encuentra inscrita en el CNE (Error 0)
Esta excepción ocurre cuando la cédula consultada es una expresión válida, pero no aparece en los registros del CNE, por lo que es imposible extraer cualquier información.

Habitualmente, detendría el flujo de ejecución; sin embargo, pueden ser ignoradas o tratadas mediante [try y except](https://docs.python.org/es/3/tutorial/errors.html).

**IMPORTANTE:** Cuando esta excepción ocurre en una instancia de la **clase multi**, no se detiene el programa. El flujo de ejecución continúa y las cédulas que no se encuentran registradas se almacenan en una **lista**, a la cual se puede acceder a través de las siguientes variables:
| Variable | Tipo | Descripción |
|:---:|:---:|:---:|
| ***errors*** | list | Lista que contiene todas las cédulas que no se encuentran registradas en el CNE.|
| ***errors_json*** | json string | Similar a la variable **errors**, pero en formato JSON.|  

**Ejemplo:**
```python
print(consulta.errors)
# Resultado: ['V-00000000','V-00000001']
```

### ConnectionError: No se ha podido establecer la conexión con el servidor (Error 1)
Este error ocurre cuando no se logra llevar a cabo la consulta debido a problemas con la conexión, o a que la URL es incorrecta. 
En este último caso, quizá sería conveniente colocar la URL apropiada mediante el parámetro `base_url` en ambas clases. De lo contrario, no es recomendable alterar dicho valor.

### Exception: Los parámetros de la consulta están vacíos (Error 2)
Esta excepción aparece cuando se lleva a cabo una consulta múltiple utilizando una lista vacía como parámetro.

## Contribuciones

Las contribuciones son bienvenidas. Si observas algún problema o bug, o deseas sugerir algún cambio, ¡siéntete libre de comentarlo en la sección correspondiente!

## Importante
 Toda la información que se puede extraer con esta librería es **pública**; sin embargo, no nos hacemos responsables por el uso que se le de a esta herramienta.
 
## Licencia

[MIT](https://choosealicense.com/licenses/mit/)