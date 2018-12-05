from django.contrib import admin
from map.models import Geodata


class GeodataAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Geodata, GeodataAdmin)
