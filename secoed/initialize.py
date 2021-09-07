from django.contrib.auth.models import AnonymousUser

from conf.models import Menu, Modulo


def load_menu(request):
    context = {}
    if isinstance(request.user, AnonymousUser):
        return context
    else:
        modulos  = Modulo.objects.order_by('orden')
        context['modulo'] = modulos
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
