from django.contrib import admin

from .models import Config, Collection, TypesHAL, Auteur, ClassementPubli, Source, Publication, Referentiel

class ReferentielAdmin(admin.ModelAdmin):
    search_fields = ["titre"]

class PubliAdmin(admin.ModelAdmin):
    search_fields = ["titre"]

class AuteurAdmin(admin.ModelAdmin):
    search_fields = ["prenom", "nom", "nom_complet"]
    
class ConfigAdmin(admin.ModelAdmin):
    fields = ("url_hal", ('annee_min_publis', 'annee_max_publis'), 
              'types_publis', 'repertoire_export')
    filter_horizontal = ('types_publis', )

admin.site.register(Config, ConfigAdmin)
admin.site.register(Collection)
admin.site.register(Source)
admin.site.register(Auteur, AuteurAdmin)
admin.site.register(TypesHAL)
admin.site.register(Publication, PubliAdmin)
admin.site.register(Referentiel, ReferentielAdmin)
admin.site.register(ClassementPubli)