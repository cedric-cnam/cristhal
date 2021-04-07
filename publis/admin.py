from django.contrib import admin

from .models import Config, Collection, Referentiel, ClassementPubli, Source, Publication

class ReferentielAdmin(admin.ModelAdmin):
    search_fields = ["titre"]

class PubliAdmin(admin.ModelAdmin):
    search_fields = ["titre"]

admin.site.register(Config)
admin.site.register(Collection)
admin.site.register(Source)
admin.site.register(Publication, PubliAdmin)
#admin.site.register(Referentiel, ReferentielAdmin)
admin.site.register(ClassementPubli)