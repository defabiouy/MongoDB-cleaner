#!/usr/bin/python3

'''
Script para limpiar documentos de una bd mongo anteriores a la fecha calculada a partir de los N días anteriores a la ejecución del script.

URL_SLACK_ERROR: es el canal de slack donde reporto los errores.
MONGO_SERVER: es la ubicación del mongo al que me voy a conectar (ej: localhost:27017)
MONGO_SERVER: es la db de Mongo donde voy a hacer cosas (ej: iotagent).
MONGO_COLLECTION: es la colección donde voy a hacer cosas (ej: devices).
'''

__author__      = "Fabio Suarez"

from datetime import datetime, date, time, timedelta
import requests, json, os, logging
from pymongo import MongoClient



try:

    if os.getenv("URL_SLACK_ERROR") is not None:
        url_slack_error = os.environ["URL_SLACK_ERROR"]
    else: #si no se seteo la variable, por omision reporto los errores al canal de alertas
        url_slack_error = 'https://hooks.slack.com/services/<<resto url>>'

    headers_slack = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache"
    }

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/tmp/' + os.path.basename(__file__),
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)


    logging.info('Inicia la ejecucion del script ' + os.path.basename(__file__) + ' a las ' + str(datetime.now()))

    #=================================== seteo variables ===================================
    if os.getenv("MONGO_SERVER") is not None:
        mongo_server = os.environ['MONGO_SERVER']
    else: #si no se seteo la variable, por omision voy a la bd local
        mongo_server = 'localhost:27017'

    if os.getenv("MONGO_DB") is not None:
        mongo_db = os.environ['MONGO_DB']
    else: #si no se seteo la variable, por omision voy a "default"
        mongo_db = 'iotagent'

    if os.getenv("MONGO_COLLECTION") is not None:
        mongo_collection = os.environ['MONGO_COLLECTION']
    else: #si no se seteo la variable, por omision voy a la collection "devices"
        mongo_collection = 'sth_/devices'

    if os.getenv("CANTIDAD_DIAS") is not None:
        cant_dias = eval(os.environ['CANTIDAD_DIAS'])
    else: #si no se seteo la variable, por omision borro los documentos anteriores a 1 año
        cant_dias = 365

    #===================== conexión a la BD e inicialización variables ======================
    today = datetime.today()
    client = MongoClient('mongodb://' + mongo_server)[mongo_db][mongo_collection]
    aborrar = client.find({'recvTime': { '$lt': today - timedelta(cant_dias)} }).count()

    #==================================== logueo inicial ====================================
    logging.info('Connectado a MongoDB:' + client.__str__())
    print("\tDocumentos a eliminar:", aborrar, "con fecha:", today - timedelta(cant_dias) )
    logging.info("\tDocumentos a eliminar: " + str(aborrar) + " con fecha: " + str(today - timedelta(cant_dias)) )
    #======================================== logueo ========================================

    #===================================== borrado ==========================================
    result = client.delete_many({'recvTime': { '$lt': today - timedelta(cant_dias)} })

    #===================================== logueo final =====================================
    print("\tDocumentos eliminados :",result.deleted_count)
    logging.info("\tDocumentos eliminados: " + str(result.deleted_count))
    logging.info('Finaliza la ejecucion del script ' + os.path.basename(__file__) + ' a las ' + str(datetime.now()))
    #======================================== logueo ========================================

except Exception as e:
    print("Error:", e, e.__doc__)
    logging.info('Error en el script ' + os.path.basename(__file__) + ' a las ' + str(datetime.now()) + " -> " + e.__doc__)
    message = u'Proceso de limpieza sth - Ocurrio un error: ' + str(e) + " -> " + e.__doc__
    payload_slack = {'attachments': [{'color': 'danger', 'text': message}]}
    #r = requests.request('POST', url_slack_error, data=json.dumps(payload_slack), headers=headers_slack)
finally:
    try:
        pass
    except Exception:
        pass