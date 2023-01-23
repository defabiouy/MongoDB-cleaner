# MongoDB-cleaner
Script para limpiar los documentos de una base mongodb, anteriores a la fecha calculada a partir de los N días anteriores a la ejecución del script.

# Variables de entorno

Para que el script funcione se debe asignar las siguientes variables de entorno:

```
URL_SLACK_ERROR: es el canal de slack donde se reportarán los errores.
MONGO_SERVER: es la ubicación del mongo al que se conectará (ej: localhost:27017)
MONGO_DB: es la db de Mongo donde se realizaran las acciones (ej: iotagent).
MONGO_COLLECTION: es la colección donde se realizaran las acciones (ej: devices).
```


# Run

Para correr se deberá ejecutar el script de la siguiente forma:

`python3 job-mongodb-cleaner.py`
