from .models import *
from django.forms import ModelForm
from django import forms


class ClientForm(ModelForm):
    class Meta:
        model = ClientCli
        widgets = {'cli_horaire_debut': forms.TimeInput(format='%H:%M')}
        fields = ['cli_nom', 'cli_prenom', 'cli_situation',
                  'cli_contact', 'cli_email', 'cli_noumber_of_pesons', 'cli_adresse_professionnelle',
                  'cli_pays', 'cli_ville', 'cli_lieu_recherche', 'cli_type_bien', 'cli_pack',
                  'cli_budget', 'cli_salaire_total', 'cli_montant_declare', 'cli_type', 'cli_planning',
                  'cli_horaire_debut',
                  'cli_horaire_fin', 'cli_motif', 'cli_document_avis', 'cli_document_paye', 'cli_document_quittance',
                  'cli_referent']


class SignerForm(ModelForm):
    class Meta:
        model = SignerCli
        widgets = {'cli_horaire_debut': forms.TimeInput(format='%H:%M')}
        fields = ['cli_nom', 'cli_prenom', 'cli_email', 'cli_document_avis']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli_horaire_debut'].widget.attrs.update(
            {'class': 'vTimeField hasTimepicker', 'placeholder': 'heure', })
        self.fields['cli_horaire_fin'].widget.attrs.update(
            {'class': 'vTimeField hasTimepicker'})
