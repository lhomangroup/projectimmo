# from Django.contrib.auth.signals import user_logged_in


from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from import_export import resources

from django.contrib import admin

from django.contrib.admin import AdminSite

from django.forms.models import BaseInlineFormSet

from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin

from django.db.models import Case, Count, Max, Min, Q, Sum


# Register your models here.

from django.apps import apps

from django.http import HttpResponseRedirect

from django.shortcuts import redirect

from django.shortcuts import render

from inline_actions.admin import InlineActionsModelAdminMixin

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from django.utils.safestring import mark_safe

from django.dispatch import receiver

from django.db.models.signals import *

from import_export.admin import ImportExportModelAdmin
from django.contrib import messages
from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
from soumission.models import checkboxcourses

admin.site.register(checkboxcourses)

@admin.register(PlanningPla)
class PlanningAdmin(admin.ModelAdmin):
    '''Admin View for Planning'''

    list_display = ('pla_intitule',)
    list_filter = ('pla_intitule',)


class VisiteAdmin(InlineActionsMixin, admin.TabularInline):

    pass
    model = VisiteVit
    list_display = ('cli', 'vit_commentaire', 'vit_date')

    #list_filter = ('cla', 'sal_code')

    #actions = ['get_emploi_temps', ]

    #exclude = ['pro_deleted']
# @admin.register(ClientCli)


# @admin.register(BilanBil)
class BilanAdmin(InlineActionsMixin, admin.TabularInline):

    pass
    model = BilanBil
    list_display = ('cli', 'bil_commentaire', 'bil_date')

    #list_filter = ('cla', 'sal_code')

    #actions = ['get_emploi_temps', ]

    #exclude = ['pro_deleted']


# @admin.register(RecommandationNek)
class RecommandationAdmin(InlineActionsMixin, admin.TabularInline):

    pass
    model = RecommandationNek
    list_display = ('cli', 'nek_recommandation', 'nek_date_recommandation')

    #list_filter = ('cla', 'sal_code')

    #actions = ['get_emploi_temps', ]

    exclude = ['nek_date_recommandation']


# @admin.register(RecommandationNek)
class CommentaireAdmin(InlineActionsMixin, admin.TabularInline):

    pass
    model = CommentaireDem
    list_display = ('cli', 'dem_commentaire', 'dem_date_commentaire')

    #list_filter = ('cla', 'sal_code')

    #actions = ['get_emploi_temps', ]

    exclude = ['dem_date_commentaire']


@admin.register(ClientCli)
class ClientAdmin(admin.ModelAdmin, InlineActionsModelAdminMixin):

    pass

    list_display = ('cli_nom', 'cli_prenom', 'cli_contact',
                    'validate', 'reunion')
    inlines = [RecommandationAdmin,
               CommentaireAdmin, VisiteAdmin, BilanAdmin, ]
    exclude = ['cli_decision_ok', 'cli_decision_reunion']
    #list_filter = ('cla', 'sal_code')

    #actions = ['get_emploi_temps', ]

    #exclude = ['pro_deleted']

    def validate_client(self, request, queryset):

        # soutenance_amount = self.sal.cla
        #ins = queryset[0].ins_id
        #scolarite = ScolariteSco.objects.all()
        return render(request,

                      'invoice.html',

                      context={

                      })
