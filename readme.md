# bermoto


## repositorio

- la documentación se encuentra el la carpeta **docs**
- el código de servidor se encuentra en la carpeta **backend**
- el codigo de la app se encuentra en la carpeta **frontend**


## metodologia

en cada carpeta de codigo se encuentran los archivos **test.py** que tienen los
tests de cada funcionalidad, cada contrubuyente o grupo de los mismos debe mandar
un pull request cada vez que:

- haga que un test funcione
- haga alguna correccion a un test
- haga alguna correccion a una funcion que ya funcione
- que corrija o amplie la documentación


en caso de encontrar un error, reportarlo al issue tracker y citar el issue
tracker en el pull request cuando este sea por una correccion

pull requests con archivos basura o con archivos de configuración seran rechazados


## entorno de desarrollo

se sugiere usar entornos virtuales, para poner a punto el entorno virtual,
se recomienda para backend usar python3 y para frontend python2, una vez instalado
el paquete **virtualenv** se procede a crear el entorno virtual de la siguiente
manera:


```virtualenv -p /usr/bin/python3 tor  # para linux
source tor/bin/activate  # para activar el entorno virtual
```

luego de eso, usar ```pip install -r code_path_folder/requirements.txt``` para
instalar todos las librerias que estan en el archivo **requirements.txt**

## reglas de estilo

uso de pep8:

- separacion de guiones bajos en lo posible para variables y funciones
- camelcase en lo posible para clases
- 4 espacios, no tabs


## funcionalidades

servidor:

especificas:
- login-logout
- crearse perfil
- mandar pedido
- aceptar pedido
- cancelar pedido
- pedido terminado exitoso


interfaz:

- login-logout
- mostrar gps con dos marcadores
- hacer pedido
- aceptar pedido
- cancelar pedido
- finalizar pedido
