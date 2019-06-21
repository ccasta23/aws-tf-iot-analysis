from bson.json_util import dumps, ObjectId
from pymongo import MongoClient, DESCENDING
from werkzeug.local import LocalProxy
import json


# Este método se encarga de configurar la conexión con la base de datos
def get_db():
    print("Iniciando Lecura de la configuración")
    with open('configDB.json') as json_file:  
        args = json.load(json_file)
        db = args['DB_URI']
        client = MongoClient(db)
    return client.iot


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def test_connection():
    return dumps(db.collection_names())


def collection_stats(collection_nombre):
    return dumps(db.command('collstats', collection_nombre))


# -----------------InformaciónMabe-------------------------


def crear_datos(json):
    return str(db.datos.insert_one(json).inserted_id)

# -----------------Carreras-------------------------


def crear_carrera(json):
    return str(db.carreras.insert_one(json).inserted_id)


def consultar_carrera_por_id(carrera_id):
    return dumps(db.carreras.find_one({"_id": ObjectId(carrera_id)})) ##dumps => From bson to json


def actualizar_carrera(carrera):
    # Esta funcion solamente actualiza nombre y descripcion de la carrera
    return str(db.carreras.update_one({'_id': ObjectId(carrera['_id'])}, {'$set': {'nombre': carrera['nombre'], 'descripcion': carrera['descripcion']}}).modified_count)


def borrar_carrera_por_id(carrera_id):
    return str(db.carreras.delete_one({'_id': carrera_id}).deleted_count)


# Clase de operadores
def consultar_carreras(skip, limit):
    return dumps(db.carreras.find({}).skip(int(skip)).limit(int(limit)))


def agregar_curso(json):
    curso = consultar_curso_por_id_proyeccion(json['id_curso'], {"nombre": 1})
    return str(db.carreras.update_one({"_id" : ObjectId(json['id_carrera'])}, {"$addToSet": {"cursos": curso}}).modified_count)


def borrar_curso_de_carrera(json):
    return str(db.carreras.update_one({"_id" : ObjectId(json['id_carrera'])}, {'$pull' : {'cursos' : {'_id': ObjectId(json['id_curso'])}}}).modified_count)

# -----------------Cursos-------------------------


def crear_curso(json):
    return str(db.cursos.insert_one(json).inserted_id)


def consultar_curso_por_id(id_curso):
    return dumps(db.cursos.find_one({"_id" : ObjectId(id_curso) })) ##dumps => From bson to json


def actualizar_curso(curso):
    # Esta funcion solamente actualiza nombre, descripcion y clases del curso
    return db.cursos.update_one({"_id" : ObjectId(curso['_id'])}, {'$set': {
        "nombre": curso['nombre'],
        "descripcion": curso['descripcion'],
        "clases": curso['clases']
    }}).modified_count


def borrar_curso_por_id(curso_id):
    return db.cursos.delete_one({"_id" : ObjectId(curso_id)}).deleted_count


def consultar_curso_por_id_proyeccion(id_curso, proyeccion=None):
    return db.cursos.find_one({"_id" : ObjectId(id_curso)}, proyeccion) ##Proyección para saber qué campos traer y qué campos no


def consultar_curso_por_nombre(nombre):
    ## db.cursos.createIndex({nombre: 'text'}) ##Desde la consola
    return dumps(db.cursos.find({'$text' : {'$search' : nombre}})) ## Necesita un indice de texto para ejecutar

