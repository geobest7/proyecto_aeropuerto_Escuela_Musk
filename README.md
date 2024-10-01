Proyecto Aeroporto
Estructura del Proyecto


proyecto/
│
├── entities/
│   ├── __init__.py
│   ├── aeropuerto.py
│   ├── lector.py
│   └── slot.py
│
├── data/
│   ├── vuelos1.txt
│   ├── vuelos2.csv
│   └── vuelos3.json
│
├── tests/
│   ├── __init__.py
│   ├── test_aeropuerto.py
│   ├── test_lector.py
│   └── test_slot.py
│
├── main.py
└── __init__.py
Descripción de Directorios
entities/: Contiene los módulos que definen las entidades principales del proyecto: Aeropuerto, Lector y Slot, cada uno en su respectivo archivo.

data/: Almacena los datos de entrada del proyecto en diferentes formatos (TXT, CSV, JSON).

tests/: Incluye los archivos de pruebas unitarias para cada una de las clases en la carpeta entities. Estas pruebas se ejecutarán automáticamente.

main.py: Punto de entrada de la aplicación donde se inicia la lógica principal del proyecto.

requirements.txt: Lista las bibliotecas necesarias para el proyecto, que incluyen:

numpy
pandas
python-dateutil
pytz
six
Funcionalidad
El programa está diseñado para gestionar vuelos en un aeropuerto, calculando la fecha y hora de despegue de cada vuelo y asociando slots para el repostaje y embarque de pasajeros. Se controlan los slots disponibles y el tiempo restante para su liberación. Los datos se leen de tres archivos diferentes (TXT, CSV, JSON).

Clases Principales
Clase Aeropuerto
Constructor: Inicializa el aeropuerto con un DataFrame de vuelos, número de slots disponibles y tiempos de embarque.
Métodos:
calcula_fecha_despegue(): Calcula la fecha de despegue de un vuelo.
encuentra_slot(): Busca un slot disponible para un vuelo.
asigna_slot(): Asigna un slot a un vuelo.
asigna_slots(): Asigna slots a todos los vuelos del DataFrame.
Clase Lector
Constructor: Inicializa la clase con una ruta de archivo.
Métodos:
_comprueba_extension(): Verifica que la extensión del archivo sea correcta.
lee_archivo(): Lee el archivo.
convierte_dict_a_csv(): Convierte un diccionario a CSV.
Clases LectorCSV, LectorJSON, LectorTXT (heredadas de Lector)
Constructor: Constructor específico para cada tipo de archivo.
Métodos: Implementación específica de lectura para cada tipo de archivo.
Clase Slot
Constructor: Inicializa un slot con un identificador y fechas inicial y final.
Métodos:
asigna_vuelo(): Asigna un vuelo al slot.
slot_esta_libre_fecha_determinada(): Verifica si el slot está libre en una fecha específica.
Recomendaciones para Desarrollo
Se sugiere comenzar el desarrollo de las clases en el siguiente orden:

Clase Slot: Definir cómo representar los slots de tiempo.
Clase Lector y sus subclases: Implementar la lectura de archivos.
Clase Aeropuerto: Integrar la funcionalidad de asignación de vuelos.
