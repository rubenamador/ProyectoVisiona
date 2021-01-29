from django.contrib import admin

from apps.Nodes.models import Node, Port

# Register your models here.
admin.site.register(Node)
admin.site.register(Port)
