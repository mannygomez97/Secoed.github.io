from django.db import models
from django.forms import model_to_dict
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import matplotlib.pyplot as plt
import time
from eva.models import Ciclo, Ciclo2

from django.views.generic import TemplateView
from eva.models import ParametrosGeneral, Parametro, Respuesta, Usuario


class ResultadoProcesos(models.Model):
    answer = models.ForeignKey(Respuesta, db_column='respuesta', null=False, blank=False, on_delete=models.CASCADE)
    cycle = models.IntegerField(null=False, blank=False, db_column='ciclo')
    user = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE, db_column='docente')
    coevaluator = models.CharField(max_length=10, null=True, blank=True, db_column='coevaluador')
    auto_result_Tic = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    auto_result_Did = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    auto_result_Ped = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Total_Proceso_Auto = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coe_result_Tic = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coe_result_Did = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coe_result_Ped = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Total_Proceso_Coe = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Total_Proceso = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date_created = models.DateTimeField(db_column='fecha_creacion', auto_now_add=True,
                                        help_text='Registra la fecha de creación de un valor')
    updated_at = models.DateTimeField(db_column='fecha_edicion', auto_now=True,
                                      help_text='Registra la fecha de creación de un valor')

    class Meta:
        managed = False
        db_table = "pt_resultado_proceso"


def rutaSemaforo(total):
    if (total <= 25.00):
        return 'static/images/eva/rojo.png'
    elif (total <= 60.00):
        return 'static/images/eva/amarillo.png'
    elif (total <= 94.99):
        return 'static/images/eva/verde.png'
    elif (total <= 100.00):
        return 'static/images/eva/azul.png'
    else:
        return 'static/images/eva/azul.png'


def notaAutoevaluacion(objeto, identificacion):
    ruta = "static/images/secoed/mtpl1_autoevaluacion" + identificacion + ".png"
    valores = [objeto.auto_result_Tic, objeto.auto_result_Did, objeto.auto_result_Ped]
    label_list = ['TICS - ' + str(objeto.auto_result_Tic), 'DIDÁCTICA - ' + str(objeto.auto_result_Did),
                  'PEDAGÓGIA - ' + str(objeto.auto_result_Ped)]
    colores = ['#957DAD', '#E0BBE4', '#D291BC']
    plt.clf()
    plt.pie(x=valores, labels=label_list, colors=colores, autopct='%1.2f%%', shadow=True)
    plt.title('NOTAS DE AUTOEVALUACIÓN')
    plt.savefig(ruta)
    return ruta


def notaCoevaluacion(objeto, identificacion):
    ruta = "static/images/secoed/mtpl1_coevaluacion_" + identificacion + ".png"
    valores = [objeto.coe_result_Tic, objeto.coe_result_Did, objeto.coe_result_Ped]
    label_list = ['TICS - ' + str(objeto.coe_result_Tic), 'DIDÁCTICA - ' + str(objeto.coe_result_Did),
                  'PEDAGÓGIA - ' + str(objeto.coe_result_Ped)]
    colores = ['#957DAD', '#E0BBE4', '#D291BC']
    plt.clf()
    plt.pie(x=valores, labels=label_list, colors=colores, autopct='%1.2f%%', shadow=True)
    plt.title('NOTAS DE COEVALUACIÓN')
    plt.savefig(ruta)
    return ruta


class Resultado(TemplateView):
    model = ResultadoProcesos
    template_name = 'resultados/resultadosProceso.html'

    def get_resultados(self):
        result = ResultadoProcesos.objects.all()
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Resultados'
        context['resultados'] = self.get_resultados()
        parameter = Parametro.objects.filter(name='Indicadores').first()
        context['parametros_Generales'] = ParametrosGeneral.objects.filter(parameter=parameter.id)
        return context

    def reporte_individual(request, pk):
        # Create the HttpResponse hearders with PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'atachment; filename = REPORTE_INDIVIDUAL.pdf'
        # Create PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        # Clase usuario
        resultadoOBJ = get_object_or_404(ResultadoProcesos, pk=pk)
        userObj = resultadoOBJ.user
        ciclo = get_object_or_404(Ciclo2, pk=resultadoOBJ.cycle)
        # Cabecera
        # title
        c.setFont("Times-Roman", 12)
        c.drawImage('static/images/secoed/logo-secoed.png', 480, 710, mask='auto', width=100, height=100)
        c.drawString(30, 790, 'FACULTAD: POR DEFINIR')
        c.drawString(30, 770, 'CARRERA: POR DEFINIR')
        c.drawString(30, 750, 'CICLO: ' + ciclo.nombre)
        c.drawString(30, 730, 'RESULTADOS EVALUACIÓN DOCENTE POR CARRERA')
        c.drawString(30, 710, (userObj.nombres + ' ' + userObj.apellidos))
        c.drawString(30, 690, 'COEVALUADOR: ' + resultadoOBJ.coevaluator)
        c.drawString(30, 670, 'FECHA DE EMISIÓN: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        c.drawString(510, 670, 'Pag.1/1')
        # cabecera detalle
        c.setFont("Times-Roman", 10)
        c.line(30, 645, 565, 645)
        c.drawString(30, 635, 'CATEGORÍA')
        c.drawString(150, 635, 'PEDAGOGÍA')
        c.drawString(270, 635, 'DIDÁCTICA')
        c.drawString(390, 635, 'TIC')
        c.drawString(510, 635, 'TOTAL')
        c.line(30, 630, 565, 630)
        # detalle autoevaluacion
        c.drawString(30, 615, 'AUTOEVALUACIÓN')
        c.drawString(150, 615, str(resultadoOBJ.auto_result_Ped))
        c.drawString(270, 615, str(resultadoOBJ.auto_result_Did))
        c.drawString(390, 615, str(resultadoOBJ.auto_result_Tic))
        c.drawString(510, 615, str(resultadoOBJ.Total_Proceso_Auto))
        # detalle coevaluacion
        c.drawString(30, 600, 'COEVALUACIÓN')
        c.drawString(150, 600, str(resultadoOBJ.coe_result_Ped))
        c.drawString(270, 600, str(resultadoOBJ.coe_result_Did))
        c.drawString(390, 600, str(resultadoOBJ.coe_result_Tic))
        c.drawString(510, 600, str(resultadoOBJ.Total_Proceso_Coe))
        # TOTAL DEL PROCESO
        c.setFont("Times-Roman", 18)
        c.drawString(30, 550, 'TOTAL, PROCESO: ' + str(resultadoOBJ.Total_Proceso))
        # semaforo
        c.setFont("Times-Roman", 12)
        c.drawString(250, 515, 'SEMÁFORO')
        c.drawImage(rutaSemaforo(resultadoOBJ.Total_Proceso), 180, 380, mask='auto', width=200, height=150)
        # DIAGRAMA PASTEL
        c.drawImage(notaAutoevaluacion(resultadoOBJ, userObj.identificacion), 30, 100, mask='auto', width=300,
                    height=280)
        c.drawImage(notaCoevaluacion(resultadoOBJ, userObj.identificacion), 300, 100, mask='auto', width=300,
                    height=280)
        # save
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


