from crispy_forms.layout import Layout, Field
from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from address.forms import AddressField
from account.models import Account
from crispy_forms.helper import FormHelper
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class AnnonceForm(ModelForm):
    class Meta:
        model = Annonce
        fields = ['categorie_logement', 'type_location_choices']

    def __init__(self, *args, **kwargs):
        super(AnnonceForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class LoggedForm(ModelForm):
    class Meta:
        model = Annonce
        fields = ['categorie_logement', 'type_location_choices']

    def __init__(self, *args, **kwargs):
        super(LoggedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

TYPE_UTILISATEUR_CHOICES = [
    ('locataire', 'Locataire'),
    ('proprietaire', 'Propriétaire'),
    ('partenaire', 'Partenaire'),
]

class CreateUserForm(UserCreationForm):
    type_utilisateur = forms.ChoiceField(
        choices=TYPE_UTILISATEUR_CHOICES,
        label="Type d'utilisateur",
        widget=forms.Select(attrs={'id': 'id_type_utilisateur'})
    )

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('email','first_name','last_name','telephone','type_utilisateur','typelocataire')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class DescriptionForm(ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre_logement','description','nombre_personne', 'pieces_couchage', 'hebergement_choice', 'type_location_choices']
        widgets = {
            'titre_logement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du logement'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée du logement'}),
            'nombre_personne': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'pieces_couchage': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'hebergement_choice': forms.Select(attrs={'class': 'form-control'}),
            'type_location_choices': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class EquipmentForm(ModelForm):
    class Meta:
        model = Annonce
        fields = ['equipements']

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['services']

    services = forms.ModelMultipleChoiceField(
        queryset=Services.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class CategorieServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['categorie']

    def __init__(self, *args, **kwargs):
        super(CategorieServicesForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'


class FormLoyer(ModelForm):
    class Meta:
        model = Annonce
        fields = ['loyer_tc', 'charges_loyer']

    def __init__(self, *args, **kwargs):
        super(FormLoyer, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class FormCalendrier(ModelForm):
    class Meta:
        model = Calendrier
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormCalendrier, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class FormCondition(ModelForm):
    class Meta:
        model = Condition
        exclude = ['annonce']

    def __init__(self, *args, **kwargs):
        super(FormCondition, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class FormEquipement(ModelForm):
    class Meta:
        model = Equipement
        exclude = ['annonce']

    def __init__(self, *args, **kwargs):
        super(FormEquipement, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class FormDiagnostic(ModelForm):
    class Meta:
        model = Diagnostic
        exclude = ['annonce']
        labels = {
            'consommationNrj' : 'Consommations énergétiques en kWhEP/m²/an',
            'emissionGaz' : 'Émissions de gaz à effet de serre (GES) en kgéqCO2/m²/an',
            'risqueNaturel' : 'Risques naturels et technologiques',
            'risquePlomb' : "Risques d'exposition au plomb",
            'interieurElecGaz' : 'Installation intérieure électricité et gaz',
            'amianteDoc' : "État mentionnant l'absence de matériaux contenant de l'amiante",
            'copopriete' : 'Extrait du règlement de copropriété',
            'docPerformance': 'Diagnostic de Performance Énergétique',
        }

    def __init__(self, *args, **kwargs):
        super(FormDiagnostic, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class UserModif(ModelForm):
    class Meta:
        model = Account
        fields = ('email','first_name','last_name','telephone','typelocataire')

    def __init__(self, *args, **kwargs):
        super(UserModif, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class VerifImage(ModelForm):
    class Meta:
        model = Account
        fields = ('photo_profil', 'photo_identite')

    def __init__(self, *args, **kwargs):
        super(VerifImage, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class ImageForm(ModelForm):
    class Meta:
        model = ImageLogement
        fields = ['images']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class DureeLOcationForm(ModelForm):
    class Meta:
        model = Annonce
        fields = ['dureeLocationMini', 'dureeLocationMaxi']

    def __init__(self, *args, **kwargs):
        super(DureeLOcationForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'


class PlanPaiementCautionForm(forms.ModelForm):
    class Meta:
        model = PlanPaiementCaution
        fields = ['montant_caution_total', 'nombre_mensualites']

    def __init__(self, *args, **kwargs):
        super(PlanPaiementCautionForm, self).__init__(*args, **kwargs)
        self.fields['nombre_mensualites'].widget = forms.Select(choices=[
            (1, '1 mois'),
            (2, '2 mois'),
            (3, '3 mois'),
            (6, '6 mois'),
            (12, '12 mois')
        ])
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

class PaiementMensuelForm(forms.ModelForm):
    class Meta:
        model = PaiementMensuelCaution
        fields = ['reference_paiement']

    def __init__(self, *args, **kwargs):
        super(PaiementMensuelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'