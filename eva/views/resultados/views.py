from django.views.generic import TemplateView
from eva.models import ResultadoProceso

class Resultado(TemplateView):
    model = ResultadoProceso
    template_name = 'resultados/resultadosProceso.html'

    def get_resultados(self):
        result = ResultadoProceso.objects.all()
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Resultados'
        context['resultados'] = self.get_resultados()
        return context
