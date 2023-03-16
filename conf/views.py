import json
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from numpy import delete

from authentication.models import RolUser
from conf.forms import *
from conf.models import *


from authentication.models import Usuario
from django.shortcuts import render, redirect
from auditoria.apps import GeneradorAuditoria

# CONSTANTES
m_NombreTablaMenu= "conf_menu"
m_ProcesoMenu = "MENU"
class MenuContentView(View):
    def get(self, request):
        menusview = Menu.objects.order_by('orden')
        modulos = Modulo.objects.order_by('descripcion')
        menusItem = Menu.objects.exclude(url__isnull=False).exclude(modulo_id__isnull=True).order_by('descripcion')
        greeting = {'heading': "Menu", 'pageview': "Administración", "menusview": menusview}
        return render(request, 'conf/menu.html', greeting)

    # Metodo para guardar un nuevo menu
    def newMenu(request):
        if request.method == 'POST':
            menuForm = MenuForm(request.POST)
            if menuForm.is_valid():
                menuForm.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaMenu)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaMenu, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoMenu, "No se puedo registrar", request.user.id)
            return redirect('menu')
        else:
            menuFormView = MenuForm()
            menu = Menu()
            view = False
            context = {'menuFormView': menuFormView, 'menu': menu, 'view': view}
        return render(request, 'conf/menuForm.html', context)

    # Consulta el registro de un menu por su pk
    def viewMenu(request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        menuFormView = MenuForm(instance=menu)
        view = True
        context = {'menuFormView': menuFormView, 'menu': menu, 'view': view}
        return render(request, 'conf/menuForm.html', context)

    # Editar los datos de un menu por su pk
    def editMenu(request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if request.method == 'POST':
            ##editarField
            request.POST._mutable = True
            request.POST['descripcion'] = request.POST['descripcion'].capitalize()
            request.POST['key'] = request.POST['descripcion'].replace(" ", "_").lower() + "_" + request.POST['orden']
            if request.POST['modulo_id'] and request.POST['parent_id']:
                request.POST['modulo_id'] = ''
            request.POST._mutable = False
            # endEditarField
            form = MenuForm(request.POST, instance=menu)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaMenu, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaMenu, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaMenu, kwargs["pk"], newJson, oldJson,
                                                                request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('menu')
        else:
            menuFormView = MenuForm(instance=menu)
            view = False
            context = {'menuFormView': menuFormView, 'menu': menu, 'view': view}
        return render(request, 'conf/menuForm.html', context)

    # Elimina un registro del menu
    def deleteMenu(request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if menu:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaMenu, kwargs)
            menu.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaMenu, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('menu')

    # AJAX
    def loadMenus(request):
        modulo_id = request.GET.get('modulo_id')
        menus = Menu.objects.filter(Q(modulo_id=modulo_id) & (Q(href__isnull=True) | Q(href=''))).order_by(
            'descripcion')
        return render(request, 'conf/menuList.html', {'menus': menus})

# CONSTANTES
m_NombreTablaModulo = "conf_modulo"
m_ProcesoModulo = "MODULO"
class ModuloContentView(View):

    # Carga los datos iniciales del HTML
    def get(self, request):
        modulos = Modulo.objects.order_by('orden')
        greeting = {'heading': "Modulo", 'pageview': "Administración", 'modulosview': modulos}
        return render(request, 'conf/modulo.html', greeting)

    # Metodo para guardar un nuevo modulo
    def newModulo(request):
        if request.method == 'POST':
            ##editarField
            request.POST._mutable = True
            request.POST['descripcion'] = request.POST['descripcion'].capitalize()
            request.POST['key'] = request.POST['descripcion'].replace(" ", "_").lower() + "_" + request.POST['orden']
            request.POST._mutable = False
            # endEditarField
            modForm = ModuloForm(request.POST)
            if modForm.is_valid():
                modForm.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaModulo)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaModulo, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoModulo, "No se puedo registrar", request.user.id)
            return redirect('modulo')
        else:
            moduloFormView = ModuloForm();
            modulo = Modulo()
            view = False
            context = {'moduloFormView': moduloFormView, 'modulo': modulo, 'view': view}
        return render(request, 'conf/moduloForm.html', context)

    # Consulta el registro de un modulo por su pk
    def viewModulo(request, pk):
        modulo = get_object_or_404(Modulo, pk=pk)
        moduloFormView = ModuloForm(instance=modulo)
        view = True
        context = {'moduloFormView': moduloFormView, 'modulo': modulo, 'view': view}
        return render(request, 'conf/moduloForm.html', context)

    # Editar los datos de un modulo por su pk
    def editModulo(request, pk):
        modulo = get_object_or_404(Modulo, pk=pk)
        if request.method == 'POST':
            ##editarField
            request.POST._mutable = True
            request.POST['descripcion'] = request.POST['descripcion'].capitalize()
            request.POST['key'] = request.POST['descripcion'].replace(" ", "_").lower() + "_" + request.POST['orden']
            request.POST._mutable = False
            # endEditarField
            form = ModuloForm(request.POST, instance=modulo)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaModulo, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaModulo, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaModulo, kwargs["pk"], newJson, oldJson,
                                                                request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('modulo')
        else:
            moduloFormView = ModuloForm(instance=modulo)
            view = False
            context = {'moduloFormView': moduloFormView, 'modulo': modulo, 'view': view}
        return render(request, 'conf/moduloForm.html', context)

    # Elimina un registro del modulo
    def deleteModulo(request, pk):
        modulo = get_object_or_404(Modulo, pk=pk)
        if modulo:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaModulo, kwargs)
            modulo.delete()
            messages.success(request, "Se ha eliminado correctamente", "success")
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaModulo, kwargs["pk"], oldJson, request.user.id)
        return redirect('modulo')

# CONSTANTES
m_NombreTablaUniversidad = "conf_universidad"
m_ProcesoUniversidad = "UNIVERSIDAD"
class UniversidadContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        universidad = Universidad.objects.order_by('descripcion')
        greeting = {'heading': "Universidad", 'pageview': "Administración", 'universidadview': universidad}
        return render(request, 'conf/universidad.html', greeting)

    # Metodo para guardar un nuevo universidad
    def newUniversidad(request):
        if request.method == 'POST':
            universidadForm = UniversidadForm(request.POST)
            if universidadForm.is_valid():
                universidadForm.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaUniversidad)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaUniversidad, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoUniversidad, "No se puedo registrar",
                                                               request.user.id)
            return redirect('universidad')
        else:
            universidadFormView = UniversidadForm();
            universidad = Universidad()
            view = False
            context = {'universidadFormView': universidadFormView, 'universidad': universidad, 'view': view}
        return render(request, 'conf/universidadForm.html', context)

    # Consulta el registro de un universidad por su pk
    def viewUniversidad(request, pk):
        universidad = get_object_or_404(Universidad, pk=pk)
        universidadFormView = UniversidadForm(instance=universidad)
        view = True
        context = {'universidadFormView': universidadFormView, 'universidad': universidad, 'view': view}
        return render(request, 'conf/universidadForm.html', context)

    # Editar los datos de un universidad por su pk
    def editUniversidad(request, pk):
        universidad = get_object_or_404(Universidad, pk=pk)
        if request.method == 'POST':
            form = UniversidadForm(request.POST, instance=universidad)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaUniversidad, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaUniversidad, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaUniversidad, kwargs["pk"], newJson,
                                                                oldJson, request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('universidad')
        else:
            universidadFormView = UniversidadForm(instance=universidad)
            view = False
            context = {'universidadFormView': universidadFormView, 'universidad': universidad, 'view': view}
        return render(request, 'conf/universidadForm.html', context)

    # Elimina un registro del universidad
    def deleteUniversidad(request, pk):
        universidad = get_object_or_404(Universidad, pk=pk)
        if universidad:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaUniversidad, kwargs)
            universidad.delete()
            messages.success(request, "Se ha eliminado correctamente", "success")
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaUniversidad, kwargs["pk"], oldJson,
                                                        request.user.id)
        return redirect('universidad')

# CONSTANTES
m_NombreTablaFacultad = "conf_facultad"
m_ProcesoFacultad = "FACULTAD"
class FacultadContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        facultad = Facultad.objects.order_by('descripcion')
        greeting = {'heading': "Facultad", 'pageview': "Administración", 'facultadview': facultad}
        return render(request, 'conf/facultad.html', greeting)

    # Metodo para guardar un nuevo facultad
    def newFacultad(request):
        if request.method == 'POST':
            facultadForm = FacultadForm(request.POST)
            if facultadForm.is_valid():
                facultadForm.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaFacultad)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaFacultad, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoFacultad, "No se puedo registrar",
                                                               request.user.id)
            return redirect('facultad')
        else:
            facultadFormView = FacultadForm();
            facultad = Facultad()
            view = False
            context = {'facultadFormView': facultadFormView, 'facultad': facultad, 'view': view}
        return render(request, 'conf/facultadForm.html', context)

    # Consulta el registro de un facultad por su pk
    def viewFacultad(request, pk):
        facultad = get_object_or_404(Facultad, pk=pk)
        facultadFormView = FacultadForm(instance=facultad)
        view = True
        context = {'facultadFormView': facultadFormView, 'facultad': facultad, 'view': view}
        return render(request, 'conf/facultadForm.html', context)

    # Editar los datos de un facultad por su pk
    def editFacultad(request, pk):
        facultad = get_object_or_404(Facultad, pk=pk)
        if request.method == 'POST':
            form = FacultadForm(request.POST, instance=facultad)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaFacultad, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaFacultad, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaFacultad, kwargs["pk"], newJson,
                                                                oldJson, request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('facultad')
        else:
            facultadFormView = FacultadForm(instance=facultad)
            view = False
            context = {'facultadFormView': facultadFormView, 'facultad': facultad, 'view': view}
        return render(request, 'conf/facultadForm.html', context)

    # Elimina un registro del facultad
    def deleteFacultad(request, pk):
        facultad = get_object_or_404(Facultad, pk=pk)
        if facultad:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaFacultad, kwargs)
            facultad.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaFacultad, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('facultad')

# CONSTANTES
m_NombreTablaCarrera = "conf_carrera"
m_ProcesoCarrera = "CARRERA"
class CarreraContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        carrera = Carrera.objects.order_by('descripcion')
        greeting = {'heading': "Carrera", 'pageview': "Administración", 'carreraview': carrera}
        return render(request, 'conf/carrera.html', greeting)

    # Metodo para guardar un nuevo carrera
    def newCarrera(request):
        if request.method == 'POST':
            carreraForm = CarreraForm(request.POST)
            if carreraForm.is_valid():
                carreraForm.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaCarrera)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaCarrera, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoCarrera, "No se puedo registrar",
                                                               request.user.id)
            return redirect('carrera')
        else:
            carreraFormView = CarreraForm();
            carrera = Carrera()
            view = False
            context = {'carreraFormView': carreraFormView, 'carrera': carrera, 'view': view}
        return render(request, 'conf/carreraForm.html', context)

    # Consulta el registro de un carrera por su pk
    def viewCarrera(request, pk):
        carrera = get_object_or_404(Carrera, pk=pk)
        carreraFormView = CarreraForm(instance=carrera)
        view = True
        context = {'carreraFormView': carreraFormView, 'carrera': carrera, 'view': view}
        return render(request, 'conf/carreraForm.html', context)

    # Editar los datos de un carrera por su pk
    def editCarrera(request, pk):
        carrera = get_object_or_404(Carrera, pk=pk)
        if request.method == 'POST':
            form = CarreraForm(request.POST, instance=carrera)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCarrera, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCarrera, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaCarrera, kwargs["pk"], newJson,
                                                                oldJson, request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('carrera')
        else:
            carreraFormView = CarreraForm(instance=carrera)
            view = False
            context = {'carreraFormView': carreraFormView, 'carrera': carrera, 'view': view}
        return render(request, 'conf/carreraForm.html', context)

    # Elimina un registro del modulo
    def deleteCarrera(request, pk):
        carrera = get_object_or_404(Carrera, pk=pk)
        if carrera:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaCarrera, kwargs)
            carrera.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaCarrera, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('carrera')

# CONSTANTES
m_NombreTablaRol = "conf_rol"
m_ProcesoRol = "ROL"
class RolContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        rol = Rol.objects.order_by('descripcion')
        greeting = {'heading': "Roles del SECOED", 'pageview': "Administración", 'rolview': rol}
        return render(request, 'conf/roles.html', greeting)

    # Metodo para guardar un nuevo rol
    def newRol(request):
        if request.method == 'POST':
            rolForm = RolForm(request.POST)
            if rolForm.is_valid():
                rolForm.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaRol)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaRol, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoRol, "No se puedo registrar",
                                                               request.user.id)
            return redirect('roles')
        else:
            rolFormView = RolForm();
            rol = Rol()
            view = False
            context = {'rolFormView': rolFormView, 'rol': rol, 'view': view}
        return render(request, 'conf/rolesForm.html', context)

    # Consulta el registro de un rol por su pk
    def viewRol(request, pk):
        rol = get_object_or_404(Rol, pk=pk)
        rolFormView = RolForm(instance=rol)
        view = True
        context = {'rolFormView': rolFormView, 'rol': rol, 'view': view}
        return render(request, 'conf/rolesForm.html', context)

    # Editar los datos de un rol por su pk
    def editRol(request, pk):
        rol = get_object_or_404(Rol, pk=pk)
        if request.method == 'POST':
            form = RolForm(request.POST, instance=rol)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRol, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRol, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaRol, kwargs["pk"], newJson,
                                                                oldJson, request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('roles')
        else:
            rolFormView = RolForm(instance=rol)
            view = False
            context = {'rolFormView': rolFormView, 'rol': rol, 'view': view}
        return render(request, 'conf/rolesForm.html', context)

    # Elimina un registro del rol
    def deleteRol(request, pk):
        rol = get_object_or_404(Rol, pk=pk)
        if rol:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRol, kwargs)
            rol.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaRol, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('roles')

# CONSTANTES
m_NombreTablaRolMenu = "conf_rol_menu"
m_ProcesoRolMenu = "ROL-MENU"
class RolMenuContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        rolesMenu = RolMenu.objects.order_by('descripcion')
        greeting = {'heading': "Roles de menú del SECOED", 'pageview': "Administración", 'rolesMenuView': rolesMenu}
        return render(request, 'conf/rolMenu.html', greeting)

    # Elimina un registro del rol-usuario
    def deleteRolMenu(request, pk):
        rol = get_object_or_404(RolMenu, pk=pk)
        if rol:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRolMenu, kwargs)
            rol.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaRolMenu, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('roles-menu')

# CONSTANTES
m_NombreTablaRolMenu = "conf_rol_user"
m_ProcesoRolMenu = "ROL-USUARIO"
class RolUsuarioContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        rolesUsuario = RolUser.objects.order_by('descripcion')
        greeting = {'heading': "Roles de usuario del SECOED", 'pageview': "Administración",
                    'rolesUsuarioView': rolesUsuario}
        return render(request, 'conf/rolUsuarios.html', greeting)

    # Elimina un registro del rol-usuario
    def deleteRolUsuario(request, pk):
        rol = get_object_or_404(RolUser, pk=pk)
        if rol:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRolMenu, kwargs)
            rol.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaRolMenu, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('roles-usuario')

# CONSTANTES
m_NombreTablaRolMoodle = "conf_rol_moodle"
m_ProcesoRolMoodle = "ROL-MOODLE"
class RolMoodleContentView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        rolMoodle = RolMoodle.objects.order_by('codigo')
        greeting = {'heading': "Roles de Moodle", 'pageview': "Administración", 'rolMoodleView': rolMoodle}
        return render(request, 'conf/rolesMoodle.html', greeting)

    # Metodo para guardar un nuevo rol de moodle
    def newRolMoodle(request):
        if request.method == 'POST':
            rolMoodleFormView = RolMoodleForm(request.POST)
            if rolMoodleFormView.is_valid():
                rolMoodleFormView.save()
                newJson = GeneradorAuditoria().GenerarJSONNuevo(m_NombreTablaRolMoodle)
                GeneradorAuditoria().GenerarAuditoriaCrear(m_NombreTablaRolMoodle, newJson, request.user.id)
                messages.success(request, "Se registro correctamente", "success")
            else:
                messages.error(request, "No se puedo registrar", "error")
                GeneradorAuditoria().CrearAuditoriaAdvertencia(m_ProcesoRolMoodle, "No se puedo registrar",
                                                               request.user.id)
            return redirect('roles-moodle')
        else:
            rolMoodleFormView = RolMoodleForm();
            rolMoodle = RolMoodle()
            view = False
            context = {'rolMoodleFormView': rolMoodleFormView, 'rolMoodle': rolMoodle, 'view': view}
        return render(request, 'conf/rolMoodleForm.html', context)

    # Consulta el registro de un rol de moodle por su pk
    def viewRolMoodle(request, pk):
        rolMoodle = get_object_or_404(RolMoodle, pk=pk)
        rolMoodleFormView = RolMoodleForm(instance=rolMoodle)
        view = True
        context = {'rolMoodleFormView': rolMoodleFormView, 'rolMoodle': rolMoodle, 'view': view}
        return render(request, 'conf/rolMoodleForm.html', context)

    # Editar los datos de un rol de moodle por su pk
    def editRolMoodle(request, pk):
        rolMoodle = get_object_or_404(RolMoodle, pk=pk)
        if request.method == 'POST':
            form = RolMoodleForm(request.POST, instance=rolMoodle)
            if form.is_valid():
                kwargs = {'pk': pk}
                oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRolMoodle, kwargs)
                form.save()
                newJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRolMoodle, kwargs)
                GeneradorAuditoria().GenerarAuditoriaActualizar(m_NombreTablaRolMoodle, kwargs["pk"], newJson,
                                                                oldJson, request.user.id)
                messages.success(request, "Se edito correctamente", "success")
                return redirect('roles-moodle')
        else:
            rolMoodleFormView = RolMoodleForm(instance=rolMoodle)
            view = False
            context = {'rolMoodleFormView': rolMoodleFormView, 'rolMoodle': rolMoodle, 'view': view}
        return render(request, 'conf/rolMoodleForm.html', context)

    # Elimina un registro del rol de moodle
    def deleteRolMoodle(request, pk):
        rolMoodle = get_object_or_404(RolMoodle, pk=pk)
        if rolMoodle:
            kwargs = {'pk': pk}
            oldJson = GeneradorAuditoria().GenerarJSONExistente(m_NombreTablaRolMoodle, kwargs)
            rolMoodle.delete()
            GeneradorAuditoria().GenerarAuditoriaBorrar(m_NombreTablaRolMoodle, kwargs["pk"], oldJson, request.user.id)
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('roles-moodle')


