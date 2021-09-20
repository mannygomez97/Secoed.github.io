from django.urls import reverse_lazy
from django.views.generic import ListView

from eva.models import Usuario, Ciclo


class TeacherListView(ListView):
    model = Usuario
    template_name = 'docente/list.html'
    success_url = reverse_lazy('eva:list-teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Nomina de Docente'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['object_list'] = Usuario.objects.filter(roles=3)
        context['url_list'] = reverse_lazy('eva:list-teacher')
        return context


class TeacherCoevaluatorListView(ListView):
    model = Usuario
    template_name = 'docente/list.html'
    success_url = reverse_lazy('eva:list-coevaluators')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Nomina de Coevaluadores'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['object_list'] = Usuario.objects.filter(roles=2)
        context['url_list'] = reverse_lazy('eva:list-coevaluators')
        return context

