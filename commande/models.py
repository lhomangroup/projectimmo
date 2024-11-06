from django.db import models
from client.models import Client
#from produit.models import Produit

# Create your models here.
class Commande(models.Model):
    STATUS=['non soumis','soumis','en instance','non livre','livre','livre',]
    LIVRE = 'Livré'
    NON_LIVRE = 'Non livré'
    EN_INSTANCE = 'En instance'
    SOUMIS = 'Soumis'
    NON_SOUMIS = 'Non soumis'
    STATUS = [
        (LIVRE, 'Livré'),
        (NON_LIVRE, 'Non livré'),
        (EN_INSTANCE, 'En instance'),
        (SOUMIS, 'Soumis'),
        (NON_SOUMIS, 'Non soumis'),
    ]
    client=models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
 #   produit=models.ForeignKey(Produit, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=200,
        null=True,
        choices=STATUS,
        default=NON_SOUMIS,
    )
    date_creation = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.client
