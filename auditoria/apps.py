from django.apps import AppConfig
from django.db import connection
import datetime
import pandas as pq

class AuditoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit'

# Métodos para el registro de auditorías
m_CreateAccion = "CREATE"
m_UpdateAccion = "UPDATE"
m_DeleteAccion = "DELETE"

m_TipoAdvertencia = "WARNING"
m_TipoError = "ERROR"

class DatoFormulario:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

class GeneradorAuditoria:
    def GenerarAuditoriaCrear(self, nombreTabla, jsonNew, idUsuario):
        idRegistro = GetLastId(nombreTabla)
        InsertAuditoria(nombreTabla, idRegistro, m_CreateAccion, jsonNew, "", idUsuario)
    def GenerarAuditoriaActualizar(self, nombreTabla, idRegistro, jsonNew, jsonOld, idUsuario):
        InsertAuditoria(nombreTabla, idRegistro, m_UpdateAccion, jsonNew, jsonOld, idUsuario)
    def GenerarAuditoriaBorrar(self, nombreTabla, idRegistro, jsonOld, idUsuario):
        InsertAuditoria(nombreTabla, idRegistro, m_DeleteAccion, "", jsonOld, idUsuario)

    # Métodos para generar JSON
    def GenerarJSONExistente(self, nombreTabla, idDictionary):
        return generateSelectJSON(nombreTabla, idDictionary)
    def GenerarJSONNuevo(self, nombreTabla):
        return generateSelectJSON(nombreTabla, {'pk': GetLastId(nombreTabla)})

    # Métodos para el registro de errores
    def CrearAuditoriaAdvertencia(self, proceso, excepcion, idUsuario):
        InsertError(proceso, m_TipoAdvertencia, excepcion, idUsuario)
    def CrearAuditoriaError(self, proceso, excepcion, idUsuario):
        InsertError(proceso, m_TipoError, excepcion, idUsuario)

# Métodos adicionales
def InsertAuditoria(tablaName, idRegistro, command, jsonNew, jsonOld, idUsuario):
    base_sql = "INSERT INTO TB_AUDITORIA (tabla, idRegistro, comando, registroNuevo, registroAnterior, idUsuarioCreacion, fechaCreacion) " \
       "VALUES (%s, %s, %s, %s, %s, %s, %s);"
    fechaHoraActual = datetime.datetime.now()
    valores = [
        tablaName, idRegistro, command, jsonNew, jsonOld, idUsuario, fechaHoraActual
    ]
    curs = connection.cursor()
    curs.execute(base_sql, valores)

def InsertError(proceso, tipoError, excepcion, idUsuario):
    base_sql = "INSERT INTO TB_ERRORES (proceso, tipo, excepcion, idUsuario, fechaCreacion) " \
               "VALUES (%s, %s, %s, %s, %s);"
    fechaHoraActual = datetime.datetime.now()
    valores = [
        proceso, tipoError, excepcion, idUsuario, fechaHoraActual
    ]
    curs = connection.cursor()
    curs.execute(base_sql, valores)

def GetPrimaryKeyColumnName(nombreTabla):
    base_sql = "SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)" \
                "WHERE  i.indrelid = '" + nombreTabla + "'::regclass AND i.indisprimary;"
    curs = connection.cursor()
    curs.execute(base_sql)
    return curs.fetchone()[0]

def GetLastId(nombreTabla):
    pkField = GetPrimaryKeyColumnName(nombreTabla)
    base_sql = "SELECT coalesce(MAX(" + pkField + "), 0) FROM " + nombreTabla
    curs = connection.cursor()
    curs.execute(base_sql)
    return curs.fetchone()[0]

def generateSelectJSON(nombreTabla, idDictionary):
    primaryKeyFild = GetPrimaryKeyColumnName(nombreTabla)
    base_sql = "SELECT * FROM " + nombreTabla + " WHERE " + primaryKeyFild + " = " + str(idDictionary["pk"])
    curs = connection.cursor()
    curs.execute(base_sql)
    sqlDatas = curs.fetchone()

    data = []
    for sqlData in sqlDatas:
        if type(sqlData).__name__ == 'datetime':
            date_string = f'{sqlData:%Y-%m-%d %H:%M:%S}'
            data.append(str(date_string))
        else:
            data.append(str(sqlData))
        a = 1

    cols = list(map(lambda x: x[0], curs.description))
    lista = pq.DataFrame([data], columns=cols)
    return lista.to_json(orient ='records')