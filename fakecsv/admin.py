from django.contrib import admin

# Register your models here.

from .models import Schema, Column, DataSet

admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(DataSet)