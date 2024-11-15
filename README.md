# Vehicle_Application_List

# Actividad Final Modulo 3 - Base de Datos


# ----  APLICACION DE REGISTRO DE LA COVERTURA DE UNA HERRAMIENTA DE PROGRAMACION DE LLAVES DE VEHICULO ------

## PROYECTO:

Este proyecto se basa en la creacion de una aplicacion que muestra la covertura de los vehiculos que soporta una herramienta de programacion de llaves
destinado a los comerciales de la empresa. 

La aplicacion se compone de 4 ventanas de dialogo: 

> Ventana principal (Main Windows): Muestra la barra de herramientas con 3 botones (añadir vehiculo, buscar datos de vehiculo y cerrar aplicacion). Tambien se muestra la tabla con
        los datos del vehiculo y cada vehiculo dispone de un boton de opciones para poder actualizar ("Edit") sus datos o poder eliminarlo ("Delete").

![Main windows](https://github.com/user-attachments/assets/c36260ff-dadf-41c8-8fdb-6fdf76ed52dd)


> Ventana añadir vehiculo (New Vehicle): Muestra el cuadro de dialogo con los datos del vehiculo que se requieren introducir. Disponde de dos botone tanto para guardar el vehiculo como
        para cancelar el registro.

![New Vehicle Dialog](https://github.com/user-attachments/assets/4e041ecb-f3e4-401a-adf5-1ed8bd90b4e4)


> Ventana busqueda (Search): Muestra el cuadro de dialogo para realizar distintas busquedas, se compone en la parte superior de 4 botones en el que cada boton realiza una
consulta QSL:

        · Boton "All vehicles" que realiza la consulta de todos los vehiculos registrados en la base de datos
        · Boton "Vehicles programming" que realiza la consulta de todos los vehiculos que se pueden programar
        · Boton "Vehicles cloning" que realiza la consulta de todos los vehiculos que se pueden clonar
        · Boton "Vehicles not coverage" que realiza la consulta de los vehiculos que no se pueden ni programar ni clonar

        Tambien dispone de un buscador de datos de un vehiculo especifico (Search vehicle name) en el que se puede introducir el nombre del vehiculo o seleccionar
        directamente del listado que se muestra. Cuando se selecciona el vehiculo en la parte izquierda aparece el panel de resultados con los datos de dicho
        vehiculo. Analogamente si pulsamos el boton "See more details" se muestra dicho vehiculo en la tabla de la ventana principal.

![Search Vehicle Dialog](https://github.com/user-attachments/assets/6dc2bdcc-0596-49df-8419-8faab769fea5)


> Ventana de actualizacion (Update Vehicle): Muestra el cuadro de dialogo para actualizar los datos y aparece cuando se selecciona en el vehiculo la opcion de "Edit"

![Update Vehicle Dialog](https://github.com/user-attachments/assets/0424f271-b1fc-46f0-8310-7025db4c878e)
