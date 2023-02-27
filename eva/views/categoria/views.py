from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Categoria, Ciclo, Ciclo2
from eva.forms import CategoriaForm
from django.http import JsonResponse
from auditoria.apps import GeneradorAuditoria

m_Proceso = "CATEGORIA"
m_NombreTabla = "pt_categoria"
class CategoryListView(ListView):
    model = Categoria
    template_name = 'categoria/list.html'
    success_url = reverse_lazy('eva:list-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Categorias'
        #cycle = Ciclo.objects.filter(is_active=True).first()
        #context['pageview'] = cycle.name
        context['object_list'] = Categoria.objects.all()
        context['create_url'] = reverse_lazy('eva:create-category')
        context['url_list'] = reverse_lazy('eva:list-category')
        return context

class CategoryCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categoria/create.html"
    success_url = reverse_lazy('eva:list-category')
    
    def post(self, request, *args, **kwargs):
        response = None
        try:
            if request.is_ajax():
                updated_request = request.POST.copy()
                updated_request.update({'ciclo_id': self.request.session.get('cicloId')})
                form = self.form_class(updated_request)
                if form.is_valid():
                    form.save()
                    message = f'{self.model.__name__} registrada correctamente'
                    error = 'No han ocurrido errores'
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 201
                    newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTabla)
                    GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTabla, newJson, request.user.id)
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo registrar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(error), request.user.id)
                    return response
        except Exception as e:
            message = 'error'
            response = JsonResponse({'message': message, 'error': str(e)})
            GeneradorAuditoria().CrearAuditoriaError(m_Proceso, str(e), request.user.id)
        return JsonResponse(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Categoria'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-category')
        return context

class CategoryUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categoria/update.html"
    success_url = reverse_lazy('eva:list-category')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
           if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
                message = f'{self.model.__name__} actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 201
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTabla, kwargs["pk"], newJson, oldJson, request.user.id)
                return response
            else:
                message = f'{self.model.__name__} no se pudo actualizar!'
                error = form.errors
                response = JsonResponse({'message': message, 'error': error})
                response.status_code = 400
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_Proceso, str(error), request.user.id)
                return response
        except Exception as e:
            data['error'] = str(e)
            GeneradorAuditoria().CrearAuditoriaError(m_Proceso, str(e), request.user.id)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Categoria'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-category')
        return context

class CategoryDeleteView(DeleteView):
    model = Categoria
    success_url = reverse_lazy('eva:list-category')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTabla, kwargs)
            category = self.get_object()
            category.state = False
            category.save()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTabla, kwargs["pk"], oldJson, request.user.id)
            return response
        else:
            return redirect('eva:list-category')
