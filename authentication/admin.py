from django.contrib import admin

from authentication.models import Usuario
from authentication.models import Post

admin.site.register(Usuario)

admin.site.register(Post)
