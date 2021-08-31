from django.contrib.auth.models import AnonymousUser

from conf.models import Menu, Modulo


def load_menu(request):
    modulos = []

    if isinstance(request.user, AnonymousUser) == False:
        if request.user.usuario_administrador == True:
            modulos = Modulo.objects.order_by('orden')
            setMenus(modulos)
        else:
            aux = 0
            modList = Modulo.objects.order_by('orden')
            for x in modList:
                menuList1 = Menu.objects.filter(modulo_id=x)
                for x1 in menuList1:
                    if x1.href == '':
                        print("")
                    else:
                        menuList2 = Menu.objects.filter(parent_id=x1)
                        for x2 in menuList2:
                            print(x2)
    greeting = {'modulo': modulos}
    return greeting


def setMenuItem(menu):
    for item in menu:
        item.items = Menu.objects.filter(parent_id=item.id)
        if item.items:
            setMenuItem(item.items)


def setMenus(modulos):
    for mod in modulos:
        mod.menus = Menu.objects.filter(modulo_id=mod.id)
        setMenuItem(mod.menus)
