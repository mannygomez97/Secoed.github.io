from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from eva.models import ResultadoProceso, Docente, Ciclo


class ProcessResultEvaluations(TemplateView):
    template_name = 'reports/results/result.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_graph_co_evaluation_by_category(self):
        data = []
        try:
            docente = Docente.objects.filter(user=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result_by_teacher = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values(
                'coe_result_Tic', 'coe_result_Did', 'coe_result_Ped').first()

            tic = ['Tics', float(result_by_teacher['coe_result_Tic'])]
            did = ['Didáctica', float(result_by_teacher['coe_result_Did'])]
            ped = ['Pedagógica', float(result_by_teacher['coe_result_Ped'])]

            data.append(tic)
            data.append(did)
            data.append(ped)
        except:
            pass
        return data

    def get_total_auto_evaluation(self):
        total_auto = []
        try:
            docente = Docente.objects.filter(user=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values('Total_Proceso_Auto').first()
            for r in result:
                tot = float(result['Total_Proceso_Auto'])
                total_auto.append(tot)
        except:
            pass
        return total_auto

    def get_total_auto(self):
        result = None
        try:
            docente = Docente.objects.filter(user=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).first()
        except:
            pass
        return result

    def get_total_co_evaluation(self):
        total_coe = []
        try:
            docente = Docente.objects.filter(user=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values('Total_Proceso_Coe').first()
            for r in result:
                tot = float(result['Total_Proceso_Coe'])
                total_coe.append(tot)
        except:
            pass
        return total_coe

    def get_graph_auto_evaluation_by_category(self):
        data = []
        try:
            docente = Docente.objects.filter(user=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result_by_teacher = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values(
                'auto_result_Tic', 'auto_result_Did', 'auto_result_Ped').first()

            tic = ['Tics', float(result_by_teacher['auto_result_Tic'])]
            did = ['Didáctica', float(result_by_teacher['auto_result_Did'])]
            ped = ['Pedagógica', float(result_by_teacher['auto_result_Ped'])]

            data.append(tic)
            data.append(did)
            data.append(ped)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Reporte de proceso'
        context['auto'] = self.get_total_auto()
        context['total_auto'] = self.get_total_auto_evaluation()
        context['total_coe'] = self.get_total_co_evaluation()
        context['graph_evaluation'] = self.get_graph_auto_evaluation_by_category()
        context['graph_co_evaluation'] = self.get_graph_co_evaluation_by_category()
        return context
