from django.apps import AppConfig
from django.db import connection
import datetime

class AuditoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditoria'

# Métodos para el registro de auditorías
m_CreateAccion = "CREATE"
m_UpdateAccion = "UPDATE"
m_DeleteAccion = "DELETE"
class GeneradorAuditoria:
    def GenerarAuditoriaCrear(self, nombreTabla, jsonNew, idUsuario):
        InsertAuditoria(nombreTabla, m_CreateAccion, jsonNew, "", idUsuario)
    def GenerarAuditoriaActualizar(self, nombreTabla, jsonNew, jsonOld, idUsuario):
        InsertAuditoria(nombreTabla, m_UpdateAccion, jsonNew, jsonOld, idUsuario)
    def GenerarAuditoriaBorrar(self, nombreTabla, jsonOld, idUsuario):
        InsertAuditoria(nombreTabla, m_DeleteAccion, "", jsonOld, idUsuario)

# Métodos para el registro de errores
class GeneradorErrores:
    i = 0

# Métodos adicionales
def InsertAuditoria(tablaName, command, jsonNew, jsonOld, idUsuario):
    base_sql = "INSERT INTO TB_AUDITORIA (tabla, comando, registroNuevo, registroAnterior, idUsuarioCreacion, fechaCreacion) " \
       "VALUES (%s, %s, %s, %s, %s, %s);"
    fechaHoraActual = datetime.datetime.now()
    valores = [
        tablaName, command, jsonNew, jsonOld, idUsuario, fechaHoraActual
    ]
    curs = connection.cursor()
    curs.execute(base_sql, valores)