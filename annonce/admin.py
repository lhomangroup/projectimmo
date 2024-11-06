from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Annonce)
admin.site.register(Equipements)
admin.site.register(Charges)
#admin.site.register(ImageLogement)
admin.site.register(Calendrier)
admin.site.register(Condition)
admin.site.register(Diagnostic)
admin.site.register(AdressAnnonce)
admin.site.register(Services)
admin.site.register(CategorieService)
