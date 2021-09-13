from django.contrib.auth.models import AnonymousUser

from authentication.models import RolUser
from conf.models import Menu, Modulo, RolMenu


def load_menu(request):
    context = {}
    if isinstance(request.user, AnonymousUser):
        return context
    else:
        # Cargar menu si es administrador:
        if request.user.usuario_administrador:
            modulos = Modulo.objects.order_by('orden')
            setMenus(modulos)
            context['modulo'] = modulos
            return context
        # Cargar menu si no es administrador
        else:
            arrayModulo = []
            rolUsuario = RolUser.objects.filter(user_id=request.user.id)
            rolMenu = RolMenu.objects.filter(rol__id__in=rolUsuario)
            for x in rolMenu:
                print(x.id)
                print(x.menu.parent_id)
                print(x.menu.modulo_id)
            context['modulo'] = arrayModulo
            return context


def setMenuItem(menu):
    for item in menu:
        item.items = Menu.objects.filter(parent_id=item.id)
        if item.items:
            setMenuItem(item.items)


def setMenus(modulos):
    for mod in modulos:
        mod.menus = Menu.objects.filter(modulo_id=mod.id)
        setMenuItem(mod.menus)
