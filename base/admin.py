from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Graph)
admin.site.register(Node)
admin.site.register(Content)
admin.site.register(Link)
